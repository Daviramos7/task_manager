import sqlite3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

DATABASE_NAME = 'tarefas.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def task_to_dict(row):
    if row is None:
        return None
    return dict(row)

class TaskApiHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, body, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(json.dumps(body).encode('utf-8'))

    def _get_task_id_from_path(self):
        try:
            return int(self.path.split('/')[-1])
        except (IndexError, ValueError):
            return None

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        conn = get_db_connection()
        cursor = conn.cursor()

        if path == '/tasks':
            cursor.execute("SELECT * FROM tarefas")
            tasks = [task_to_dict(row) for row in cursor.fetchall()]
            self._send_response(200, tasks)
        elif path.startswith('/tasks/'):
            task_id = self._get_task_id_from_path()
            if task_id is None:
                self._send_response(400, {'error': 'ID de tarefa inválido'})
                return

            cursor.execute("SELECT * FROM tarefas WHERE id =?", (task_id,))
            task = task_to_dict(cursor.fetchone())

            if task:
                self._send_response(200, task)
            else:
                self._send_response(404, {'error': 'Tarefa não encontrada'})
        else:
            self._send_response(404, {'error': 'Rota não encontrada'})
        
        conn.close()

    def do_POST(self):
        if self.path == '/tasks':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
            except (json.JSONDecodeError, TypeError, KeyError):
                self._send_response(400, {'error': 'Corpo da requisição inválido ou ausente'})
                return

            if 'titulo' not in data or not data['titulo']:
                self._send_response(400, {'error': 'O campo "titulo" é obrigatório'})
                return

            titulo = data['titulo']
            descricao = data.get('descricao', '')

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tarefas (titulo, descricao) VALUES (?,?)", (titulo, descricao))
            conn.commit()
            
            new_task_id = cursor.lastrowid
            cursor.execute("SELECT * FROM tarefas WHERE id =?", (new_task_id,))
            new_task = task_to_dict(cursor.fetchone())
            conn.close()

            self._send_response(201, new_task)
        else:
            self._send_response(404, {'error': 'Rota não encontrada'})

    def do_PUT(self):
        if self.path.startswith('/tasks/'):
            task_id = self._get_task_id_from_path()
            if task_id is None:
                self._send_response(400, {'error': 'ID de tarefa inválido'})
                return

            try:
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                data = json.loads(put_data)
            except (json.JSONDecodeError, TypeError, KeyError):
                self._send_response(400, {'error': 'Corpo da requisição inválido ou ausente'})
                return

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tarefas WHERE id =?", (task_id,))
            task = cursor.fetchone()

            if not task:
                self._send_response(404, {'error': 'Tarefa não encontrada'})
                conn.close()
                return

            titulo = data.get('titulo', task['titulo'])
            descricao = data.get('descricao', task['descricao'])
            status = data.get('status', task['status'])

            cursor.execute("""
                UPDATE tarefas SET titulo =?, descricao =?, status =?
                WHERE id =?
            """, (titulo, descricao, status, task_id))
            conn.commit()

            cursor.execute("SELECT * FROM tarefas WHERE id =?", (task_id,))
            updated_task = task_to_dict(cursor.fetchone())
            conn.close()

            self._send_response(200, updated_task)
        else:
            self._send_response(404, {'error': 'Rota não encontrada'})

    def do_DELETE(self):
        if self.path.startswith('/tasks/'):
            task_id = self._get_task_id_from_path()
            if task_id is None:
                self._send_response(400, {'error': 'ID de tarefa inválido'})
                return

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM tarefas WHERE id =?", (task_id,))
            task = cursor.fetchone()

            if not task:
                self._send_response(404, {'error': 'Tarefa não encontrada'})
                conn.close()
                return

            cursor.execute("DELETE FROM tarefas WHERE id =?", (task_id,))
            conn.commit()
            conn.close()

            self.send_response(204)
            self.end_headers()
        else:
            self._send_response(404, {'error': 'Rota não encontrada'})

def run_server(server_class=HTTPServer, handler_class=TaskApiHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor iniciado na porta {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

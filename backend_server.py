import sqlite3
import json
import time
import sys
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
    
    def log_performance(self, method, route, db_time, total_time, payload_size):
        db_ms = db_time * 1000
        total_ms = total_time * 1000
        
        print(f"\n📊 [ESTATÍSTICA] {method} {route}")
        print(f"   ├─ 💾 Tempo de Banco (SQL): {db_ms:.4f} ms")
        print(f"   ├─ ⚡ Tempo Total da API:   {total_ms:.4f} ms")
        print(f"   └─ 📦 Tamanho da Resposta:  {payload_size} bytes")

    def _send_response(self, status_code, body, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        response_bytes = json.dumps(body).encode('utf-8')
        self.wfile.write(response_bytes)
        return len(response_bytes)

    def _get_task_id_from_path(self):
        try:
            return int(self.path.split('/')[-1])
        except (IndexError, ValueError):
            return None

    def do_GET(self):
        start_time = time.time()
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        response_size = 0
        db_duration = 0

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if path == '/tasks':
                sql_start = time.time()
                cursor.execute("SELECT * FROM tarefas")
                rows = cursor.fetchall()
                db_duration = time.time() - sql_start
                
                tasks = [task_to_dict(row) for row in rows]
                response_size = self._send_response(200, tasks)
                
            elif path.startswith('/tasks/'):
                task_id = self._get_task_id_from_path()
                if task_id is None:
                    self._send_response(400, {'error': 'ID inválido'})
                    return

                sql_start = time.time()
                cursor.execute("SELECT * FROM tarefas WHERE id =?", (task_id,))
                row = cursor.fetchone()
                db_duration = time.time() - sql_start
                
                task = task_to_dict(row)

                if task:
                    response_size = self._send_response(200, task)
                else:
                    self._send_response(404, {'error': 'Não encontrada'})
            else:
                self._send_response(404, {'error': 'Rota não encontrada'})
        
        finally:
            conn.close()
            total_duration = time.time() - start_time
            if path.startswith('/tasks'):
                self.log_performance("GET", path, db_duration, total_duration, response_size)

    def do_POST(self):
        start_time = time.time() 
        db_duration = 0
        response_size = 0
        
        if self.path == '/tasks':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
            except:
                self._send_response(400, {'error': 'Erro no Body'})
                return

            if 'titulo' not in data:
                self._send_response(400, {'error': 'Titulo obrigatório'})
                return

            titulo = data['titulo']
            descricao = data.get('descricao', '')

            conn = get_db_connection()
            cursor = conn.cursor()
            
            sql_start = time.time()
            cursor.execute("INSERT INTO tarefas (titulo, descricao) VALUES (?,?)", (titulo, descricao))
            conn.commit()
            new_id = cursor.lastrowid
            cursor.execute("SELECT * FROM tarefas WHERE id =?", (new_id,))
            new_task = task_to_dict(cursor.fetchone())
            db_duration = time.time() - sql_start
            
            conn.close()

            response_size = self._send_response(201, new_task)
            
            total_duration = time.time() - start_time # ⏱️ FIM
            self.log_performance("POST", "/tasks", db_duration, total_duration, response_size)
        else:
            self._send_response(404, {'error': 'Rota não encontrada'})

    def do_PUT(self):
        self._send_response(501, {'error': 'Não instrumentado para teste'})
        
    def do_DELETE(self):
         self._send_response(501, {'error': 'Não instrumentado para teste'})

def run_server(server_class=HTTPServer, handler_class=TaskApiHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"🚀 Servidor de Alta Performance iniciado na porta {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
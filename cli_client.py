import requests
import json

BASE_URL = 'http://localhost:8000'

def print_task(task):
    print("-" * 30)
    print(f"ID: {task['id']}")
    print(f"Título: {task['titulo']}")
    print(f"Descrição: {task.get('descricao', 'N/A')}")
    print(f"Status: {task['status']}")
    print(f"Criado em: {task['criado_em']}")
    print("-" * 30)

def list_tasks():
    try:
        response = requests.get(f"{BASE_URL}/tasks")
        if response.status_code == 200:
            tasks = response.json()
            if not tasks:
                print("Nenhuma tarefa encontrada.")
            else:
                print("\n--- Lista de Tarefas ---")
                for task in tasks:
                    print_task(task)
        else:
            print(f"Erro ao buscar tarefas: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Erro de conexão: Não foi possível conectar ao servidor.")

def add_task():
    titulo = input("Título da tarefa: ")
    descricao = input("Descrição da tarefa (opcional): ")
    if not titulo:
        print("O título é obrigatório.")
        return
    
    payload = {'titulo': titulo, 'descricao': descricao}
    try:
        response = requests.post(f"{BASE_URL}/tasks", json=payload)
        if response.status_code == 201:
            print("Tarefa adicionada com sucesso!")
            print_task(response.json())
        else:
            print(f"Erro ao adicionar tarefa: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Erro de conexão: Não foi possível conectar ao servidor.")

def view_task():
    try:
        task_id = int(input("Digite o ID da tarefa: "))
    except ValueError:
        print("ID inválido. Por favor, digite um número.")
        return

    try:
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        if response.status_code == 200:
            print_task(response.json())
        elif response.status_code == 404:
            print(f"Tarefa com ID {task_id} não encontrada.")
        else:
            print(f"Erro ao visualizar tarefa: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Erro de conexão: Não foi possível conectar ao servidor.")

def update_task():
    try:
        task_id = int(input("Digite o ID da tarefa a ser atualizada: "))
    except ValueError:
        print("ID inválido. Por favor, digite um número.")
        return

    print("Digite os novos dados (deixe em branco para não alterar):")
    titulo = input("Novo título: ")
    descricao = input("Nova descrição: ")
    status = input("Novo status (ex: pendente, completo): ")

    payload = {}
    if titulo:
        payload['titulo'] = titulo
    if descricao:
        payload['descricao'] = descricao
    if status:
        payload['status'] = status

    if not payload:
        print("Nenhum dado fornecido para atualização.")
        return

    try:
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
        if response.status_code == 200:
            print("Tarefa atualizada com sucesso!")
            print_task(response.json())
        elif response.status_code == 404:
            print(f"Tarefa com ID {task_id} não encontrada.")
        else:
            print(f"Erro ao atualizar tarefa: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Erro de conexão: Não foi possível conectar ao servidor.")

def delete_task():
    try:
        task_id = int(input("Digite o ID da tarefa a ser deletada: "))
    except ValueError:
        print("ID inválido. Por favor, digite um número.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        if response.status_code == 204:
            print("Tarefa deletada com sucesso!")
        elif response.status_code == 404:
            print(f"Tarefa com ID {task_id} não encontrada.")
        else:
            print(f"Erro ao deletar tarefa: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Erro de conexão: Não foi possível conectar ao servidor.")

def print_menu():
    print("\n--- Sistema de Gestão de Tarefas ---")
    print("1. Listar todas as tarefas")
    print("2. Adicionar nova tarefa")
    print("3. Visualizar uma tarefa")
    print("4. Atualizar uma tarefa")
    print("5. Deletar uma tarefa")
    print("6. Sair")

def main():
    while True:
        print_menu()
        choice = input("Escolha uma opção: ")
        if choice == '1':
            list_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            view_task()
        elif choice == '4':
            update_task()
        elif choice == '5':
            delete_task()
        elif choice == '6':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()

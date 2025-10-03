Sistema de Gestão de Tarefas (To-Do List)Um sistema simples de gestão de tarefas (To-Do List) com uma arquitetura Cliente-Servidor, desenvolvido inteiramente em Python, sem o uso de frameworks externos.🏛️ ArquiteturaO projeto segue uma arquitetura Cliente-Servidor, onde as responsabilidades são claramente divididas:Servidor Backend (backend_server.py): O cérebro da aplicação. Gere toda a lógica de negócio, processa as requisições HTTP e é o único componente com acesso direto ao banco de dados.Cliente (cli_client.py): A interface do utilizador. Responsável por apresentar um menu, recolher os dados do utilizador e comunicar com o servidor através de uma API RESTful.Banco de Dados (tarefas.db): Uma base de dados SQLite para garantir a persistência dos dados das tarefas.+------------------+         HTTP/JSON         +---------------------+         SQL          +----------------+
|      Cliente     | <-----------------------> |   Servidor Backend  | <------------------> | Banco de Dados |
| (cli_client.py)  |                           | (backend_server.py) |                      |    (SQLite)    |
+------------------+                           +---------------------+                      +----------------+
✨ Funcionalidades[x] Criar uma nova tarefa[x] Listar todas as tarefas existentes[x] Visualizar os detalhes de uma tarefa específica por ID[x] Atualizar o título, descrição e estado de uma tarefa[x] Eliminar uma tarefa🚀 ComeçarSiga estas instruções para configurar e executar o projeto no seu ambiente local.Pré-requisitosCertifique-se de que tem o Python 3 e o SQLite 3 instalados no seu sistema.Python 3SQLite 3Instalação e ExecuçãoCrie e Ative um Ambiente VirtualNo diretório do projeto, crie um ambiente virtual para instalar as dependências de forma isolada.# Criar o ambiente
python -m venv venv
# Ativar no Windows
.\venv\Scripts\activate
# Ativar no Linux/macOS
source venv/bin/activate
Instale as DependênciasCom o ambiente virtual ativo, instale a única dependência externa, a biblioteca requests.pip install requests
Configure o Banco de DadosExecute o seguinte comando para criar o ficheiro tarefas.db e a tabela tasks a partir do script SQL.sqlite3 tarefas.db < database_setup.sql
Execute a AplicaçãoA aplicação requer dois terminais a correr em simultâneo.No Terminal 1 (Inicie o Servidor):python backend_server.py
Deverá ver a mensagem: Servidor rodando na porta 8000. Mantenha este terminal aberto.No Terminal 2 (Inicie o Cliente):python cli_client.py
O menu interativo da aplicação será exibido e poderá começar a utilizá-la.↔️ Rotas da APIA API do servidor expõe os seguintes endpoints:Verbo HTTPRotaDescriçãoPOST/tasksCria uma nova tarefa.GET/tasksRetorna uma lista de todas as tarefas.GET/tasks/<task_id>Retorna os detalhes de uma tarefa.PUT/tasks/<task_id>Atualiza uma tarefa existente.DELETE/tasks/<task_id>Elimina uma tarefa.

<div align="center">

# Sistema de Gestão de Tarefas  
Um sistema de **To-Do List** com arquitetura **Cliente-Servidor**, desenvolvido em **Python puro** para a disciplina de *Backend Frameworks*.

</div>

---

## 📖 Tabela de Conteúdos
- [Arquitetura](#️-arquitetura)
- [Funcionalidades](#-funcionalidades)
- [Como Executar](#-como-executar)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação Passo a Passo](#instalação-passo-a-passo)
  - [Executar a Aplicação](#executar-a-aplicação)
- [Documentação da API](#️-documentação-da-api)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)

---

## 🏛️ Arquitetura

O projeto foi construído sobre uma arquitetura **Cliente-Servidor**, garantindo a separação de responsabilidades.

- **Servidor Backend (`backend_server.py`)**:  
  Contém a lógica de negócio, processa requisições HTTP e é o único componente com acesso ao banco de dados.
- **Cliente (`cli_client.py`)**:  
  Interface em linha de comando. Comunica com o servidor através da API RESTful.
- **Banco de Dados (`tarefas.db`)**:  
  Base de dados **SQLite** para a persistência dos dados.

```text
┌─────────────────┐         HTTP/JSON         ┌─────────────────────┐         SQL          ┌────────────────┐
│     Cliente     │ ◀───────────────────────▶ │   Servidor Backend  │ ◀──────────────────▶ │ Banco de Dados │
│ (cli_client.py) │                           │ (backend_server.py) │                      │    (SQLite)    │
└─────────────────┘                           └─────────────────────┘                      └────────────────┘
````

---

## ✨ Funcionalidades

* [x] Criar uma nova tarefa.
* [x] Listar todas as tarefas existentes.
* [x] Visualizar os detalhes de uma tarefa específica por ID.
* [x] Atualizar o título, descrição e estado de uma tarefa.
* [x] Eliminar uma tarefa do sistema.

---

## 🚀 Como Executar

Siga estas instruções para configurar e executar o projeto no seu ambiente local.

### Pré-requisitos

* Python 3
* SQLite 3

### Instalação Passo a Passo

**1. Criar e Ativar um Ambiente Virtual**

```bash
# Criar o ambiente
python -m venv venv

# Ativar (Windows)
.\venv\Scripts\activate

# Ativar (Linux/macOS)
source venv/bin/activate
```

**2. Instalar Dependências**

```bash
pip install requests
```

**3. Configurar o Banco de Dados**

```bash
sqlite3 tarefas.db < database_setup.sql
```

### Executar a Aplicação

A aplicação requer **dois terminais** em execução simultânea:

**Terminal 1 - Servidor ⚙️**

```bash
python backend_server.py
```

Mantenha este terminal aberto para o servidor escutar as requisições.

**Terminal 2 - Cliente 🖥️**

```bash
python cli_client.py
```

Use este terminal para interagir com o sistema.

---

## ↔️ Documentação da API

O servidor expõe os seguintes endpoints:

| Verbo HTTP | Rota               | Descrição                         |
| ---------- | ------------------ | --------------------------------- |
| POST       | `/tasks`           | Cria uma nova tarefa              |
| GET        | `/tasks`           | Retorna todas as tarefas          |
| GET        | `/tasks/<task_id>` | Retorna os detalhes de uma tarefa |
| PUT        | `/tasks/<task_id>` | Atualiza uma tarefa existente     |
| DELETE     | `/tasks/<task_id>` | Elimina uma tarefa                |

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem**: Python 3
* **Servidor**: `http.server` (biblioteca padrão do Python)
* **Cliente**: `requests`
* **Banco de Dados**: SQLite 3

---

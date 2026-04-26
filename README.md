# ✅ Task Manager — API REST de Alta Performance

> Servidor HTTP REST + cliente CLI para gestão de tarefas, desenvolvido em **Python puro** — zero dependências externas no servidor.

---

## ⚡ Performance

| Métrica | Resultado |
|---|---|
| Tempo total de resposta (API) | **4,7 ms** |
| Tempo de consulta (SQL) | **~4 ms** |
| Tamanho do payload | **136 bytes** |
| Dependências externas do servidor | **0** |

---

## 🛠️ Stack

![Python](https://img.shields.io/badge/Python_Puro-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

**Servidor:** `http.server` · `sqlite3` · `json` · `time` — 100% biblioteca padrão Python

**Cliente:** `requests`

---

## 📋 Sobre o Projeto

Sistema Cliente-Servidor para gestão de tarefas com API RESTful e interface de linha de comando. O objetivo foi dominar o ciclo completo de uma requisição HTTP — parsing, roteamento, acesso ao banco, serialização e resposta — sem depender de nenhum framework.

O servidor instrumenta cada requisição com métricas separadas de tempo de banco e tempo total de API, permitindo identificar gargalos com precisão.

---

## 🏗️ Arquitetura

```
┌─────────────────┐     HTTP/JSON      ┌──────────────────────┐     SQL      ┌──────────────┐
│     Cliente     │ ◀────────────────▶ │   Servidor Backend   │ ◀──────────▶ │    SQLite    │
│ (cli_client.py) │                    │ (backend_server.py)  │              │  tarefas.db  │
└─────────────────┘                    └──────────────────────┘              └──────────────┘
```

**Servidor (`backend_server.py`)** — lógica de negócio, roteamento manual, acesso exclusivo ao banco. Cada request loga tempo de banco, tempo total e tamanho do payload separadamente.

**Cliente (`cli_client.py`)** — interface CLI com CRUD completo. Comunica com o servidor via HTTP/JSON.

**Banco (`tarefas.db`)** — SQLite com `row_factory = sqlite3.Row` para retorno de linhas como dicionários.

---

## 🔧 Decisões Técnicas

**Zero dependências no servidor**
Uso exclusivo da biblioteca padrão do Python (`http.server`, `sqlite3`). A decisão força o entendimento do ciclo completo de uma requisição HTTP sem abstração de framework.

**Instrumentação de performance separada**
O `log_performance()` mede o tempo de banco (`db_time`) separado do tempo total da API (`total_time`). Isso permite identificar se o gargalo está no SQL ou no overhead da aplicação — padrão de observabilidade de sistemas em produção.

**`sqlite3.Row` como row_factory**
Converte automaticamente rows do SQLite em objetos acessíveis por nome de coluna, eliminando mapeamento manual e permitindo serialização direta para dict/JSON.

---

## ↔️ Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/tasks` | Cria uma nova tarefa |
| `GET` | `/tasks` | Lista todas as tarefas |
| `GET` | `/tasks/<id>` | Retorna uma tarefa por ID |
| `PUT` | `/tasks/<id>` | Atualiza uma tarefa |
| `DELETE` | `/tasks/<id>` | Remove uma tarefa |

---

## ✨ Funcionalidades

- CRUD completo de tarefas via CLI
- Persistência em SQLite com timestamp automático de criação
- Status de tarefa: `pendente` / `completo`
- Log de performance por requisição no terminal do servidor

---

## 🚀 Como Executar

**1. Configurar o banco**
```bash
sqlite3 tarefas.db < database_setup.sql
```

**2. Terminal 1 — Servidor**
```bash
python backend_server.py
```

**3. Terminal 2 — Cliente**
```bash
pip install requests
python cli_client.py
```

---

## 📁 Estrutura

```
task_manager/
│
├── backend_server.py     # Servidor HTTP REST (Python puro)
├── cli_client.py         # Cliente CLI com CRUD completo
├── database_setup.sql    # Schema do banco SQLite
├── tarefas.db            # Banco de dados gerado
└── assets/
    └── demo.png
```

---

## 📄 Licença

Copyright © 2026 por Davi Ramos Ferreira. Todos os Direitos Reservados.

---

**Desenvolvido com 💙 por [Davi Ramos Ferreira](https://github.com/Daviramos7)**

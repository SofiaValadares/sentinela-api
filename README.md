# Sentinela API

A **Sentinela API** é uma aplicação desenvolvida com FastAPI que registra automaticamente o IP de qualquer usuário que acessa suas rotas. O projeto utiliza SQLite como banco de dados local, SQLAlchemy como ORM, e Middleware para interceptar requisições.

---

## 📦 Arquitetura do Projeto

```
sentinela-api/
├── .env                         # Variáveis de ambiente
├── pyproject.toml               # Configuração do projeto (Poetry, dependências)
├── sentinela/
│   ├── __init__.py              # Define a pasta como módulo Python
│   ├── main.py                  # Ponto de entrada da aplicação
│   ├── config.py                # Carrega configurações do .env
│   ├── database.py              # Engine, sessão e Base do SQLAlchemy
│   ├── models.py                # Modelo AccessLog (tabela de logs de IP)
│   ├── middleware.py            # Middleware que registra IPs
│   ├── routes/
│   │   └── logs.py              # Rota para consultar logs
│   └── schemas/
│       └── log_schema.py        # Schema Pydantic para retorno dos logs
```

---

## 🚀 Como Rodar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/SofiaValadares/sentinela-api.git
cd sentinela-api
```

### 2. Crie o arquivo `.env`

```env
DATABASE_URL=sqlite:///sentinela.db
```

### 3. Instale as dependências

Se estiver usando **Poetry**:

```bash
poetry install
poetry shell
```

Ou com **pip + venv**:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy python-dotenv
```

### 4. Execute a aplicação

```bash
uvicorn sentinela.main:app --reload
```

### 5. Teste no navegador

- `GET /ping` → Teste de conectividade: retorna `{ "ping": "pong" }`
- `GET /logs` → Lista os IPs registrados
- `GET /docs` → Documentação Swagger interativa

---
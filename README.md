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
│   ├── routes/                  # Rotas da aplicação
│   │   └── now.py               # Rota para risco de incêndio
│   │   └── logs.py              # Rota para consultar logs
│   ├── schemas/                 # Schemas Pydantic
│   │   └── log_schema.py        # Schema para retorno dos logs
│   ├── ia/                      # Inteligência Artificial e modelos
│   │   ├── __init__.py
│   │   ├── funcs.py             # Funções de predição e preprocessamento
│   │   ├── modelo_com_dias_sem_chuva.pkl      # Modelo ML com dias sem chuva
│   │   └── modelo_sem_dias_sem_chuva.pkl      # Modelo ML sem dias sem chuva
│   └── map/                     # Funções e dados de geolocalização
│       ├── __init__.py
│       ├── map_funcs.py         # Funções para encontrar estado por coordenada
│       └── map.geojson          # Arquivo GeoJSON dos estados
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

---

## 🌐 Rotas Principais da API

| Método | Rota    | Descrição                                                                 |
|--------|---------|---------------------------------------------------------------------------|
| GET    | /ping   | Teste de conectividade. Retorna `{ "ping": "pong" }`                      |
| GET    | /now    | Retorna o risco de incêndio para uma coordenada e data atual              |

---

### Exemplos de uso

#### `GET /now`

Retorna o risco de incêndio para as coordenadas e data atual.

**Parâmetros:**
- `latitude` (float): Latitude do local (obrigatório)
- `longitude` (float): Longitude do local (obrigatório)
- `numero_dias_sem_chuva` (int): Número de dias sem chuva (opcional)

**Exemplo de requisição:**
```bash
curl "http://localhost:8000/now?latitude=-8.05&longitude=-34.9&numero_dias_sem_chuva=5"
```

**Resposta esperada:**
```json
{
  "risco": 1,
  "estado": "PERNAMBUCO"
}
```
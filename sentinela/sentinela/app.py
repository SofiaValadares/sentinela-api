from fastapi import FastAPI
from sentinela.sentinela.routes import connection_test

app = FastAPI()

# Include routes2
app.include_router(connection_test.router)

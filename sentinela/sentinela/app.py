from fastapi import FastAPI
from routes import connection_test

app = FastAPI()

# Include routes
app.include_router(connection_test.router)

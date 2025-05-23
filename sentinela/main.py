from fastapi import FastAPI
from sentinela.database import Base, engine
from sentinela.middleware import LogIPMiddleware
from sentinela.routes import logs, history, now, alert_me, weather

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.add_middleware(LogIPMiddleware)

@app.get("/")
async def root():
    return {"message": "Sentinela API ativa"}

@app.get("/ping")
async def ping():
    return {"ping": "pong"}

app.include_router(logs.router)
app.include_router(history.router)
app.include_router(now.router)
app.include_router(alert_me.router)
app.include_router(weather.router)
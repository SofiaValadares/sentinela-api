from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sentinela.database import SessionLocal
from sentinela.models import AccessLog

class LogIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.headers.get("X-Forwarded-For") or request.client.host
        db = SessionLocal()
        try:
            log = AccessLog(ip_address=ip)
            db.add(log)
            db.commit()
        finally:
            db.close()
        return await call_next(request)
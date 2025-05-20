from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sentinela.database import SessionLocal
from sentinela.models import AccessLog
from sentinela.schemas.log_schema import AccessLogResponse

router = APIRouter(prefix="/logs", tags=["Logs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[AccessLogResponse])
def list_logs(db: Session = Depends(get_db)):
    logs = db.query(AccessLog).order_by(AccessLog.accessed_at.desc()).all()
    return logs
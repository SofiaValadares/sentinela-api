from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sentinela.database import Base

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    accessed_at = Column(DateTime, default=datetime.utcnow)

from pydantic import BaseModel
from datetime import datetime

class AccessLogResponse(BaseModel):
    ip_address: str
    accessed_at: datetime

    class Config:
        orm_mode = True

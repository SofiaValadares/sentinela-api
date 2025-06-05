from pydantic import BaseModel
from datetime import datetime
from fastapi import Query

class NowInput(BaseModel):
    data_pas: datetime
    numero_dias_sem_chuva: int
    latitude: float
    longitude: float

    @classmethod
    def as_query(
        cls,
        data_pas: datetime = Query(...),
        numero_dias_sem_chuva: int = Query(...),
        latitude: float = Query(...),
        longitude: float = Query(...)
    ) -> "NowInput":
        return cls(
            data_pas=data_pas,
            numero_dias_sem_chuva=numero_dias_sem_chuva,
            latitude=latitude,
            longitude=longitude
        )

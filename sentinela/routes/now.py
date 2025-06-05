from fastapi import APIRouter, HTTPException
from datetime import datetime
import pandas as pd

from sentinela.map.map_funcs import find_state
from sentinela.ia.funcs import predizer_com_dias_sem_chuva

router = APIRouter(prefix="/now", tags=["Now"])

@router.get("/")
async def get_now(
    numero_dias_sem_chuva: int,
    latitude: float,
    longitude: float
):
    data_pas = datetime.now().isoformat(timespec="seconds")

    state = find_state(latitude, longitude)
    if state == "DESCONHECIDO":
        raise HTTPException(status_code=400, detail="Coordenadas fora da área de cobertura")


    dados = pd.DataFrame([{
        "data_pas": data_pas,
        "numero_dias_sem_chuva": numero_dias_sem_chuva,
        "latitude": latitude,
        "longitude": longitude,
        "estado": state
    }])

    # CONVERSÃO IMPORTANTE
    dados["data_pas"] = pd.to_datetime(dados["data_pas"])

    try:
        resultado = predizer_com_dias_sem_chuva(dados)
        return {"risco": int(resultado[0]), "estado": state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

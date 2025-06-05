from fastapi import APIRouter, HTTPException
from datetime import datetime
import pandas as pd

from sentinela.map.map_funcs import find_state
from sentinela.ia.funcs import (
    predizer_com_dias_sem_chuva,
    predizer_sem_dias_sem_chuva
)

router = APIRouter(prefix="/now", tags=["Now"])

@router.get("/")
async def get_now(
    latitude: float,
    longitude: float,
    numero_dias_sem_chuva: int = None,
):
    # Data atual no formato correto
    data_pas = datetime.now().isoformat(timespec="seconds")

    # Verifica o estado com base nas coordenadas
    state = find_state(latitude, longitude)
    if state == "DESCONHECIDO":
        raise HTTPException(status_code=400, detail="Coordenadas fora da área de cobertura")

    # Monta o DataFrame com os dados
    dados = pd.DataFrame([{
        "data_pas": data_pas,
        "latitude": latitude,
        "longitude": longitude,
        "estado": state,
        **({"numero_dias_sem_chuva": numero_dias_sem_chuva} if numero_dias_sem_chuva is not None else {})
    }])

    # Converte a coluna data_pas para datetime real
    dados["data_pas"] = pd.to_datetime(dados["data_pas"])

    # Seleciona o modelo adequado com base no parâmetro
    try:
        if numero_dias_sem_chuva is not None:
            resultado = predizer_com_dias_sem_chuva(dados)
        else:
            resultado = predizer_sem_dias_sem_chuva(dados)

        return {
            "risco": int(resultado[0]),
            "estado": state

        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

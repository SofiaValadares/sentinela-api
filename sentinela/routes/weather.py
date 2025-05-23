from fastapi import APIRouter, Query
from sentinela.weather_service import get_weather_data

router = APIRouter()

@router.get("/weather")
async def weather(lat: float = Query(...), lon: float = Query(...)):
    """
    Retorna dados climáticos da Open Meteo.
    """
    return await get_weather_data(lat, lon)

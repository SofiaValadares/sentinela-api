import httpx

async def get_weather_data(lat: float, lon: float):
    """
    Consulta a Open Meteo e retorna os dados climáticos atuais.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/alert-me", tags=["Alert Me"])

@router.get("/")
async def get_alert():
    return {"status": "TO-DO", "mensagem": "Esta funcionalidade será implementada futuramente."}
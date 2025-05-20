from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/now", tags=["Now"])

@router.get("/")
async def get_now():
    return {"status": "TO-DO", "mensagem": "Esta funcionalidade será implementada futuramente."}
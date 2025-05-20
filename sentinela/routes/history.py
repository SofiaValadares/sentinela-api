from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/history", tags=["History"])

@router.get("/")
async def get_history():
    return {"status": "TO-DO", "mensagem": "Esta funcionalidade será implementada futuramente."}
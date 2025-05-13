from fastapi import APIRouter

router = APIRouter()

@router.get("/connection-test")
def test_connection():
    return {"status": "connected successfully!"}

from fastapi import APIRouter, Body, HTTPException, Depends

router = APIRouter()

@router.get("/test/{id}")
async def test(id):
    print(id)
    return {"message": "Success!"}

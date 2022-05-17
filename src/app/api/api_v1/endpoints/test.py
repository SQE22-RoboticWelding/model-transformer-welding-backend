from fastapi import APIRouter, Body, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps

router = APIRouter()

@router.get("/test/{id}")
async def test(id):
    print(id)
    return {"message": "Success!"}


@router.get("/database")
async def database(
        db: AsyncSession = Depends(deps.get_async_db)
):
    if db is not None:
        print("We have a database :)")
        return {"message": "Success"}
    else:
        print("We don't have a database :(")
        return {"message": "Failure"}
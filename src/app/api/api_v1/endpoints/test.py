from fastapi import APIRouter, Body, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps


router = APIRouter()


@router.get("/test/{id}")
async def test(id):
    return {"message": f"{id} was sent"}


@router.get("/database")
async def database(
        db: AsyncSession = Depends(deps.get_async_db)
):
    if db:
        return {"message": "Database reachable"}
    else:
        return {"message": "Database not reachable"}

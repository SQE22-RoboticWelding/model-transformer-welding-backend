from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.robot_type import RobotTypeCreate
router = APIRouter()


@router.post("/", response_description="Add new robot type")
async def create_robot_type(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        robot_type_in: RobotTypeCreate):
    print(robot_type_in.name, robot_type_in.vendor)
    return { "Status": "Success" }
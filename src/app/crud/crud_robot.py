from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, Dict, Optional, Union, List

from app.crud.base import CRUDBase
from app.models.robot import Robot
from app.schemas.robot import RobotCreate, RobotUpdate


class CRUDRobot(CRUDBase[Robot, RobotCreate, RobotUpdate]):
    async def create(
            self, db: AsyncSession, *, obj_in: RobotCreate
    ) -> Robot:
        db_obj = Robot(
            project_id=obj_in.project_id,
            robot_type_id=obj_in.robot_type_id,
            description=obj_in.description,
            name=obj_in.name,
            position_x=obj_in.position_x,
            position_y=obj_in.position_y,
            position_z=obj_in.position_z,
            position_norm_vector_x=obj_in.position_norm_vector_x,
            position_norm_vector_y=obj_in.position_norm_vector_y,
            position_norm_vector_z=obj_in.position_norm_vector_z,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self, db: AsyncSession, *, db_obj: Robot, obj_in: Union[RobotUpdate, Dict[str, Any]]
    ) -> Robot:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def get_by_id( # noqa
            self, db: AsyncSession, *, id: int
    ) -> Optional[Robot]:
        result = await db.execute(select(Robot).filter(Robot.id == id))
        return result.scalars().first()

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Robot]:
        result = await db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


robot = CRUDRobot(Robot)

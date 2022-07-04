from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, Dict, Optional, Union, List

from app.crud.base import CRUDBase
from app.models.robot_type import RobotType
from app.schemas.robot_type import RobotTypeCreate, RobotTypeUpdate


class CRUDRobotType(CRUDBase[RobotType, RobotTypeCreate, RobotTypeUpdate]):
    async def create(
            self, db: AsyncSession, *, obj_in: RobotTypeCreate
    ) -> RobotType:
        db_obj = RobotType(**obj_in.dict(exclude_unset=True, exclude={"id"}))
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def update(
            self, db: AsyncSession, *, db_obj: RobotType, obj_in: Union[RobotTypeUpdate, Dict[str, Any]]
    ) -> RobotType:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def get_by_id( # noqa
            self, db: AsyncSession, *, id: int
    ) -> Optional[RobotType]:
        result = await db.execute(select(RobotType).filter(RobotType.id == id))
        return result.scalars().first()

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[RobotType]:
        result = await db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


robot_type = CRUDRobotType(RobotType)

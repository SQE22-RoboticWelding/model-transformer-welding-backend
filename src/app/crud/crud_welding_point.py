from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, Dict, Optional, Union, List

from app.crud.base import CRUDBase
from app.models.welding_point import WeldingPoint
from app.schemas.welding_point import WeldingPointCreate, WeldingPointUpdate


class CRUDWeldingPoint(CRUDBase[WeldingPoint, WeldingPointCreate, WeldingPointUpdate]):
    async def create(
            self, db: AsyncSession, *, obj_in: WeldingPointCreate
    ) -> WeldingPoint:
        db_obj = WeldingPoint(
            description=obj_in.description,
            project_id=obj_in.project_id,
            robot_id=obj_in.robot_id,
            welding_order=obj_in.welding_order,
            name=obj_in.name,
            x=obj_in.x,
            y=obj_in.y,
            z=obj_in.z,
            pitch=obj_in.pitch,
            roll=obj_in.roll,
            yaw=obj_in.yaw,
            tolerance=obj_in.tolerance
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_multi(
            self, db: AsyncSession, *, obj_in: List[WeldingPointCreate]
    ) -> List[WeldingPoint]:
        return await super().create_multi(db=db, obj_in=obj_in)

    async def update(
            self, db: AsyncSession, *, db_obj: WeldingPoint, obj_in: Union[WeldingPointUpdate, Dict[str, Any]]
    ) -> WeldingPoint:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def get_by_id( # noqa
            self, db: AsyncSession, *, id: int
    ) -> Optional[WeldingPoint]:
        result = await db.execute(select(WeldingPoint).filter(WeldingPoint.id == id))
        return result.scalars().first()

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[WeldingPoint]:
        result = await db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


welding_point = CRUDWeldingPoint(WeldingPoint)

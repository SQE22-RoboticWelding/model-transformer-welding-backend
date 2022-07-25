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
        db_obj = WeldingPoint(**obj_in.dict(exclude_unset=True, exclude={"id"}))
        db.add(db_obj)
        await db.flush()
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

    async def get_multi_by_project_id(
            self, db: AsyncSession, project_id: int) -> List[WeldingPoint]:
        result = await db.execute(
            select(self.model).filter(self.model.project_id == project_id))
        return result.scalars().all()


welding_point = CRUDWeldingPoint(WeldingPoint)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, Dict, Optional, Union, List

from app.crud.base import CRUDBase
from app.models.workpiece import Workpiece
from app.schemas.workpiece import WorkpieceCreate, WorkpieceUpdate


class CRUDWorkpiece(CRUDBase[Workpiece, WorkpieceCreate, WorkpieceUpdate]):
    async def create(
            self, db: AsyncSession, *, obj_in: WorkpieceCreate
    ) -> Workpiece:
        db_obj = Workpiece(**obj_in.dict(exclude_unset=True, exclude={"id"}))
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def update(
            self, db: AsyncSession, *, db_obj: Workpiece, obj_in: Union[WorkpieceUpdate, Dict[str, Any]]
    ) -> Workpiece:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def get_by_id( # noqa
            self, db: AsyncSession, *, id: int
    ) -> Optional[Workpiece]:
        result = await db.execute(select(Workpiece).filter(Workpiece.id == id))
        return result.scalars().first()

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Workpiece]:
        result = await db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


workpiece = CRUDWorkpiece(Workpiece)

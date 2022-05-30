from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, Dict, Optional, Union, List

from app.crud.base import CRUDBase
from app.models.welding_configuration import WeldingConfiguration
from app.schemas.welding_configuration import WeldingConfigurationCreate, WeldingConfigurationUpdate


class CRUDWeldingConfiguration(CRUDBase[WeldingConfiguration, WeldingConfigurationCreate, WeldingConfigurationUpdate]):
    async def create(
            self, db: AsyncSession, *, obj_in: WeldingConfigurationCreate
    ) -> WeldingConfiguration:
        db_obj = WeldingConfiguration(
            name=obj_in.name,
            description=obj_in.description
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self, db: AsyncSession, *, db_obj: WeldingConfiguration, obj_in: Union[WeldingConfigurationUpdate, Dict[str, Any]]
    ) -> WeldingConfiguration:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def get_by_id( # noqa
            self, db: AsyncSession, *, id: int
    ) -> Optional[WeldingConfiguration]:
        result = await db.execute(select(WeldingConfiguration).filter(WeldingConfiguration.id == id))
        return result.scalars().first()

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[WeldingConfiguration]:
        result = await db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


welding_configuration = CRUDWeldingConfiguration(WeldingConfiguration)

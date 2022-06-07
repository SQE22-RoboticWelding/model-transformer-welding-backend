from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, Dict, Optional, Union, List

from app.crud.base import CRUDBase
from app.models.generation_template import GenerationTemplate as GenerationTemplateDB
from app.schemas.generation_template import GenerationTemplateCreate, GenerationTemplateUpdate


class CRUDGenerationTemplate(CRUDBase[GenerationTemplateDB, GenerationTemplateCreate, GenerationTemplateUpdate]):
    async def create(
            self, db: AsyncSession, *, obj_in: GenerationTemplateCreate
    ) -> GenerationTemplateDB:
        db_obj = GenerationTemplateDB(
            name=obj_in.name,
            description=obj_in.description,
            content=obj_in.content
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self, db: AsyncSession, *, db_obj: GenerationTemplateDB,
            obj_in: Union[GenerationTemplateUpdate, Dict[str, Any]]
    ) -> GenerationTemplateDB:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def get_by_id( # noqa
            self, db: AsyncSession, *, id: int
    ) -> Optional[GenerationTemplateDB]:
        result = await db.execute(select(GenerationTemplateDB).filter(GenerationTemplateDB.id == id))
        return result.scalars().first()

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[GenerationTemplateDB]:
        result = await db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


generation_template = CRUDGenerationTemplate(GenerationTemplateDB)

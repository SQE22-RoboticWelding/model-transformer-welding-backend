from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, Dict, Optional, Union, List

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    async def create(
            self, db: AsyncSession, *, obj_in: ProjectCreate
    ) -> Project:
        db_obj = Project(
            name=obj_in.name,
            description=obj_in.description
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self, db: AsyncSession, *, db_obj: Project, obj_in: Union[ProjectUpdate,
                                                                      Dict[str, Any]]
    ) -> Project:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def get_by_id( # noqa
            self, db: AsyncSession, *, id: int
    ) -> Optional[Project]:
        result = await db.execute(select(Project).filter(Project.id == id))
        return result.scalars().first()

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        result = await db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


project = CRUDProject(Project)

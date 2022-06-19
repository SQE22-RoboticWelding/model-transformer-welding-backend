import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.generation_template import GenerationTemplate
from app.crud.crud_generation_template import generation_template
from app.schemas.generation_template import GenerationTemplateUpdate
from app.tests.utils.models import create_generation_template

pytestmark = pytest.mark.asyncio


async def test_crud_generation_template_create(database: AsyncSession):
    generation_template_obj = await create_generation_template(db=database)
    assert generation_template_obj is not None
    assert isinstance(generation_template_obj, GenerationTemplate)


async def test_crud_generation_template_get(database: AsyncSession):
    generation_template_obj = await create_generation_template(db=database)
    tmp = await generation_template.get_by_id(db=database, id=generation_template_obj.id)
    assert generation_template_obj.__eq__(tmp)


async def test_crud_generation_template_get_multi(database: AsyncSession):
    await create_generation_template(db=database)
    await create_generation_template(db=database)
    generation_templates = await generation_template.get_multi(db=database)
    assert len(generation_templates) == 2


async def test_crud_generation_template_update(database: AsyncSession):
    generation_template_obj = await create_generation_template(db=database)
    await generation_template.update(db=database, db_obj=generation_template_obj, obj_in={"name": "modified"})
    assert generation_template_obj.name == "modified"

    await generation_template.update(db=database, db_obj=generation_template_obj,
                                     obj_in=GenerationTemplateUpdate(name="modified again"))
    assert generation_template_obj.name == "modified again"

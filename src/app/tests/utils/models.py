from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_generation_template import generation_template
from app.crud.crud_robot import robot
from app.crud.crud_robot_type import robot_type
from app.crud.crud_project import project
from app.crud.crud_welding_point import welding_point
from app.models.project import Project
from app.models.welding_point import WeldingPoint
from app.models.generation_template import GenerationTemplate
from app.models.robot import Robot
from app.models.robot_type import RobotType
from app.schemas.generation_template import GenerationTemplateCreate
from app.schemas.project import ProjectCreate
from app.schemas.robot import RobotCreate
from app.schemas.robot_type import RobotTypeCreate
from app.schemas.welding_point import WeldingPointCreate
from app.tests.utils.utils import random_string, random_float, get_example_template


async def create_project(db: AsyncSession) -> Project:
    project_in = ProjectCreate(
        name=random_string(),
        description=random_string())
    return await project.create(db=db, obj_in=project_in)


async def create_robot_type(db: AsyncSession) -> RobotType:
    robot_type_in = RobotTypeCreate(
        name=random_string(),
        vendor=random_string(),
        capacity_load_kg=random_float(),
        range_m=random_float())
    return await robot_type.create(db=db, obj_in=robot_type_in)


async def create_robot(db: AsyncSession, robot_type_obj: RobotType) -> Robot:
    robot_in = RobotCreate(
        robot_type_id=robot_type_obj.id,
        description=random_string())
    return await robot.create(db=db, obj_in=robot_in)


async def create_welding_point(db: AsyncSession,
                               project_obj: Project,
                               welding_order_in: int = 0) -> WeldingPoint:
    welding_point_in = WeldingPointCreate(
        project_id=project_obj.id,
        welding_order=welding_order_in,
        name=random_string(),
        description=random_string(),
        x=random_float(),
        y=random_float(),
        z=random_float(),
        roll=random_float(),
        pitch=random_float(),
        yaw=random_float(),
        tolerance=random_float(negative=False)
    )
    return await welding_point.create(db=db, obj_in=welding_point_in)


async def create_generation_template(db: AsyncSession) -> GenerationTemplate:
    generation_template_in = GenerationTemplateCreate(
        name=random_string(),
        description=random_string(),
        content=get_example_template()
    )
    return await generation_template.create(db=db, obj_in=generation_template_in)

from typing import Optional

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


async def create_project(db: AsyncSession, commit_and_refresh: bool = False) -> Project:
    project_in = ProjectCreate(
        name=random_string(),
        description=random_string())

    project_obj = await project.create(db=db, obj_in=project_in)
    assert project_obj.name == project_in.name
    assert project_obj.description == project_in.description

    # Useful when the date fields in the object are needed as they get only filled when the database executes
    # the transaction
    if commit_and_refresh:
        await db.commit()
        await db.refresh(project_obj)
    return project_obj


async def create_robot_type(db: AsyncSession, template_id: Optional[int] = None,
                            commit_and_refresh: bool = False) -> RobotType:
    robot_type_in = RobotTypeCreate(
        name=random_string(),
        vendor=random_string(),
        capacity_load_kg=random_float(),
        range_m=random_float(),
        generation_template_id=template_id)

    robot_type_obj = await robot_type.create(db=db, obj_in=robot_type_in)
    assert robot_type_obj.name == robot_type_in.name
    assert robot_type_obj.vendor == robot_type_in.vendor
    assert robot_type_obj.capacity_load_kg == robot_type_in.capacity_load_kg
    assert robot_type_obj.range_m == robot_type_in.range_m
    if template_id is not None:
        assert robot_type_obj.generation_template_id == template_id

    if commit_and_refresh:
        await db.commit()
        await db.refresh(robot_type_obj)
    return robot_type_obj


async def create_robot(db: AsyncSession, robot_type_obj: RobotType, project_obj: Project,
                       commit_and_refresh: bool = False) -> Robot:
    robot_in = RobotCreate(
        robot_type_id=robot_type_obj.id,
        project_id=project_obj.id,
        name=random_string(),
        description=random_string(),
        position_x=random_float(),
        position_y=random_float(),
        position_z=random_float(),
        position_norm_vector_x=random_float(),
        position_norm_vector_y=random_float(),
        position_norm_vector_z=random_float()
    )

    robot_obj = await robot.create(db=db, obj_in=robot_in)
    assert robot_obj.robot_type_id == robot_in.robot_type_id
    assert robot_obj.name == robot_in.name
    assert robot_obj.description == robot_in.description
    assert robot_obj.position_x == robot_in.position_x
    assert robot_obj.position_y == robot_in.position_y
    assert robot_obj.position_z == robot_in.position_z
    assert robot_obj.position_norm_vector_x == robot_in.position_norm_vector_x
    assert robot_obj.position_norm_vector_y == robot_in.position_norm_vector_y
    assert robot_obj.position_norm_vector_z == robot_in.position_norm_vector_z

    if commit_and_refresh:
        await db.commit()
        await db.refresh(robot_obj)
    return robot_obj


async def create_welding_point(db: AsyncSession, project_obj: Project, welding_order_in: int = 0,
                               commit_and_refresh: bool = False) -> WeldingPoint:
    welding_point_in = get_welding_point_create(project_obj=project_obj, welding_order_in=welding_order_in)

    welding_point_obj = await welding_point.create(db=db, obj_in=welding_point_in)
    assert welding_point_obj.project_id == welding_point_in.project_id
    assert welding_point_obj.welding_order == welding_point_in.welding_order
    assert welding_point_obj.name == welding_point_in.name
    assert welding_point_obj.description == welding_point_in.description
    assert welding_point_obj.x_original == welding_point_in.x_original
    assert welding_point_obj.y_original == welding_point_in.y_original
    assert welding_point_obj.z_original == welding_point_in.z_original
    assert welding_point_obj.x == welding_point_in.x
    assert welding_point_obj.y == welding_point_in.y
    assert welding_point_obj.z == welding_point_in.z
    assert welding_point_obj.roll == welding_point_in.roll
    assert welding_point_obj.pitch == welding_point_in.pitch
    assert welding_point_obj.yaw == welding_point_in.yaw

    if commit_and_refresh:
        await db.commit()
        await db.refresh(welding_point_obj)
    return welding_point_obj


async def create_generation_template(db: AsyncSession, commit_and_refresh: bool = False) -> GenerationTemplate:
    generation_template_in = GenerationTemplateCreate(
        name=random_string(),
        description=random_string(),
        content=get_example_template(),
        language="HolyC",
        file_extension=".HC",
        version=1.00
    )

    generation_template_obj = await generation_template.create(db=db, obj_in=generation_template_in)
    assert generation_template_obj.name == generation_template_in.name
    assert generation_template_obj.description == generation_template_in.description
    assert generation_template_obj.content == generation_template_in.content
    assert generation_template_obj.language == generation_template_in.language
    assert generation_template_obj.file_extension == generation_template_in.file_extension

    # Useful when the date fields in the object are needed as they get only filled when the database executes
    # the transaction
    if commit_and_refresh:
        await db.commit()
        await db.refresh(generation_template_obj)
    return generation_template_obj


def get_welding_point_create(project_obj: Project, welding_order_in: int = 0) -> WeldingPointCreate:
    x_original = random_float()
    y_original = random_float()
    z_original = random_float()

    return WeldingPointCreate(
        project_id=project_obj.id,
        welding_order=welding_order_in,
        name=random_string(),
        description=random_string(),
        x_original=x_original,
        y_original=y_original,
        z_original=z_original,
        x=x_original,
        y=y_original,
        z=z_original,
        roll=random_float(),
        pitch=random_float(),
        yaw=random_float(),
        tolerance=random_float(negative=False)
    )


def get_welding_point_json_data():
    return {
        "project_id": 1,
        "welding_order": 1,
        "name": "P7",
        "description": "Welding point next to the reactor entrance",
        "x_original": -3.14,
        "y_original": 5.12,
        "z_original": -2.4,
        "x": 3.14,
        "y": -5.12,
        "z": 2.4,
        "roll": -1.7,
        "pitch": -2.0,
        "yaw": 4.512
    }

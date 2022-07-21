from app.codegen.code_generator import CodeGenerator
from app.models.generation_template import GenerationTemplate
from app.models.welding_point import WeldingPoint
from app.models.robot import Robot
from app.tests.utils.utils import get_example_template


def test_code_generation():
    robot_obj = Robot(id=1,
                      name="Test Robot",
                      position_x=1,
                      position_y=1,
                      position_z=1)

    welding_point_obj = WeldingPoint(project_id=1,
                                     welding_order=0,
                                     robot_id=robot_obj.id,
                                     robot=robot_obj,
                                     x=10,
                                     y=5.5,
                                     z=0.25,
                                     roll=0.35,
                                     pitch=3,
                                     yaw=0)
    generation_template_obj = GenerationTemplate(id=1, name="My Template", content=get_example_template())

    generated = CodeGenerator.generate(template=generation_template_obj, welding_points=[welding_point_obj])
    assert generated == "10, 5.5, 0.25 / 0.35, 3, 0 / 0"

from app.codegen.code_generator import CodeGenerator
from app.models.generation_template import GenerationTemplate
from app.models.welding_point import WeldingPoint
from app.tests.utils.utils import get_example_template


def test_code_generation():
    welding_point_obj = WeldingPoint(project_id=1,
                                     welding_order=0,
                                     x=10,
                                     y=5.5,
                                     z=0.25,
                                     roll=0.35,
                                     pitch=3,
                                     yaw=0)
    generation_template_obj = GenerationTemplate(id=1, name="My Template", content=get_example_template())

    generated = CodeGenerator.generate(template=generation_template_obj, welding_points=[welding_point_obj])
    assert generated == "10, 5.5, 0.25 / 0.35, 3, 0 / 0"

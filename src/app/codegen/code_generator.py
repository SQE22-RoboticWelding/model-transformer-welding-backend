"""code_generator.py handles codegen of models."""
from io import BytesIO

from jinja2 import Template
from zipfile import ZipFile

from app.models.project import Project
from app.schemas.generation_template import GenerationTemplate
from typing import List

from app.models.robot import Robot
from app.models.welding_point import WeldingPoint


class GeneratedCode:
    robot: Robot
    code: str

    def __init__(self, robot_obj, code):
        self.robot = robot_obj
        self.code = code


class CodeGenerator:
    @staticmethod
    def generate(template: GenerationTemplate, welding_points: List[WeldingPoint]) -> str:
        return Template(template.content, keep_trailing_newline=True).render({"welding_points": welding_points})

    @staticmethod
    def generate_code_by_robot(welding_points_by_robot: List[List[WeldingPoint]]) -> List[GeneratedCode]:
        result = []
        for wp_list in welding_points_by_robot:
            robot = wp_list[0].robot
            code = CodeGenerator.generate(robot.robot_type.generation_template, wp_list)
            result.append(GeneratedCode(robot, code))
        return result

    @staticmethod
    def zip_generated_code(generated_code: List[GeneratedCode]) -> BytesIO:
        in_memory_file = BytesIO()
        in_memory_zip = ZipFile(in_memory_file, "w")

        # Write generated code to file
        for generated in generated_code:
            filename = (f"{generated.robot.id}_{generated.robot.name}"
                        f".{generated.robot.robot_type.generation_template.file_extension}")
            in_memory_zip.writestr(filename, generated.code)
        in_memory_zip.close()

        # Reset stream position
        in_memory_file.seek(0)
        return in_memory_file

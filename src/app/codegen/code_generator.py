"""code_generator.py handles codegen of models."""
import random
import string
from io import BytesIO
from typing import List
from zipfile import ZipFile

import jinja2
from jinja2 import BaseLoader, Environment

from app.models.project import Project
from app.models.robot import Robot
from app.models.welding_point import WeldingPoint
from app.schemas.generation_template import GenerationTemplate


class GeneratedCode:
    robot: Robot
    code: str

    def __init__(self, robot_obj, code):
        self.robot = robot_obj
        self.code = code


class TemplateFunctions:
    """
    Helper class with methods available in jinja templates
    """
    @staticmethod
    def generate_blockly_block_id() -> str:
        """
        Generates a blockly block ID consisting of 20 chars, all letters and digits allowed
        :return: Blockly block ID
        """
        return "".join(random.choices(string.ascii_letters + string.digits, k=20))


class CodeGeneratorException(Exception):
    pass


class CodeGenerator:
    @staticmethod
    def generate(template: GenerationTemplate, welding_points: List[WeldingPoint]) -> str:
        """
        Generates code from a template and a list of welding points
        :param template: Template used for generation
        :param welding_points: Welding points to be used in the template
        :return: Generated code
        """

        # Define a dictionary with functions, which can be used in templates
        func_dict = {"generate_blockly_block_id": TemplateFunctions.generate_blockly_block_id}

        # Robot for which the program will be generated
        robots = set([wp.robot.id for wp in welding_points])
        if len(robots) != 1 or robots[0] is None:
            raise CodeGeneratorException("All welding points must have the same non-None robot")
        robot = welding_points[0].robot

        # Add welding points x, y, z relative to robot to be available as expression in templates
        wp_list = [wp.as_dict() for wp in welding_points]
        for wp in wp_list:
            wp["x_rel"] = wp["x"] - robot.position_x
            wp["y_rel"] = wp["y"] - robot.position_y
            wp["z_rel"] = wp["z"] - robot.position_z

        # Create new jinja environment and load template from string
        env = Environment(loader=BaseLoader(),
                          keep_trailing_newline=True,
                          autoescape=True,
                          undefined=jinja2.StrictUndefined)\
            .from_string(template.content)
        generated_code = env.render({"welding_points": wp_list} | {"robot": robot} | func_dict)

        return generated_code

    @staticmethod
    def generate_code_by_robot(welding_points_by_robot: List[List[WeldingPoint]]) -> List[GeneratedCode]:
        """
        Generates code for multiple robots
        :param welding_points_by_robot: List of multiple robots, containing a list of the welding points of the
        respective robot
        :return: Generated code for each robot
        """
        result = []
        for wp_list in welding_points_by_robot:
            robot = wp_list[0].robot
            code = CodeGenerator.generate(robot.robot_type.generation_template, wp_list)
            result.append(GeneratedCode(robot, code))
        return result

    @staticmethod
    def generate_code_for_project(project_obj: Project):
        # Get welding points seperated by robot, each list sorted by welding order ascending
        wp_by_robot = []
        robots = {wp.robot_id for wp in project_obj.welding_points}
        for robot_id in robots:
            wps = [wp for wp in project_obj.welding_points if wp.robot_id == robot_id]
            wps.sort(key=lambda x: x.welding_order)
            wp_by_robot.append(wps)

        # Generate code for each robot
        return CodeGenerator.generate_code_by_robot(wp_by_robot)

    @staticmethod
    def zip_generated_code(generated_code: List[GeneratedCode]) -> BytesIO:
        """
        Creates an in-memory zipfile, which includes the provided generated code, each code as its own file
        :param generated_code: List of generated code to be placed in the zipfile
        :return: In-memory zipfile
        """
        in_memory_file = BytesIO()
        in_memory_zip = ZipFile(in_memory_file, "w")

        # Write generated code to file
        for generated in generated_code:
            filename = (f"{generated.robot.name}"
                        f".{generated.robot.robot_type.generation_template.file_extension}")
            in_memory_zip.writestr(filename, generated.code)
        in_memory_zip.close()

        # Reset stream position
        in_memory_file.seek(0)
        return in_memory_file

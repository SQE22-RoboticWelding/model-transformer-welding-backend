from typing import List

from app.models.project import Project
from app.models.generation_template import GenerationTemplate
from app.schemas.generation_template import GenerationTemplateUpdate
from app.models.welding_point import WeldingPoint


def verify_welding_order_in_project(project_obj: Project) -> bool:
    """
    Verifies the welding order of a project to be unique and that every
    welding point has an order index
    :param project_obj: Project to verify
    :return: True, if welding order in project is correct, false otherwise
    """
    unique_order_indices = {wp.welding_order for wp in project_obj.welding_points}
    return len(unique_order_indices) == len(project_obj.welding_points)


def calculate_distance_from_origin(wp: WeldingPoint):
    x_dist_square = (wp.x - wp.x_original)**2
    y_dist_square = (wp.y - wp.y_original)**2
    z_dist_square = (wp.z - wp.z_original)**2
    return (x_dist_square + y_dist_square + z_dist_square)**0.5


# TODO: once we have normal vector this should check the tolerance on its orthogonal plane, not in a sphere
def verify_welding_coordinates_in_tolerance(welding_points: List[WeldingPoint]) -> bool:
    """
    Verifies that the welding point coordinates are within the tolerance
    """
    for wp in welding_points:
        if wp.tolerance is None:
            continue
        dist = calculate_distance_from_origin(wp)
        if dist > wp.tolerance:
            return False
    return True


def verify_welding_points_robot_assignment(project_obj: Project) -> bool:
    """
    Verifies, if all welding points have a robot assigned
    :param project_obj: Project to verify
    :return: True, if all welding points have a robot assigned, false otherwise
    """
    for wp in project_obj.welding_points:
        if wp.robot_id is None:
            return False
    return True


def verify_project_robot_type_template_assignment(project_obj: Project) -> bool:
    """
    Verifies that all robots used in the project have a robot type with a template assigned
    :param project_obj: Project to verify
    :return: True, if all used robot types have a template assigned, false otherwise
    """
    robot_types = {wp.robot.robot_type for wp in project_obj.welding_points}
    for robot_type in robot_types:
        if robot_type.generation_template_id is None:
            return False
    return True


def verify_template_version_increase_on_content_change(generation_template_obj: GenerationTemplate,
                                                       generation_template_in: GenerationTemplateUpdate) -> bool:
    """
    Verifies that on template update the content can only be changed when the version was increased as well
    :param generation_template_obj: Current template in the database
    :param generation_template_in:  Update object of the template to update
    :return: True, if template update ensures the constraint
    """
    if generation_template_in.content is None or generation_template_obj.content == generation_template_in.content:
        return True
    if generation_template_in.version is None or generation_template_in.version <= generation_template_obj.version:
        return False
    return True

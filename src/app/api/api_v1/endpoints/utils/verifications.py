from app.models.project import Project


def verify_welding_order_in_project(project_obj: Project) -> bool:
    """
    Verifies the welding order of a project to be unique and that every
    welding point has an order index
    :param project_obj: Project to verify
    :return: True, if welding order in project is correct, false otherwise
    """
    unique_order_indices = {wp.welding_order for wp in project_obj.welding_points}
    return len(unique_order_indices) == len(project_obj.welding_points)


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

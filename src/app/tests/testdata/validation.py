from typing import List

from app.schemas.welding_point import WeldingPointCreate


def validate_project_file_welding_points(welding_points: List[WeldingPointCreate]) -> None:
    assert welding_points[0].name == "P1"
    assert welding_points[1].name == "P2"

    assert welding_points[0].x == 0.297
    assert welding_points[1].x == 0

    assert welding_points[0].y == 0
    assert welding_points[1].y == 0.21

    assert welding_points[0].z == 0.1
    assert welding_points[1].z == 0.1

    assert welding_points[0].roll == 0
    assert welding_points[1].roll == 0

    assert welding_points[0].pitch == 0
    assert welding_points[1].pitch == 0

    assert welding_points[0].yaw == 0
    assert welding_points[1].yaw == 1.5708

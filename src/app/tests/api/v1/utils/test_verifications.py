from app.api.api_v1.endpoints.utils.verifications import verify_welding_coordinates_in_tolerance
from app.models.project import Project
from app.models.welding_point import WeldingPoint


def test_tolerance_distance_one_dimension_fail():
    wp = WeldingPoint(x_original=0,
                      y_original=0,
                      z_original=0,
                      x=0,
                      y=0,
                      z=10,
                      tolerance=9.9999)
    assert not verify_welding_coordinates_in_tolerance([wp])


def test_tolerance_distance_one_dimension_success():
    wp = WeldingPoint(x_original=0,
                      y_original=0,
                      z_original=0,
                      x=0,
                      y=0,
                      z=10,
                      tolerance=10.0001)
    assert verify_welding_coordinates_in_tolerance([wp])


def test_tolerance_distance_two_dimensions_fail():
    wp = WeldingPoint(x_original=0,
                      y_original=0,
                      z_original=0,
                      x=10,
                      y=0,
                      z=10,
                      tolerance=14.14213)
    assert not verify_welding_coordinates_in_tolerance([wp])


def test_tolerance_distance_two_dimensions_success():
    wp = WeldingPoint(x_original=0,
                      y_original=0,
                      z_original=0,
                      x=1,
                      y=0,
                      z=1,
                      tolerance=14.14214)
    assert verify_welding_coordinates_in_tolerance([wp])


def test_tolerance_distance_three_dimensions_fail():
    wp = WeldingPoint(x_original=0,
                      y_original=0,
                      z_original=0,
                      x=10,
                      y=10,
                      z=10,
                      tolerance=17.3205)
    assert not verify_welding_coordinates_in_tolerance([wp])


def test_tolerance_distance_three_dimensions_success():
    wp = WeldingPoint(x_original=0,
                      y_original=0,
                      z_original=0,
                      x=10,
                      y=10,
                      z=10,
                      tolerance=17.3206)
    assert verify_welding_coordinates_in_tolerance([wp])

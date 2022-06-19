from pathlib import Path
import pytest
from fastapi import UploadFile

from app.models.project import Project
from app.parser.pandas_parser import PandasParser
from testdata.getter import get_upload_file
from testdata.validation import validate_project_file_welding_points

pytestmark = pytest.mark.asyncio


def __get_project():
    return Project(
        id=1,
        name="Death Star Project",
        description="Plans for the death star"
    )


async def test_pandasparser_excel():
    file = get_upload_file("project_file.xlsx")

    parser = PandasParser(file)
    content = await file.read()

    result = parser.parse(content)
    assert result.error is False

    project_obj = __get_project()
    welding_points = parser.get_welding_points(project=project_obj)
    validate_project_file_welding_points(welding_points)

    await file.close()


async def test_pandasparser_excel_missing_column():
    file = get_upload_file("project_file_missing_column.xlsx")
    parser = PandasParser(file)
    content = await file.read()

    result = parser.parse(content)
    assert result.error is True

    await file.close()


async def test_pandasparser_excel_missing_data():
    file = get_upload_file("project_file_missing_data.xlsx")
    parser = PandasParser(file)
    content = await file.read()

    result = parser.parse(content)
    assert result.error is True

    await file.close()


async def test_pandasparser_excel_wrong_data_type():
    file = get_upload_file("project_file_wrong_data_type.xlsx")
    parser = PandasParser(file)
    content = await file.read()

    result = parser.parse(content)
    assert result.error is True

    await file.close()


async def test_pandasparser_csv():
    file = get_upload_file("project_file.csv")

    parser = PandasParser(file)
    content = await file.read()

    result = parser.parse(content)
    assert result.error is False

    project_obj = __get_project()
    welding_points = parser.get_welding_points(project=project_obj)
    validate_project_file_welding_points(welding_points)

    await file.close()


async def test_pandasparser_csv_missing_column():
    file = get_upload_file("project_file_missing_column.csv")
    parser = PandasParser(file)
    content = await file.read()

    result = parser.parse(content)
    assert result.error is True

    await file.close()


async def test_pandasparser_csv_missing_data():
    file = get_upload_file("project_file_missing_data.csv")
    parser = PandasParser(file)
    content = await file.read()

    result = parser.parse(content)
    assert result.error is True

    await file.close()


async def test_pandasparser_csv_wrong_data_type():
    file = get_upload_file("project_file_wrong_data_type.csv")
    parser = PandasParser(file)
    content = await file.read()

    result = parser.parse(content)
    assert result.error is True

    await file.close()


async def test_pandasparser_json():
    file = get_upload_file("project_file.json")

    parser = PandasParser(file)
    content = await file.read()

    result = parser.parse(content)
    assert result.error is False

    project_obj = __get_project()
    welding_points = parser.get_welding_points(project=project_obj)
    validate_project_file_welding_points(welding_points)

    await file.close()


async def test_pandasparser_json_missing_column():
    file = get_upload_file("project_file_missing_column.json")
    parser = PandasParser(file)
    content = await file.read()

    result = parser.parse(content)
    assert result.error is True

    await file.close()


async def test_pandasparser_json_missing_data():
    file = get_upload_file("project_file_missing_data.json")
    parser = PandasParser(file)
    content = await file.read()

    result = parser.parse(content)
    assert result.error is True

    await file.close()


async def test_pandasparser_json_wrong_data_type():
    file = get_upload_file("project_file_wrong_data_type.json")
    parser = PandasParser(file)
    content = await file.read()

    result = parser.parse(content)
    assert result.error is True

    await file.close()

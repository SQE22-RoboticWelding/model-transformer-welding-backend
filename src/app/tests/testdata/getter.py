from pathlib import Path
from fastapi import UploadFile, File

__path_to_testdata = Path(__file__).parent

content_types = {"excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                 "csv": "text/csv",
                 "json": "application/json"}


def get_upload_file(filename: str, content_type: str) -> UploadFile:
    file = open(f"{__path_to_testdata}/{filename}", mode="rb")
    return UploadFile(filename=file.name,
                      file=file,
                      content_type=content_type)


def get_file(filename: str) -> File:
    return open(f"{__path_to_testdata}/{filename}", mode="rb")

from pathlib import Path
from fastapi import UploadFile, File
import mimetypes

__path_to_testdata = Path(__file__).parent


def __get_file_path(filename):
    return f"{__path_to_testdata}/{filename}"


def get_upload_file(filename: str, content_type: str = None) -> UploadFile:
    if content_type is None:
        content_type = mimetypes.guess_type(__get_file_path(filename))[0]
    file = get_file(filename)

    return UploadFile(filename=file.name,
                      file=file,
                      content_type=content_type)


def get_file(filename: str) -> File:
    return open(__get_file_path(filename), mode="rb")

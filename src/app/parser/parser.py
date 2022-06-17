from abc import ABC, abstractmethod
from typing import List

from app.models.project import Project
from app.schemas.welding_point import WeldingPointCreate


class ParseResult:
    """
    Result of the parsing. Contains two fields, error and detail.
    """
    error: bool
    detail: str

    def __init__(self, error: bool, detail: str = ""):
        self.error = error
        self.detail = detail

    def __str__(self):
        return "Error={}, Detail={}".format(self.error, self.detail)


class ParserBase(ABC):
    @abstractmethod
    def validate(self) -> bool:
        """
        Validates the provided file to parse for supported format and content type
        :return: Success of validation
        """
        pass

    @abstractmethod
    def parse(self, file_content: bytes) -> ParseResult:
        """
        Parse the content of the file
        :param file_content: Content of file in bytes
        :return: Parsing result consisting of error status and detail in case of an occurred error
        """
        pass

    @abstractmethod
    def get_welding_points(self, project: Project) -> List[WeldingPointCreate]:
        """
        Returns a list of creatable welding points assigned to the provided project
        :param project: Existing project to which the welding points will be assigned
        :return: List of creatable welding point objects, which can then be created in the database
        """
        pass

import io
from typing import List, Iterable, Any
from fastapi import UploadFile
import pandas as pd

from app.models.project import Project
from app.parser.parser import ParserBase, ParseResult
from app.schemas.welding_point import WeldingPointCreate

SUPPORTED_CONTENT_TYPES = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", # noqa
                           "text/csv",
                           "application/json"]
SUPPORTED_FILE_TYPES = ["xlsx",
                        "csv",
                        "json"]


class PandasParser(ParserBase):
    """
    Parser based on pandas. Supported formats are Excel, CSV and JSON.
    """
    def __init__(self, file: UploadFile):
        self.filename: str = file.filename
        self.content_type: str = file.content_type
        self.file_type: str = self.filename.split('.')[-1]
        self.welding_points: Iterable[tuple[Any, ...]] = []

    def validate(self) -> bool:
        if (self.content_type in SUPPORTED_CONTENT_TYPES and
            self.file_type in SUPPORTED_FILE_TYPES):
            return True
        return False

    def parse(self, file_content: bytes) -> ParseResult:
        def parse_content():
            if self.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": # noqa
                return pd.read_excel(file_content)
            elif self.content_type == "text/csv":
                return pd.read_csv(io.BytesIO(file_content))
            elif self.content_type == "application/json":
                return pd.read_json(io.BytesIO(file_content))
            else:
                return None

        df = parse_content()
        if df is None:
            return ParseResult(error=True,
                               detail=f"No implementation for content type {self.content_type}")
        # Check, if expected columns are present
        if not {"ID", "x", "y", "z", "roll", "pitch", "yaw"}.issubset(df.columns):
            return ParseResult(error=True, detail="Data must contain ID, x, y, z, roll, pitch and yaw columns")
        # Check, if all rows in required columns contain data
        if df[["x", "y", "z", "roll", "pitch", "yaw"]].isnull().values.any():
            return ParseResult(error=True, detail="Not all required columns contain data")
        # Check, if expected numeric columns are numeric
        if not all(list(df[["x", "y", "z", "roll", "pitch", "yaw"]].dtypes.map(pd.api.types.is_numeric_dtype))):
            return ParseResult(error=True, detail="Columns contain data with unexpected data type")

        self.welding_points = df.itertuples(name="WeldingPoint", index=True)
        return ParseResult(error=False)

    def get_welding_points(self, project: Project) -> List[WeldingPointCreate]:
        result = []
        for row in self.welding_points:
            result.append(
                WeldingPointCreate(project_id=project.id,
                                   welding_order=getattr(row, "Index"),
                                   name=getattr(row, "ID"),
                                   x_original=getattr(row, "x"),  # we use the x, y, z values as original defaults
                                   y_original=getattr(row, "y"),
                                   z_original=getattr(row, "z"),
                                   x=getattr(row, "x"),
                                   y=getattr(row, "y"),
                                   z=getattr(row, "z"),
                                   roll=getattr(row, "roll"),
                                   pitch=getattr(row, "pitch"),
                                   yaw=getattr(row, "yaw")))
        return result

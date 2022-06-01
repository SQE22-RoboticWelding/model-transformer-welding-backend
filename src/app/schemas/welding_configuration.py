from typing import Optional
from pydantic import BaseModel
from pydantic.schema import datetime


class WeldingConfigurationBase(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Death Star",
                "description": "Welding configuration for the Death Star"
            }
        }


class WeldingConfigurationCreate(WeldingConfigurationBase):
    name: str


class WeldingConfigurationUpdate(WeldingConfigurationBase):
    name: Optional[str]


# Properties shared by models stored in DB
class WeldingConfigurationInDBBase(WeldingConfigurationBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True


class WeldingConfiguration(WeldingConfigurationInDBBase):
    pass


class WeldingConfigurationInDB(WeldingConfigurationInDBBase):
    pass

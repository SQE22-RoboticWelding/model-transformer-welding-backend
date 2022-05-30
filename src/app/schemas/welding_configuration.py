from typing import Optional
from pydantic import BaseModel
from pydantic.schema import datetime


class WeldingConfigurationBase(BaseModel):
    name: str
    description: Optional[str] = None


class WeldingConfigurationCreate(WeldingConfigurationBase):
    name: str
    description: str


class WeldingConfigurationUpdate(WeldingConfigurationBase):
    name: str
    description: str


# Properties shared by models stored in DB
class WeldingConfigurationInDBBase(WeldingConfigurationBase):
    id: int
    name: str
    description: str
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True


class WeldingConfiguration(WeldingConfigurationInDBBase):
    pass


class WeldingConfigurationInDB(WeldingConfigurationInDBBase):
    pass

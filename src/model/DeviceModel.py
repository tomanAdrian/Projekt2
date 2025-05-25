from pydantic import BaseModel


class ConfigurationModel(BaseModel):
    config: str


class VersionModel(BaseModel):
    version: str
    freeMemory: str
    totalMemory: str

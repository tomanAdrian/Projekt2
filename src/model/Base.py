from pydantic import BaseModel


class CiscoEnable(BaseModel):
    enablePassword: str

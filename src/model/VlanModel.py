from pydantic import BaseModel
from typing import Optional
from src.model.Base import CiscoEnable


class VlanModel(BaseModel):
    id: int
    name: str
    enabled: bool
    interfaces: list[str]

    class Config:
        schema_extra = {
            "example": [
                {
                    "id": 1,
                    "name": "default",
                    "enabled": True,
                    "interfaces": [
                        "Gi0/1",
                        "Gi0/2",
                        "Gi0/3",
                        "Gi1/0",
                        "Gi1/1",
                        "Gi1/2",
                        "Gi1/3",
                        "Gi2/0",
                        "Gi2/1",
                        "Gi2/2",
                        "Gi2/3",
                        "Gi3/0",
                        "Gi3/1",
                        "Gi3/2",
                        "Gi3/3"
                    ]
                },
                {
                    "id": 101,
                    "name": "VLAN0101",
                    "enabled": True,
                    "interfaces": [
                        "Gi0/0"
                    ]
                },
                {
                    "id": 1002,
                    "name": "fddi-default",
                    "enabled": False,
                    "interfaces": []
                },
                {
                    "id": 1003,
                    "name": "token-ring-default",
                    "enabled": False,
                    "interfaces": []
                },
                {
                    "id": 1004,
                    "name": "fddinet-default",
                    "enabled": False,
                    "interfaces": []
                },
                {
                    "id": 1005,
                    "name": "trnet-default",
                    "enabled": False,
                    "interfaces": []
                }
            ]
        }


class AcceptVlanModel(BaseModel):
    id: int
    interface: str
    bridgeName: Optional[str]

    class Config:
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** switch",
                    "value": {
                        "id": 101,
                        "interface": "Gi1/1"
                    }
                },
                "Mikrotik": {
                    "description": "An example for **Mikrotik** switch",
                    "value": {
                        "id": 101,
                        "interface": "ether3",
                        "bridgeName": "switch"
                    }
                }
            }
        }


class CiscoAcceptVlanModel(BaseModel):
    id: int
    interface: str


class MikrotikAcceptVlanModel(BaseModel):
    id: int
    interface: str
    bridgeName: str


class TrunkModeModel(BaseModel):
    interface: str
    bridgeName: Optional[str]

    class Config:
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** switch",
                    "value": {
                        "interface": "Gi1/1"
                    }
                },
                "Mikrotik": {
                    "description": "An example for **Mikrotik** switch",
                    "value": {
                        "interface": "ether3",
                    }
                }
            }
        }


class CiscoTrunkModel(BaseModel):
    interface: str


class MikrotikTrunkModel(BaseModel):
    interface: str
    bridgeName: str


class CreateVlanModel(BaseModel):
    id: int
    name: str

    class Config:
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** switch",
                    "value": {
                        "id": 10,
                        "name": "School"
                    }
                }
            }
        }

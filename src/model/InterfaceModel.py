from pydantic import BaseModel
from typing import Optional
from enum import Enum
from ipaddress import IPv4Address
from src.model.Base import CiscoEnable


class LearnedBy(Enum):
    STATIC = 0
    DYNAMIC = 1
    UNSET = 3


class InterfaceShort(BaseModel):
    interface: Optional[str]
    ipaddress: Optional[str] = ''
    mask: Optional[str] = ''
    learnedBy: Optional[str] = ''
    enabled: Optional[bool] = False

    class Config:
        schema_extra = {
            "example":
                [
                    {
                        "interface": "FastEthernet0/0",
                        "ipaddress": "158.193.152.76",
                        "mask": "255.255.255.128",
                        "learnedBy": "DYNAMIC",
                        "enabled": True
                    },
                    {
                        "interface": "FastEthernet0/1",
                        "ipaddress": "192.158.10.10",
                        "mask": "255.255.255.0",
                        "learnedBy": "",
                        "enabled": True
                    },
                    {
                        "interface": "Serial1/0",
                        "ipaddress": "",
                        "mask": "",
                        "learnedBy": "",
                        "enabled": False
                    }
                ]

        }


class InterfaceStatusModel(BaseModel):
    interface: str
    enabled: bool

    class Config:
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** devices",
                    "value": {
                        "interface": "Gi0/1",
                        "enabled": False
                    }
                },
                "Mikrotik": {
                    "description": "An example for **Mikrotik** devices",
                    "value": {
                        "interface": "ether5",
                        "enabled": True
                    }
                }
            }
        }


class CiscoInterfaceStatusModel(BaseModel):
    interface: str
    enabled: bool


class MikrotikInterfaceStatusModel(BaseModel):
    interface: str
    enabled: bool


class InterfaceIpModel(BaseModel):
    interface: str
    address: IPv4Address
    mask: IPv4Address

    class Config:
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** routers",
                    "value": {
                        "interface": "Fastethernet 0/1",
                        "address": "188.188.18.1",
                        "mask": "255.255.255.0",
                    }
                },
                "Mikrotik": {
                    "description": "An example for **Mikrotik** routers",
                    "value": {
                        "interface": "ether4",
                        "address": "188.188.18.1",
                        "mask": "255.255.255.0"
                    }
                }
            }
        }


class CiscoInterfaceIpModel(BaseModel):
    interface: str
    address: IPv4Address
    mask: IPv4Address


class MikrotikInterfaceIpModel(BaseModel):
    interface: str
    address: IPv4Address
    mask: IPv4Address

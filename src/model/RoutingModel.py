from pydantic import BaseModel, validator, Field
from typing import Optional, Union
from src.core.config import settings
from fastapi.exceptions import HTTPException
from fastapi import status
from ipaddress import IPv4Address
from src.model.Base import CiscoEnable


class RouteModel(BaseModel):
    address: str = None
    mask: str = None
    interface: str = None
    nextHop: str = None
    learned: str = None


class NetworkModel(BaseModel):
    network: Optional[str]
    mask: str = None
    interface: str = None
    nextHop: str = None
    learned: str = None


class RoutingTableModel(BaseModel):
    defaultGateway: Optional[str]
    networks: Union[list[NetworkModel]] = []

    class Config:
        schema_extra = {
            "example": {
                "defaultGateway": "158.193.152.1",
                "networks": [
                    {
                        "address": "158.193.152.0",
                        "mask": "255.255.255.128",
                        "interface": "FastEthernet0/0",
                        "nextHop": "",
                        "learned": "C"
                    },
                    {

                        "address": "192.158.10.0",
                        "mask": "255.255.255.0",
                        "interface": "FastEthernet0/1",
                        "nextHop": "",
                        "learned": "C"

                    },
                    {
                        "address": "199.200.11.0",
                        "mask": "255.255.255.0",
                        "interface": "FastEthernet0/1",
                        "nextHop": "183.183.180.2",
                        "learned": "S"
                    }
                ]
            }
        }


class StaticRouteModel(BaseModel):
    network: IPv4Address
    networkMask: IPv4Address
    nextHop: Optional[IPv4Address]
    nextHopInterface: Optional[str]
    distance: Optional[int]

    class Config:
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** routers",
                    "value": {
                        "network": "199.200.11.0",
                        "networkMask": "255.255.255.0",
                        "nextHop": "183.183.180.2",
                        "nextHopInterface": "Serial1/0",
                        "distance": 23
                    }
                },
                "Mikrotik": {
                    "description": "An example for **Mikrotik** routers",
                    "value": {
                        "network": "199.200.11.0",
                        "networkMask": "255.255.255.0",
                        "nextHop": "183.183.180.2",
                        "distance": 23,
                    }
                }
            }
        }

    @validator('nextHopInterface')
    def nextHop_xor_nextHopInt(cls, v, values):
        if 'nextHop' not in values and not v:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Either nextHop or nextHopInterface is required"
            )
        return v


class CiscoStaticRouteModel(BaseModel):
    network: IPv4Address
    networkMask: IPv4Address
    nextHop: Optional[IPv4Address]
    nextHopInterface: Optional[str]
    distance: Optional[int]


class OSPFNetworkModel(BaseModel):
    network: IPv4Address
    mask: IPv4Address
    area: IPv4Address


class OSPFModel(BaseModel):
    processId: Optional[int] = None
    name: Optional[str] = None
    routerId: IPv4Address
    networks: list[OSPFNetworkModel]
    passiveInterfaces: Optional[list[str]] = None
    internetRoute: bool = False
    shareStatic: bool = False

    class Config:
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** routers",
                    "value": {
                        "processId": 10,
                        "routerId": "1.1.1.1",
                        "networks": [
                            {
                                "network": "192.158.10.0",
                                "mask": "255.255.255.0",
                                "area": "0.0.0.0"
                            },
                            {
                                "network": "201.10.10.0",
                                "mask": "255.255.255.0",
                                "area": "0.0.0.0"
                            },
                            {
                                "network": "192.153.155.0",
                                "mask": "255.255.255.0",
                                "area": "1.1.1.1"
                            }
                        ],
                        "internetRoute": True,
                        "shareStatic": False,
                    }
                },
                "Mikrotik": {
                    "description": "An example for **Mikrotik** routers",
                    "value": {
                        "name": "ospf-mikrotik",
                        "routerId": "2.2.2.2",
                        "networks": [
                            {
                                "network": "192.158.10.0",
                                "mask": "255.255.255.0",
                                "area": "0.0.0.0"
                            },
                            {
                                "network": "201.10.10.0",
                                "mask": "255.255.255.0",
                                "area": "0.0.0.0"
                            },
                            {
                                "network": "192.153.155.0",
                                "mask": "255.255.255.0",
                                "area": "1.1.1.1"
                            }
                        ],
                        "internetRoute": False,
                        "shareStatic": False,
                    }
                }
            }
        }


class CiscoOspfModel(BaseModel):
    processId: int
    routerId: IPv4Address
    networks: list[OSPFNetworkModel]
    passiveInterfaces: Optional[list[str]]
    internetRoute: bool = False
    shareStatic: bool = False


class MikrotikOspfModel(BaseModel):
    name: str
    routerId: IPv4Address
    networks: list[OSPFNetworkModel]
    internetRoute: bool = False
    shareStatic: bool = False


class OSPFModelResponse(BaseModel):
    processId: Optional[int] = None
    name: Optional[str] = None
    routerId: str = None
    networks: Optional[list[OSPFNetworkModel]] = None
    passiveInterfaces: Optional[list[str]] = None
    internetRoute: bool = False
    shareStatic: bool = False

    class Config:
        schema_extra = {
            "example": {
                "processId": 10,
                "routerId": "1.1.1.1",
                "networks": [
                    {
                        "network": "192.158.10.0",
                        "mask": "255.255.255.0",
                        "area": "3.3.3.3"
                    },
                    {
                        "network": "201.10.10.0",
                        "mask": "255.255.255.0",
                        "area": "0.0.0.0"
                    },
                    {
                        "network": "192.153.155.0",
                        "mask": "255.255.255.0",
                        "area": "1.1.1.1"
                    }
                ],
                "internetRoute": False,
                "shareStatic": True,
            }
        }


class AddOSPFNetworkModel(BaseModel):
    network: IPv4Address
    mask: IPv4Address
    area: IPv4Address

    class Config:
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** routers",
                    "value": {
                        "network": "192.133.13.0",
                        "mask": "255.255.255.0",
                        "area": "0.0.0.0"
                    }
                },
                "Mikrotik": {
                    "description": "An example for **Mikrotik** routers",
                    "value": {
                        "network": "192.133.13.0",
                        "mask": "255.255.255.0",
                        "area": "0.0.0.0",
                    }
                }
            }
        }


class CiscoAddOspfNetworkModel(BaseModel):
    network: IPv4Address
    mask: IPv4Address
    area: IPv4Address

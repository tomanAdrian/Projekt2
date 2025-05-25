from ipaddress import IPv4Address

from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Location(str, Enum):
    INSIDE = 'inside'
    OUTSIDE = 'outside'


class Protocols(str, Enum):
    TCP = 'tcp'
    UDP = 'udp'


class SNATModel(BaseModel):
    iAddress: IPv4Address
    oAddress: IPv4Address

    class Config:
        schema_extra = {
            "examples": {
                "Mikrotik": {
                    "value": {
                        "iAddress": "192.158.10.23",
                        "oAddress": "213.158.192.110"
                    }
                },
                "Cisco": {
                    "value": {
                        "iAddress": "192.158.10.23",
                        "oAddress": "213.158.192.110",
                    }
                }
            }
        }


class CiscoSNATModel(BaseModel):
    iAddress: IPv4Address
    oAddress: IPv4Address


class NetworkModel(BaseModel):
    network: IPv4Address
    mask: IPv4Address


class PATModel(BaseModel):
    aclId: Optional[int]
    acceptedAddresses: Optional[list[NetworkModel]]
    oInterface: str

    class Config:
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** routers",
                    "value": {
                        "aclId": 1,
                        "acceptedAddresses":
                            [
                                {
                                    "network": "192.158.10.0",
                                    "mask": "255.255.255.0"
                                }
                            ],
                        "oInterface": "Fastethernet 0/1"
                    }
                },
                "Mikrotik": {
                    "description": "An example for **Mikrotik** routers",
                    "value": {
                        "oInterface": "ether1"
                    }
                }
            }
        }


class CiscoPATModel(BaseModel):
    aclId: int
    acceptedAddresses: list[NetworkModel]
    oInterface: str


class InterfacePortRedirectionModel(BaseModel):
    address: IPv4Address
    port: int


class PortRedirectionModel(BaseModel):
    protocol: Protocols
    inside: InterfacePortRedirectionModel
    outside: InterfacePortRedirectionModel

    class Config:
        use_enum_values = True
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** routers",
                    "value": {
                        "protocol": "tcp",
                        "inside": {
                            "address": "192.158.10.9",
                            "port": 22
                        },
                        "outside": {
                            "address": "193.158.123.76",
                            "port": 29
                        }
                    }
                },
                "Mikrotik": {
                    "description": "An example for **Mikrotik** routers",
                    "value": {
                        "protocol": "tcp",
                        "inside": {
                            "address": "192.158.10.9",
                            "port": 22
                        },
                        "outside": {
                            "address": "193.158.123.76",
                            "port": 29
                        }
                    }
                }
            }
        }


class CiscoPortRedirectionModel(BaseModel):
    protocol: Protocols
    inside: InterfacePortRedirectionModel
    outside: InterfacePortRedirectionModel


class InterfaceDNATModel(BaseModel):
    address: IPv4Address
    mask: IPv4Address


class AddressRangeModel(BaseModel):
    start: IPv4Address
    end: IPv4Address
    mask: IPv4Address


class DNATModel(BaseModel):
    poolName: Optional[str]
    aclId: Optional[int]
    inside: InterfaceDNATModel
    outside: AddressRangeModel

    class Config:
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** routers",
                    "value": {
                        "poolName": "Public-Nat-Pool",
                        "aclId": 12,
                        "inside": {
                            "address": "192.158.10.0",
                            "mask": "255.255.255.0"
                        },
                        "outside": {
                            "start": "10.10.10.1",
                            "end": "10.10.10.10",
                            "mask": "255.255.255.128"
                        }
                    }
                },
                "Mikrotik": {
                    "description": "An example for **Mikrotik** routers",
                    "value": {
                        "inside": {
                            "address": "192.158.10.0",
                            "mask": "255.255.255.0"
                        },
                        "outside": {
                            "start": "10.10.10.1",
                            "end": "10.10.10.10",
                            "mask": "255.255.255.0"
                        }
                    }
                }
            }
        }


class CiscoDNATModel(BaseModel):
    poolName: str
    aclId: int
    inside: InterfaceDNATModel
    outside: AddressRangeModel


class LocationModel(BaseModel):
    interface: str
    location: Location

    class Config:
        use_enum_values = True
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** routers",
                    "value": {
                        "interface": "Fastethernet 0/1",
                        "location": "outside"
                    }
                }
            }
        }

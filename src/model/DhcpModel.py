import ipaddress
from ipaddress import IPv4Address

from pydantic import BaseModel, validator
from typing import Optional, Union
from src.model.Base import CiscoEnable


class AddressesRangeModel(BaseModel):
    start: IPv4Address
    end: IPv4Address


class DhcpStatusModel(BaseModel):
    poolName: Optional[str]
    network: Optional[str]
    mask: Optional[str]
    defaultRouter: Optional[str]
    dnsServer: Optional[str]
    domainName: Optional[str]
    interface: Optional[str]
    excludedAddresses: Optional[list[Optional[AddressesRangeModel]]]
    addressRange: Optional[AddressesRangeModel]

    class Config:
        schema_extra = {
            "example": {
                "poolName": "cisco-api-dhcp-v2",
                "network": "192.158.10.0",
                "mask": "255.255.255.0",
                "defaultRouter": "192.158.10.9",
                "dnsServer": "8.8.8.8",
                "domainName": "api.cisco.com",
                "interface": "ether2",
                "addressRange": {
                    "start": "192.158.10.10",
                    "end": "192.158.10.20"
                }

            }
        }


class DhcpLeasedAddressModel(BaseModel):
    client: str
    address: str
    expiration: str

    class Config:
        schema_extra = {
            "example": {
                "client": "7EV2.7Q54.2M4Z",
                "address": "192.158.10.23",
                "expiration": "29-1-2023, 14:30:50"
            }
        }


class DhcpModel(BaseModel):
    poolName: str
    network: IPv4Address
    mask: IPv4Address
    defaultRouter: Optional[IPv4Address]
    dnsServer: Optional[IPv4Address]
    domainName: Optional[str]
    excludedAddresses: Optional[AddressesRangeModel]
    addressRange: Optional[AddressesRangeModel]
    interface: Optional[str]

    class Config:
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** routers",
                    "value": {
                        "poolName": "cisco-api-dhcp-v2",
                        "network": "192.158.10.0",
                        "mask": "255.255.255.0",
                        "defaultRouter": "192.158.10.9",
                        "dnsServer": "8.8.8.8",
                        "domainName": "api.cisco.com",
                        "excludedAddresses": [
                            {
                                "start": "192.158.10.1",
                                "end": "192.158.10.10"
                            },
                            {
                                "start": "192.158.10.9",
                                "end": "192.158.10.10"
                            }
                        ]
                    }
                },
                "Mikrotik": {
                    "description": "An example for **Mikrotik** routers",
                    "value": {
                        "poolName": "cisco-api-dhcp-v2",
                        "network": "192.158.10.0",
                        "mask": "255.255.255.0",
                        "defaultRouter": "192.158.10.9",
                        "dnsServer": "8.8.8.8",
                        "domainName": "api.cisco.com",
                        "interface": "ether2",
                        "addressRange": {
                            "start": "192.158.10.10",
                            "end": "192.158.10.20"
                        }
                    }
                }
            }
        }


class CiscoDhcpModel(BaseModel):
    poolName: str
    network: IPv4Address
    mask: IPv4Address
    defaultRouter: Optional[IPv4Address]
    dnsServer: Optional[IPv4Address]
    domainName: Optional[str]
    excludedAddresses: Optional[AddressesRangeModel]


class MikrotikDhcpModel(BaseModel):
    poolName: str
    network: IPv4Address
    mask: IPv4Address
    defaultRouter: Optional[IPv4Address]
    dnsServer: Optional[IPv4Address]
    domainName: Optional[str]
    addressRange: AddressesRangeModel
    interface: str


class DhcpRemoveModel(BaseModel):
    network: Optional[IPv4Address]
    mask: Optional[IPv4Address]

    class Config:
        schema_extra = {
            "examples": {
                "Cisco": {
                    "description": "An example for **Cisco** routers",
                    "value": {

                    }
                },
                "Mikrotik": {
                    "description": "An example for **Mikrotik** routers",
                    "value": {
                        "network": "192.158.10.0",
                        "mask": "255.255.255.0"
                    }
                }
            }
        }


class DhcpRemoveModelMikrotik(BaseModel):
    network: IPv4Address
    mask: IPv4Address

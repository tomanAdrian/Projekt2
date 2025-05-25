from pydantic import BaseSettings
from enum import Enum


class TypeOfConnection(str, Enum):
    SSH = 'ssh'
    TELNET = 'telnet'


class Vendors(str, Enum):
    CISCO = 'cisco'
    MIKROTIK = 'mikrotik'


class QueryDescription(str, Enum):
    HOST = 'IP address of configured device'
    NAME = 'Username with which can APP access to device'
    PASSWORD = 'Password with which can APP access to device'
    CONNECTION = 'Type of connection with device'
    PORT = 'Port on which is device accessible'
    ENABLE = 'Password in privileged mode - Cisco devices'
    VENDOR = 'Vendor of configured device'
    POOL_NAME = 'Defined pool name during creation of DHCP-server'


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Network devices - API Gateway'
    MAX_BUFFER = 65535
    SLEEP_TIME = 0.5
    VENDORS = [
        'cisco',
        'mikrotik',
        'junos'
    ]
    SUPPORTED_INTERFACES = [
        'Fastethernet',
        'Serial',
        'ether'
    ]


settings = Settings()

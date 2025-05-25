from src.core.config import settings
from http import HTTPStatus
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from enum import Enum

import json


class TypeOfValidation(Enum):
    NONE = 0
    PORT = 1
    ENABLE = 2
    DHCP_REMOVE = 3
    OSPF_INSTANCE_CREATION = 4
    OSPF_DELETION = 5
    IP_ADD = 6
    IP_DELETION = 7
    OUTPUT = 8
    OSPF_NETWORK_ADDITION = 9


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Enable password is mandatory for Cisco devices"}
        }


class CommandExecutionError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code: int = status_code
        self.message: str = message
        super().__init__(message)

    def json(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status_code,
            content=json.loads(self.message)
        )


def validateEnablePassword(vendor: str, enablePassword: str):
    if vendor.lower() == 'cisco' and enablePassword is None:
        raise CommandExecutionError(status_code=status.HTTP_401_UNAUTHORIZED,
                                    message='{"detail": "Enable password is required for Cisco devices"}')


def validateOutputFromConsole(output: str, typeOfValidation: TypeOfValidation):
    if typeOfValidation == TypeOfValidation.PORT:
        validateOutputPort(output=output)
    elif typeOfValidation == TypeOfValidation.ENABLE:
        validateOutputEnablePassword(output=output)
    elif typeOfValidation == TypeOfValidation.DHCP_REMOVE:
        validateOutputDhcpRemove(output=output)
    elif typeOfValidation == TypeOfValidation.OSPF_INSTANCE_CREATION:
        validateOspfInstanceCreation(output=output)
    elif typeOfValidation == TypeOfValidation.OSPF_DELETION:
        validateOspfDeletionOutput(output=output)
    elif typeOfValidation == TypeOfValidation.IP_ADD:
        validateIpAddOutput(output=output)
    elif typeOfValidation == TypeOfValidation.IP_DELETION:
        validateIpDeletionOutput(output=output)
    elif typeOfValidation == TypeOfValidation.OSPF_NETWORK_ADDITION:
        validateOspfNetworkAddition(output=output)


def validateOutputPort(output: str):
    if output.find('Invalid input detected') != -1 or output.find('no such item') != -1 or output.find(
            'expected end of command') != -1 or output.find('any value of interface') != -1 or output.lower().find(
        'incomplete comand') != -1:
        raise CommandExecutionError(status.HTTP_403_FORBIDDEN, '{"detail": "Unknown interface"}')


def validateOutputEnablePassword(output: str):
    if output.find('#') == -1:
        raise CommandExecutionError(status_code=status.HTTP_401_UNAUTHORIZED,
                                    message='{"detail": "Missing or incorrect enable password"}')


def validateOutputDhcpRemove(output: str):
    if output.find('is not in') != -1 or output.find('no such item') != -1:
        raise CommandExecutionError(status_code=status.HTTP_403_FORBIDDEN,
                                    message='{"detail": "DHCP-server with specified name does not exist"}')


def raiseSshAuthCredentialsError(user: str):
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail=f"Unable to initiate SSH connection. User: {user}"
    )


def raiseNotImplementedError(vendor: str):
    raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail=f"This method is not implemented for particular vendors. Vendor: {vendor}"
    )


def validateOspfNetworkAddition(output: str):
    if output.lower().find('any value of instance') != -1:
        raise CommandExecutionError(status_code=status.HTTP_403_FORBIDDEN,
                                    message='{"detail": "Unknown OSPF instance"}')


def validateOspfInstanceCreation(output: str):
    if output.find('failure') != -1:
        raise CommandExecutionError(status_code=status.HTTP_403_FORBIDDEN,
                                    message='{"detail": "OSPF instance with specified name already exist"}')
    elif output.find('expected end of command') != -1:
        raise CommandExecutionError(status_code=status.HTTP_403_FORBIDDEN,
                                    message='{"detail": "Unable to initiate OSPF instance on this device"}')


def validateOspfDeletionOutput(output: str):
    if output.find('Invalid input detected') != -1 or output.find('no such item') != -1:
        raise CommandExecutionError(status_code=status.HTTP_403_FORBIDDEN,
                                    message='{"detail": "Specified OSPF identifier does not exist"}')


def validateIpAddOutput(output: str):
    if output.find('Bad mask') != -1 or output.find('input does not match') != -1:
        raise CommandExecutionError(status_code=status.HTTP_403_FORBIDDEN,
                                    message='{"detail": "Invalid mask for IP address OR interface"}')


def validateIpDeletionOutput(output: str):
    if output.find('Invalid address') != -1:
        raise CommandExecutionError(status_code=status.HTTP_403_FORBIDDEN,
                                    message='{"detail": "IP address does not exist. Check request body"}')


def missingRequiredAttribute(error) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content=json.loads(error.json())
    )

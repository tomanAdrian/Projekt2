from src.commands.interface.InterfaceCommands import Interface
from src.model.InterfaceModel import InterfaceStatusModel, InterfaceIpModel, MikrotikInterfaceStatusModel, CiscoInterfaceIpModel, MikrotikInterfaceIpModel, CiscoInterfaceStatusModel
from src.core.config import TypeOfConnection
from src.api.controllers.Controller import Controller
from src.core.config import Vendors
from pydantic import ValidationError
from fastapi.exceptions import HTTPException
from src.api.validators.Validators import missingRequiredAttribute


def validateChangeStatusBody(body: InterfaceStatusModel, vendor: str):
    if vendor == Vendors.CISCO:
        CiscoInterfaceStatusModel.parse_obj(body)
    elif vendor == Vendors.MIKROTIK:
        MikrotikInterfaceStatusModel.parse_obj(body)


def validateSetIpBody(body: InterfaceIpModel, vendor: str):
    if vendor == Vendors.CISCO:
        CiscoInterfaceIpModel.parse_obj(body)
    elif vendor == Vendors.MIKROTIK:
        MikrotikInterfaceIpModel.parse_obj(body)


class InterfaceController(Controller):
    def __init__(self):
        super().__init__()

    def getInterfacesBrief(self, host: str, user: str, password: str, vendor: str, port: int,
                           connection: TypeOfConnection):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.getInterfacesBrief():
            interfaces = communication.executeCommand(command=command, shell=shell)

        for command in commands.showProtocols():
            showProtocols = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()

        interfaces = parser.parseInterfaceBrief(interfaces)
        interfaces = parser.parseShowProtocols(showProtocols, interfaces)
        return interfaces

    def setInterfaceStatus(self, host: str, user: str, password: str, vendor: str, port: int,
                           interface: InterfaceStatusModel, connection: TypeOfConnection, enablePassword: str):
        validateChangeStatusBody(interface, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.setInterfaceStatus(interface=interface.interface, enabled=interface.enabled,
                                                   enablePass=enablePassword):
            console = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return

    def setIpaddress(self, host: str, user: str, password: str, vendor: str, port: int, body: InterfaceIpModel,
                     connection: TypeOfConnection, enablePassword: str):
        validateSetIpBody(body, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.setIpaddress(body=body, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return

    def deleteIpaddress(self, host: str, user: str, password: str, vendor: str, port: int, body: InterfaceIpModel,
                        connection: TypeOfConnection, enablePassword: str):
        validateSetIpBody(body, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.deleteIpaddress(body=body, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return

    def getCommands(self, vendor: str) -> Interface:
        if vendor == 'cisco':
            return self.ciscoRouterCommands
        elif vendor == 'mikrotik':
            return self.mikrotikRouterCommands

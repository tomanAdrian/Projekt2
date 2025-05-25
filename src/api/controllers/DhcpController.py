import time
import json

from src.model.DhcpModel import DhcpModel, CiscoDhcpModel, MikrotikDhcpModel, DhcpRemoveModel, DhcpRemoveModelMikrotik
from src.core.config import TypeOfConnection, Vendors
from src.api.controllers.Controller import Controller
from src.commands.dhcp.DhcpCommands import DHCP


def validateDhcpCreateBody(body: DhcpModel, vendor: str):
    if vendor == Vendors.CISCO:
        CiscoDhcpModel.parse_obj(body)
    elif vendor == Vendors.MIKROTIK:
        MikrotikDhcpModel.parse_obj(body)


def validateDhcpRemoveBody(body: DhcpRemoveModel, vendor: str):
    if vendor == Vendors.MIKROTIK:
        DhcpRemoveModelMikrotik.parse_obj(body)


class DhcpController(Controller):
    def __init__(self):
        super().__init__()

    def getDhcpStatus(self, host: str, user: str, password: str, vendor: str, port: int, enablePassword: str,
                      connection: TypeOfConnection):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        dhcpParams = ''
        for command in commands.dhcpParameters(enablePassword=enablePassword):
            dhcpParams += communication.executeCommand(command=command, shell=shell, sleepTime=3.0)

        communication.closeConnection()

        dhcpParams = parser.parseDhcpParams(dhcpParams)
        return dhcpParams

    def getDhcpLeasesAddresses(self, host: str, user: str, password: str, vendor: str, port: int,
                               connection: TypeOfConnection):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        leasedAddresses = None
        for command in commands.dhcpLeasedAddresses():
            leasedAddresses = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        leasedAddresses = parser.parseLeasedAddresses(leasedAddresses)
        return leasedAddresses

    def dhcpCreate(self, host: str, user: str, password: str, vendor: str, port: int, dhcp: DhcpModel,
                   connection: TypeOfConnection, enablePassword: str):
        validateDhcpCreateBody(dhcp, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.dhcpCreate(body=dhcp, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return {}

    def dhcpRemove(self, host: str, user: str, password: str, vendor: str, port: int, enablePassword: str,
                   poolName: str, connection: TypeOfConnection, body: DhcpRemoveModel):
        validateDhcpRemoveBody(body=body, vendor=vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.dhcpRemove(poolName=poolName, body=body, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return {}

    def getCommands(self, vendor: str) -> DHCP:
        if vendor == 'cisco':
            return self.ciscoRouterCommands
        elif vendor == 'mikrotik':
            return self.mikrotikRouterCommands

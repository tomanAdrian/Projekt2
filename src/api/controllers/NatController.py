from src.commands.ios.cisco.Router import CiscoRouter
from src.commands.nat.NatCommands import Nat
from src.core.config import TypeOfConnection, Vendors
from src.api.controllers.Controller import Controller

from src.model.NatModel import SNATModel, DNATModel, PATModel, PortRedirectionModel, LocationModel, CiscoDNATModel, \
    CiscoPortRedirectionModel, CiscoPATModel, CiscoSNATModel
from src.api.validators.Validators import raiseNotImplementedError


def validateSNATBody(body: SNATModel, vendor: str):
    if vendor == Vendors.CISCO:
        CiscoSNATModel.parse_obj(body)


def validateDNATBody(body: DNATModel, vendor: str):
    if vendor == Vendors.CISCO:
        CiscoDNATModel.parse_obj(body)


def validatePATBody(body: PATModel, vendor: str):
    if vendor == Vendors.CISCO:
        CiscoPATModel.parse_obj(body)


def validatePortRedirectionBody(body: PortRedirectionModel, vendor: str):
    if vendor == Vendors.CISCO:
        CiscoPortRedirectionModel.parse_obj(body)


class NatController(Controller):
    def __init__(self):
        super().__init__()

    def getSNAT(self, host: str, user: str, password: str, vendor: str, port: int, connection: TypeOfConnection, enablePassword: str):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.getSNAT(enablePassword=enablePassword):
            config = communication.executeCommand(command=command, shell=shell, sleepTime=3.0)

        communication.closeConnection()
        return parser.parseSNAT(config)

    def getDNAT(self, host: str, user: str, password: str, vendor: str, port: int, connection: TypeOfConnection, enablePassword: str):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.getDNAT(enablePassword=enablePassword):
            config = communication.executeCommand(command=command, shell=shell, sleepTime=3.0)

        communication.closeConnection()
        return parser.parseDNAT(config)

    def getPAT(self, host: str, user: str, password: str, vendor: str, port: int, connection: TypeOfConnection, enablePassword: str):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.getPAT(enablePassword=enablePassword):
            config = communication.executeCommand(command=command, shell=shell, sleepTime=3.0)

        communication.closeConnection()
        return parser.parsePAT(config)

    def getPortForward(self, host: str, user: str, password: str, vendor: str, port: int, connection: TypeOfConnection, enablePassword: str):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.getPortForward(enablePassword=enablePassword):
            config = communication.executeCommand(command=command, shell=shell, sleepTime=3.0)

        communication.closeConnection()
        return parser.parsePortForward(config)

    def setSNAT(self, host: str, user: str, password: str, vendor: str, port: int, body: SNATModel,
                connection: TypeOfConnection, enablePassword: str):
        validateSNATBody(body, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.setSNAT(body=body, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)
        communication.closeConnection()

    def setDNAT(self, host: str, user: str, password: str, vendor: str, port: int, body: DNATModel,
                connection: TypeOfConnection, enablePassword: str):
        validateDNATBody(body, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.setDNAT(body=body, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()

    def setPAT(self, host: str, user: str, password: str, vendor: str, port: int, body: PATModel,
               connection: TypeOfConnection, enablePassword: str):
        validatePATBody(body, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.setPAT(body=body, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()

    def setPortRedirection(self, host: str, user: str, password: str, vendor: str, port: int,
                           body: PortRedirectionModel, connection: TypeOfConnection, enablePassword: str):
        validatePortRedirectionBody(body, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.setPortRedirection(body=body, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()

    def setLocation(self, host: str, user: str, password: str, vendor: str, port: int, body: LocationModel,
                    connection: TypeOfConnection, enablePassword: str):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        if isinstance(commands, CiscoRouter):
            for command in commands.setLocation(location=body, enablePassword=enablePassword):
                output = communication.executeCommand(command=command, shell=shell)
            communication.closeConnection()
        else:
            communication.closeConnection()
            raiseNotImplementedError(vendor=vendor)
        return

    def getCommands(self, vendor: str) -> Nat:
        if vendor == 'cisco':
            return self.ciscoRouterCommands
        elif vendor == 'mikrotik':
            return self.mikrotikRouterCommands

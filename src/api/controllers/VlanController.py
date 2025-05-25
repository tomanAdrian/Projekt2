from src.api.validators.Validators import raiseNotImplementedError
from src.model.VlanModel import AcceptVlanModel, TrunkModeModel, CreateVlanModel, CiscoTrunkModel, CiscoAcceptVlanModel, \
    MikrotikTrunkModel, MikrotikAcceptVlanModel
from src.core.config import TypeOfConnection, Vendors
from src.commands.vlan.VlanCommands import Vlan
from src.api.controllers.Controller import Controller
from src.commands.ios.cisco.Switch import CiscoSwitch
from src.commands.ios.mikrotik.Switch import MikrotikSwitch


def validateAcceptVlanBody(body: AcceptVlanModel, vendor: str):
    if vendor == Vendors.CISCO:
        CiscoAcceptVlanModel.parse_obj(body)
    elif vendor == Vendors.MIKROTIK:
        MikrotikAcceptVlanModel.parse_obj(body)


def validateTrunkBody(body: TrunkModeModel, vendor: str):
    if vendor == Vendors.CISCO:
        CiscoTrunkModel.parse_obj(body)
    elif vendor == Vendors.MIKROTIK:
        MikrotikTrunkModel.parse_obj(body)


class VlanController(Controller):
    def __init__(self):
        super().__init__()

    def showVlan(self, host: str, user: str, password: str, vendor: str, port: int, connection: TypeOfConnection):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.showVlan():
            vlan = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return parser.parseVlan(vlan)

    def acceptVlan(self, host: str, user: str, password: str, vendor: str, port: int, body: AcceptVlanModel,
                   connection: TypeOfConnection, enablePassword: str):
        validateAcceptVlanBody(body, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.acceptVlan(body=body, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return

    def trunkMode(self, host: str, user: str, password: str, vendor: str, port: int, body: TrunkModeModel,
                  connection: TypeOfConnection, enablePassword: str):
        validateTrunkBody(body, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.trunkMode(body=body, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return

    def createVlan(self, host: str, user: str, password: str, vendor: str, port: int, body: CreateVlanModel,
                   connection: TypeOfConnection, enablePassword: str):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        if isinstance(commands, CiscoSwitch):
            for command in commands.createVlan(body=body, enablePassword=enablePassword):
                output = communication.executeCommand(command=command, shell=shell)
            communication.closeConnection()
        else:
            communication.closeConnection()
            raiseNotImplementedError(vendor=vendor)
        return

    def createBridge(self, host: str, user: str, password: str, vendor: str, port: int, name: str,
                     connection: TypeOfConnection):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        if isinstance(commands, MikrotikSwitch):
            for command in commands.createBridge(name=name):
                output = communication.executeCommand(command=command, shell=shell)
            communication.closeConnection()
        else:
            communication.closeConnection()
            raiseNotImplementedError(vendor=vendor)
        return

    def deleteVlan(self, host: str, user: str, password: str, vendor: str, port: int, vlanId: int,
                   connection: TypeOfConnection, enablePassword: str = None):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.deleteVlan(vlanId=vlanId, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return

    def getCommands(self, vendor: str) -> Vlan:
        if vendor == 'cisco':
            return self.ciscoSwitchCommands
        elif vendor == 'mikrotik':
            return self.mikrotikSwitchCommands

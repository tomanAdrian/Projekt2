from src.commands.ios.cisco.Router import CiscoRouter
from src.commands.ios.mikrotik.Router import MikrotikRouter
from src.commands.ios.cisco.Switch import CiscoSwitch
from src.commands.ios.mikrotik.Switch import MikrotikSwitch
from src.communication.Communication import SshShellCommunication, SshExecCommunication, TelnetCommunication, Communication
from src.parser.Parser import Parser
from src.parser.CiscoParser import CiscoParser
from src.parser.MikrotikParser import MikrotikParser
from src.core.config import TypeOfConnection
from paramiko import Channel


class Controller:
    def __init__(self):
        self.ciscoRouterCommands = CiscoRouter()
        self.mikrotikRouterCommands = MikrotikRouter()
        self.ciscoSwitchCommands = CiscoSwitch()
        self.mikrotikSwitchCommands = MikrotikSwitch()
        self.ciscoParser = CiscoParser()
        self.mikrotikParser = MikrotikParser()
        self.shellCommunication = SshShellCommunication()
        self.execCommunication = SshExecCommunication()
        self.telnetCommunication = TelnetCommunication()

    def init(self, host: str, user: str, password: str, vendor: str, port: int, connection: TypeOfConnection) -> (Communication, Channel, Parser):
        if connection == TypeOfConnection.SSH:
            if vendor.lower() == self.ciscoRouterCommands.getVendor():
                self.shellCommunication.initConnection(host=host, username=user, password=password, port=port, typeOfConnection=connection)
                return self.shellCommunication, self.shellCommunication.invokeShell(), self.ciscoParser
            elif vendor.lower() == self.mikrotikRouterCommands.getVendor():
                self.execCommunication.initConnection(host=host, username=user, password=password, port=port, typeOfConnection=connection)
                return self.execCommunication, self.execCommunication.invokeShell(), self.mikrotikParser
        else:
            self.telnetCommunication.initConnection(host=host, username=user, password=password, port=port, typeOfConnection=connection)
            if vendor.lower() == self.ciscoRouterCommands.getVendor():
                return self.telnetCommunication, self.telnetCommunication.invokeShell(), self.ciscoParser
            elif vendor.lower() == self.mikrotikRouterCommands.getVendor():
                return self.telnetCommunication, self.telnetCommunication.invokeShell(), self.mikrotikParser


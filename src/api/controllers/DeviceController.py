from src.core.config import TypeOfConnection
from src.api.controllers.Controller import Controller
from src.model.DeviceModel import ConfigurationModel
from src.commands.ios.cisco.Router import CiscoRouter
from src.api.validators.Validators import raiseNotImplementedError


class DeviceController(Controller):
    def __init__(self):
        super().__init__()

    def getConfiguration(self, host: str, user: str, password: str, vendor: str, port: int,
                         connection: TypeOfConnection, enablePassword: str) -> ConfigurationModel:
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.getConfig(enablePassword=enablePassword):
            config = communication.executeCommand(command=command, shell=shell, sleepTime=3.0)

        communication.closeConnection()
        config = "\n".join(config.splitlines())
        return ConfigurationModel(config=config)

    def getVersion(self, host: str, user: str, password: str, vendor: str, port: int,
                   connection: TypeOfConnection):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        version = ''
        for command in commands.getVersion():
            version += communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return parser.parseVersion(version)

    def saveConfiguration(self, host: str, user: str, password: str, vendor: str, port: int,
                          connection: TypeOfConnection, enablePassword: str):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        if isinstance(commands, CiscoRouter):
            for command in commands.saveConfig(enablePassword=enablePassword):
                output = communication.executeCommand(command=command, shell=shell, sleepTime=2.0)
        else:
            raiseNotImplementedError(vendor=vendor)

        communication.closeConnection()
        return {}

    def getCommands(self, vendor: str):
        if vendor == 'cisco':
            return self.ciscoRouterCommands
        elif vendor == 'mikrotik':
            return self.mikrotikRouterCommands

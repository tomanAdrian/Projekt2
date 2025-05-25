from src.commands.vlan.VlanCommands import Vlan
from src.commands.BaseCommands import BaseCommands
from src.model.VlanModel import AcceptVlanModel, TrunkModeModel, CreateVlanModel


class Switch(BaseCommands, Vlan):
    def createBridge(self, name: str):
        pass

    def getVersion(self) -> [dict[str, any]]:
        pass

    def getConfig(self, enablePassword=None) -> [dict[str, any]]:
        pass

    def saveConfig(self, enablePassword=None) -> [dict[str, any]]:
        pass

    def deleteVlan(self, vlanId: int, enablePassword: str = None):
        pass

    def createVlan(self, body: CreateVlanModel, enablePassword='') -> [dict[str, any]]:
        pass

    def trunkMode(self, body: TrunkModeModel, enablePassword='') -> [dict[str, any]]:
        pass

    def acceptVlan(self, body: AcceptVlanModel, enablePassword='') -> [dict[str, any]]:
        pass

    def showVlan(self) -> [dict[str, any]]:
        pass

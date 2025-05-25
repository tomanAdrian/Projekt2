from abc import ABC, abstractmethod
from src.model.VlanModel import AcceptVlanModel, TrunkModeModel, CreateVlanModel


class Vlan(ABC):

    @abstractmethod
    def deleteVlan(self, vlanId: int, enablePassword: str = None):
        pass

    @abstractmethod
    def createVlan(self, body: CreateVlanModel, enablePassword: str = '') -> [dict[str, any]]:
        pass

    @abstractmethod
    def createBridge(self, name: str):
        pass

    @abstractmethod
    def showVlan(self) -> [dict[str, any]]:
        pass

    @abstractmethod
    def acceptVlan(self, body: AcceptVlanModel, enablePassword: str = '') -> [dict[str, any]]:
        pass

    @abstractmethod
    def trunkMode(self, body: TrunkModeModel, enablePassword: str = '') -> [dict[str, any]]:
        pass

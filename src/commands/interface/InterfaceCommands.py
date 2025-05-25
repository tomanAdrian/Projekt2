from abc import ABC, abstractmethod
from src.model.InterfaceModel import InterfaceIpModel


class Interface(ABC):
    @abstractmethod
    def getInterface(self, interface) -> dict[str, any]:
        pass

    @abstractmethod
    def getInterfacesBrief(self) -> dict[str, any]:
        pass

    @abstractmethod
    def showProtocols(self) -> dict[str, any]:
        pass

    @abstractmethod
    def setInterfaceStatus(self, interface: str, enabled: bool, enablePass: str = None) -> dict[str, any]:
        pass

    @abstractmethod
    def setIpaddress(self, body: InterfaceIpModel, enablePassword: str = '') -> [dict[str, any]]:
        pass

    @abstractmethod
    def deleteIpaddress(self, body: InterfaceIpModel, enablePassword: str = '') -> [dict[str, any]]:
        pass

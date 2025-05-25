from abc import ABC, abstractmethod
from src.model.NatModel import SNATModel, PATModel, PortRedirectionModel, DNATModel, LocationModel


class Nat(ABC):

    @abstractmethod
    def getPortForward(self, enablePassword: str = None) -> [dict[str, any]]:
        pass

    @abstractmethod
    def getPAT(self, enablePassword: str = None) -> [dict[str, any]]:
        pass

    @abstractmethod
    def getSNAT(self, enablePassword: str = None) -> [dict[str, any]]:
        pass

    @abstractmethod
    def getDNAT(self, enablePassword: str = None) -> [dict[str, any]]:
        pass

    @abstractmethod
    def setSNAT(self, body: SNATModel, enablePassword: str = ''):
        pass

    @abstractmethod
    def setPAT(self, body: PATModel, enablePassword: str = ''):
        pass

    @abstractmethod
    def setPortRedirection(self, body: PortRedirectionModel, enablePassword: str = ''):
        pass

    @abstractmethod
    def setDNAT(self, body: DNATModel, enablePassword: str = ''):
        pass

    @abstractmethod
    def setLocation(self, location: LocationModel, enablePassword: str = ''):
        pass

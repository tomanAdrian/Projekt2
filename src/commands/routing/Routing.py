from abc import ABC, abstractmethod
from src.model.RoutingModel import OSPFModel, AddOSPFNetworkModel


class Routing(ABC):
    @abstractmethod
    def getRoutingTable(self) -> [dict[str, any]]:
        pass

    @abstractmethod
    def setStaticRoute(self, network: str, networkMask: str, nextHop: str = None, nextHopInterface: str = None, distance: int = None, enablePassword: str = None) -> [dict[str, any]]:
        pass

    @abstractmethod
    def setOspf(self, body: OSPFModel, enablePassword: str = '') -> [dict[str, any]]:
        pass

    @abstractmethod
    def getOspf(self, enablePassword: str = None) -> [dict[str, any]]:
        pass

    @abstractmethod
    def deleteOspf(self, identifier: str, enablePassword: str = None) -> [dict[str, any]]:
        pass

    @abstractmethod
    def addOspfNetwork(self, identifier: str, network: AddOSPFNetworkModel, enablePassword: str = ''):
        pass

    @abstractmethod
    def deleteOspfNetwork(self, identifier: str, network: AddOSPFNetworkModel, enablePassword: str = ''):
        pass

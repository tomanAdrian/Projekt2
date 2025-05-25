from abc import ABC, abstractmethod
from src.model.DhcpModel import DhcpModel, DhcpRemoveModel


class DHCP(ABC):
    @abstractmethod
    def dhcpParameters(self, enablePassword: str = None) -> [dict[str, any]]:
        pass

    @abstractmethod
    def dhcpLeasedAddresses(self) -> [dict[str, any]]:
        pass

    @abstractmethod
    def dhcpCreate(self, body: DhcpModel, enablePassword: str = '') -> [dict[str, any]]:
        pass

    @abstractmethod
    def dhcpRemove(self, poolName: str, body: DhcpRemoveModel = None, enablePassword: str = None) -> [dict[str, any]]:
        pass

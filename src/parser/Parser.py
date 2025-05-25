from abc import ABC, abstractmethod

from src.model.DhcpModel import DhcpStatusModel, DhcpLeasedAddressModel
from src.model.InterfaceModel import InterfaceShort
from src.model.RoutingModel import RoutingTableModel, OSPFModelResponse
from src.model.VlanModel import VlanModel
from src.model.DeviceModel import VersionModel
from src.model.NatModel import SNATModel, DNATModel, PATModel, PortRedirectionModel


class Parser(ABC):
    @abstractmethod
    def prepareOutput(self, pOutput, delUpperLines: int, delBellowLines: int):
        pass

    @abstractmethod
    def parseInterfaceBrief(self, pOutput) -> [InterfaceShort]:
        pass

    @abstractmethod
    def parseShowProtocols(self, pOutput, interfaces: [InterfaceShort]) -> [InterfaceShort]:
        pass

    @abstractmethod
    def parseGetInterfaceDetail(self, pOutput):
        pass

    @abstractmethod
    def parseRoutingTable(self, output) -> RoutingTableModel:
        pass

    @abstractmethod
    def parseDhcpParams(self, runningConfig) -> [DhcpStatusModel]:
        pass

    @abstractmethod
    def parseLeasedAddresses(self, leasedAddresses) -> [DhcpLeasedAddressModel]:
        pass

    @abstractmethod
    def parseOspf(self, config) -> OSPFModelResponse:
        pass

    @abstractmethod
    def parseVlan(self, iVlan) -> [VlanModel]:
        pass

    @abstractmethod
    def parseVersion(self, iVersion) -> VersionModel:
        pass

    @abstractmethod
    def parseSNAT(self, nats) -> [SNATModel]:
        pass

    @abstractmethod
    def parseDNAT(self, nats) -> [DNATModel]:
        pass

    @abstractmethod
    def parsePAT(self, nats) -> [PATModel]:
        pass

    @abstractmethod
    def parsePortForward(self, nats) -> [PortRedirectionModel]:
        pass

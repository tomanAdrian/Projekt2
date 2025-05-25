from src.commands.routing.Routing import Routing
from src.commands.interface.InterfaceCommands import Interface
from src.commands.dhcp.DhcpCommands import DHCP
from src.commands.BaseCommands import BaseCommands
from src.commands.nat.NatCommands import Nat
from src.model.InterfaceModel import InterfaceIpModel
from src.model.NatModel import SNATModel, DNATModel, PortRedirectionModel, PATModel, LocationModel
from src.model.RoutingModel import OSPFModel, AddOSPFNetworkModel
from src.model.DhcpModel import DhcpModel


class Router(BaseCommands, Routing, Interface, DHCP, Nat):
    def getPortForward(self, enablePassword=None) -> [dict[str, any]]:
        pass

    def getPAT(self, enablePassword=None) -> [dict[str, any]]:
        pass

    def getDNAT(self, enablePassword=None) -> [dict[str, any]]:
        pass

    def getSNAT(self, enablePassword=None) -> [dict[str, any]]:
        pass

    def getConfig(self, enablePassword=None) -> [dict[str, any]]:
        pass

    def saveConfig(self, enablePassword=None) -> [dict[str, any]]:
        pass

    def deleteIpaddress(self, body: InterfaceIpModel, enablePassword='') -> [dict[str, any]]:
        pass

    def setIpaddress(self, body: InterfaceIpModel, enablePassword='') -> [dict[str, any]]:
        pass

    def deleteOspfNetwork(self, identifier: str, network: AddOSPFNetworkModel, enablePassword=''):
        pass

    def addOspfNetwork(self, identifier: str, network: AddOSPFNetworkModel, enablePassword=''):
        pass

    def deleteOspf(self, identifier: str, enablePassword: str = None) -> [dict[str, any]]:
        pass

    def getOspf(self, enablePassword: str = None) -> [dict[str, any]]:
        pass

    def setOspf(self, body: OSPFModel, enablePassword='') -> [dict[str, any]]:
        pass

    def setLocation(self, location: LocationModel, enablePassword='') -> [dict[str, any]]:
        pass

    def setPAT(self, body: PATModel, enablePassword='') -> [dict[str, any]]:
        pass

    def setPortRedirection(self, body: PortRedirectionModel, enablePassword='') -> [dict[str, any]]:
        pass

    def setDNAT(self, body: DNATModel, enablePassword='') -> [dict[str, any]]:
        pass

    def setSNAT(self, body: SNATModel, enablePassword='') -> [dict[str, any]]:
        pass

    def dhcpRemove(self, poolName: str, body=None, enablePassword: str = None) -> [dict[str, any]]:
        pass

    def dhcpCreate(self, body: DhcpModel, enablePassword='') -> [dict[str, any]]:
        pass

    def dhcpLeasedAddresses(self) -> [dict[str, any]]:
        pass

    def dhcpParameters(self, enablePassword=None) -> [dict[str, any]]:
        pass

    def setStaticRoute(self, network: str, networkMask: str, nextHop: str = None, nextHopInterface: str = None, distance: int = None, enablePassword: str = None) -> [dict[str, any]]:
        pass

    def setInterfaceStatus(self, interface: str, enabled: bool, enablePass: str = None) -> [dict[str, any]]:
        pass

    def getVersion(self) -> [dict[str, any]]:
        pass

    def getRoutingTable(self) -> [dict[str, any]]:
        pass

    def getInterface(self, interface) -> [dict[str, any]]:
        pass

    def getInterfacesBrief(self) -> [dict[str, any]]:
        pass

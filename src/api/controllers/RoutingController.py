import time

from src.commands.routing.Routing import Routing
from src.model.RoutingModel import StaticRouteModel, OSPFModel, AddOSPFNetworkModel,CiscoAddOspfNetworkModel, CiscoOspfModel, CiscoStaticRouteModel, MikrotikOspfModel
from src.core.config import TypeOfConnection, Vendors
from src.api.controllers.Controller import Controller


def validateStaticRouteBody(body: StaticRouteModel, vendor: str):
    if vendor == Vendors.CISCO:
        CiscoStaticRouteModel.parse_obj(body)


def validateOspfBody(body: OSPFModel, vendor: str):
    if vendor == Vendors.CISCO:
        CiscoOspfModel.parse_obj(body)
    elif vendor == Vendors.MIKROTIK:
        MikrotikOspfModel.parse_obj(body)


def validateAddOspfNetworkBody(body: AddOSPFNetworkModel, vendor: str):
    if vendor == Vendors.CISCO:
        CiscoAddOspfNetworkModel.parse_obj(body)


class RoutingController(Controller):

    def __init__(self):
        super().__init__()

    def getRoutingTable(self, host: str, user: str, password: str, vendor: str, port: int,
                        connection: TypeOfConnection):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.getRoutingTable():
            routingTable = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return parser.parseRoutingTable(routingTable)

    def postStaticRoute(self, host: str, user: str, password: str, vendor: str, port: int, route: StaticRouteModel,
                        connection: TypeOfConnection, enablePassword: str):
        validateStaticRouteBody(route, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.setStaticRoute(network=route.network, networkMask=route.networkMask,
                                               nextHop=route.nextHop, nextHopInterface=route.nextHopInterface,
                                               distance=route.distance, enablePassword=enablePassword):
            console = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()

    def setOspf(self, host: str, user: str, password: str, vendor: str, port: int, body: OSPFModel,
                connection: TypeOfConnection, enablePassword: str):
        validateOspfBody(body, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.setOspf(body=body, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()

    def getOspf(self, host: str, user: str, password: str, vendor: str, port: int, enablePassword: str,
                connection: TypeOfConnection):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.getOspf(enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell, sleepTime=3.0)

        communication.closeConnection()
        ospf = parser.parseOspf(output)

        return ospf

    def deleteOspf(self, host: str, user: str, password: str, vendor: str, port: int, enablePassword: str,
                   identifier: str, connection: TypeOfConnection):
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.deleteOspf(identifier=identifier, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return

    def addOspfNetwork(self, host: str, user: str, password: str, vendor: str, port: int, identifier: str,
                       network: AddOSPFNetworkModel, connection: TypeOfConnection, enablePassword: str):
        validateAddOspfNetworkBody(network, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.addOspfNetwork(identifier=identifier, network=network, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return

    def deleteOspfNetwork(self, host: str, user: str, password: str, vendor: str, port: int, identifier: str,
                          network: AddOSPFNetworkModel, connection: TypeOfConnection, enablePassword: str):
        validateAddOspfNetworkBody(network, vendor)
        communication, shell, parser = self.init(host, user, password, vendor, port, connection)
        commands = self.getCommands(vendor)

        for command in commands.deleteOspfNetwork(identifier=identifier, network=network, enablePassword=enablePassword):
            output = communication.executeCommand(command=command, shell=shell)

        communication.closeConnection()
        return

    def getCommands(self, vendor: str) -> Routing:
        if vendor == 'cisco':
            return self.ciscoRouterCommands
        elif vendor == 'mikrotik':
            return self.mikrotikRouterCommands

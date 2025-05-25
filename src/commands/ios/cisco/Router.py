from src.commands.device.Router import Router
from src.commands.conf_commands.CiscoCommands import commands
from src.api.validators.Validators import TypeOfValidation
from src.model.InterfaceModel import InterfaceIpModel
from src.model.NatModel import SNATModel, PATModel, DNATModel, PortRedirectionModel, LocationModel, Location
from src.model.RoutingModel import OSPFModel, AddOSPFNetworkModel
from src.model.DhcpModel import DhcpModel, DhcpRemoveModel
from ipaddress import IPv4Address


class CiscoRouter(Router):
    def __init__(self):
        self.vendor: str = 'cisco'

    def getRoutingTable(self) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['terminalLength']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['showCommands']['routingTable']}\n",
                'validation': TypeOfValidation.OUTPUT
            }
        ]

    def getInterface(self, interface) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['showCommands']['interfaceDetail']} {interface}\n",
                'validation': TypeOfValidation.PORT
            }
        ]

    def getInterfacesBrief(self) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['showCommands']['interfacesBrief']}\n",
                'validation': TypeOfValidation.OUTPUT
            }
        ]

    def showProtocols(self) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['terminalLength']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['showCommands']['showProtocols']}\n",
                'validation': TypeOfValidation.OUTPUT
            }
        ]

    def setInterfaceStatus(self, interface: str, enabled: bool, enablePass: str = None) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePass}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['configureInterface'].format(interface=interface)}\n",
                'validation': TypeOfValidation.PORT
            },
            {
                'command': f"{commands['enableInterface'] if enabled else commands['disableInterface']}\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    # TODO: add validation that there is allowed only L3 route without interface
    def setStaticRoute(self, network: str, networkMask: str, nextHop: str = None, nextHopInterface: str = None, distance: int = None, enablePassword: str = None) -> [dict[str, any]]:
        staticRouteCommand: str
        if nextHop is not None and nextHopInterface is not None:
            staticRouteCommand = commands['setStaticRouteIpPort'].format(network=network, networkMask=networkMask, nextHop=nextHop, nextHopInterface=nextHopInterface)
        else:
            if nextHop is None:
                staticRouteCommand = commands['setStaticRoute'].format(network=network, networkMask=networkMask, nextHop=nextHopInterface)
            else:
                staticRouteCommand = commands['setStaticRoute'].format(network=network, networkMask=networkMask, nextHop=nextHop)

        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{staticRouteCommand}\n",
                'validation': TypeOfValidation.PORT
            }
        ]

    def dhcpParameters(self, enablePassword=None) -> [dict[str, any]]:
        return self.getConfig(enablePassword=enablePassword)

    def dhcpLeasedAddresses(self) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['showCommands']['dhcpLeasedAddresses']}\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    def dhcpCreate(self, body: DhcpModel, enablePassword='') -> [dict[str, any]]:
        c: [str] = [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            }
        ]
        if body.excludedAddresses is not None:
            c.append(
                {
                    'command': commands['dhcp']['excluded-addresses'].format(start=body.excludedAddresses.start, end=body.excludedAddresses.end) + '\n',
                    'validation': TypeOfValidation.NONE
                }
            )
        c.append(
            {
                'command': commands['dhcp']['createDHCP'].format(poolName=body.poolName) + '\n',
                'validation': TypeOfValidation.NONE
            }
        )
        c.append(
            {
                'command': commands['dhcp']['network'].format(network=body.network, mask=body.mask) + '\n',
                'validation': TypeOfValidation.NONE
            }
        )
        if body.defaultRouter is not None:
            c.append(
                {
                    'command': commands['dhcp']['default-gateway'].format(defaultGateway=body.defaultRouter) + '\n',
                    'validation': TypeOfValidation.NONE
                }
            )
        if body.dnsServer is not None:
            c.append(
                {
                    'command': commands['dhcp']['dns-server'].format(dnsServer=body.dnsServer) + '\n',
                    'validation': TypeOfValidation.NONE
                }
            )
        if body.domainName is not None:
            c.append(
                {
                    'command': commands['dhcp']['domain-name'].format(domainName=body.domainName) + '\n',
                    'validation': TypeOfValidation.NONE
                }
            )
        return c

    def dhcpRemove(self, poolName: str, body: DhcpRemoveModel=None, enablePassword: str = None) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': commands['dhcp']['remove'].format(poolName=poolName) + '\n',
                'validation': TypeOfValidation.DHCP_REMOVE
            }
        ]

    def setSNAT(self, body: SNATModel, enablePassword='') -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['nat']['snat'].format(iAddress=body.iAddress, oAddress=body.oAddress)}\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    def setPAT(self, body: PATModel, enablePassword='') -> [dict[str, any]]:
        o: [dict[str, any]] = [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            }
        ]

        for network in body.acceptedAddresses:
            o.append({
                'command': f"{commands['nat']['natAcl'].format(aclId=body.aclId, address=network.network, mask=str(IPv4Address(int(network.mask) ^ (2 ** 32 - 1))))}\n",
                'validation': TypeOfValidation.NONE
            })

        o.append({
                'command': f"{commands['nat']['pat'].format(aclId=body.aclId, interface=body.oInterface)}",
                'validation': TypeOfValidation.PORT
            })

        return o

    def setDNAT(self, body: DNATModel, enablePassword='') -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['nat']['natPool'].format(poolName=body.poolName, start=body.outside.start, end=body.outside.end, mask=body.outside.mask)}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['nat']['natAcl'].format(aclId=body.aclId, address=body.inside.address, mask=str(IPv4Address(int(body.inside.mask) ^ (2 ** 32 - 1))))}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['nat']['dNat'].format(aclId=body.aclId, poolName=body.poolName)}\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    def setPortRedirection(self, body: PortRedirectionModel, enablePassword='') -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['nat']['pForward'].format(protocol=body.protocol, iAddress=body.inside.address, iPort=body.inside.port, oAddress=body.outside.address, oPort=body.outside.port)}\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    def setLocation(self, location: LocationModel, enablePassword='') -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['configureInterface'].format(interface=location.interface)}\n",
                'validation': TypeOfValidation.PORT
            },
            {
                'command': f"{commands['nat']['iLocation']}\n" if location.location == Location.INSIDE else f"{commands['nat']['oLocation']}\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    def setOspf(self, body: OSPFModel, enablePassword='') -> [dict[str, any]]:
        c: [dict[str, any]] = [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['ospf']['confOspf'].format(processId=body.processId)}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['ospf']['routerId'].format(routerId=body.routerId)}\n",
                'validation': TypeOfValidation.NONE
            }
        ]
        for network in body.networks:
            c.append(
                {
                    'command': f"{commands['ospf']['network'].format(address=network.network, wildcard=str(IPv4Address(int(network.mask)^(2**32-1))), area=network.area)}\n",
                    'validation': TypeOfValidation.NONE
                }
            )

        if body.passiveInterfaces is not None:
            for passInt in body.passiveInterfaces:
                c.append(
                    {
                        'command': f"{commands['ospf']['passiveInterface'].format(interface=passInt)}\n",
                        'validation': TypeOfValidation.PORT
                    }
                )
        if body.shareStatic:
            c.append(
                {
                    'command': f"{commands['ospf']['sendStatic']}\n",
                    'validation': TypeOfValidation.NONE
                }
            )
        if body.internetRoute:
            c.append(
                {
                    'command': f"{commands['ospf']['internetRoute']}\n",
                    'validation': TypeOfValidation.NONE
                }
            )
        return c

    def getOspf(self, enablePassword: str = None) -> [dict[str, any]]:
        return self.getConfig(enablePassword=enablePassword)

    def deleteOspf(self, identifier: str, enablePassword: str = None) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['ospf']['deleteOspf'].format(identifier=identifier)}\n",
                'validation': TypeOfValidation.OSPF_DELETION
            }
        ]

    def addOspfNetwork(self, identifier: str, network: AddOSPFNetworkModel, enablePassword=''):
        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['ospf']['confOspf'].format(processId=identifier)}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['ospf']['network'].format(address=network.network, wildcard=str(IPv4Address(int(network.mask) ^ (2 ** 32 - 1))), area=network.area)}\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    def deleteOspfNetwork(self, identifier: str, network: AddOSPFNetworkModel, enablePassword=''):
        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['ospf']['confOspf'].format(processId=identifier)}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['ospf']['deleteNetwork'].format(address=network.network, wildcard=str(IPv4Address(int(network.mask) ^ (2 ** 32 - 1))), area=network.area)}\n",
                'validation': TypeOfValidation.OSPF_DELETION
            }
        ]

    def setIpaddress(self, body: InterfaceIpModel, enablePassword='') -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['configureInterface'].format(interface=body.interface)}\n",
                'validation': TypeOfValidation.PORT
            },
            {
                'command': f"{commands['setIpAddress'].format(address=body.address, mask=body.mask)}\n",
                'validation': TypeOfValidation.IP_ADD
            }
        ]

    def deleteIpaddress(self, body: InterfaceIpModel, enablePassword='') -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['confMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['configureInterface'].format(interface=body.interface)}\n",
                'validation': TypeOfValidation.PORT
            },
            {
                'command': f"{commands['deleteIpAddress'].format(address=body.address, mask=body.mask)}\n",
                'validation': TypeOfValidation.IP_DELETION
            }
        ]

    def getConfig(self, enablePassword=None) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['terminalLength']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['showCommands']['runningConfig']}\n",
                'validation': TypeOfValidation.OUTPUT
            }
        ]

    def getVersion(self) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['showCommands']['version']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['showCommands']['memory']}\n",
                'validation': TypeOfValidation.OUTPUT
            }
        ]

    def saveConfig(self, enablePassword=None) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['execMode']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{enablePassword}\n",
                'validation': TypeOfValidation.ENABLE
            },
            {
                'command': f"{commands['saveConfiguration']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"\n",
                'validation': TypeOfValidation.NONE
            }
            ,
            {
                'command': f"\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    def getSNAT(self, enablePassword=None) -> [dict[str, any]]:
        return self.getConfig(enablePassword=enablePassword)

    def getDNAT(self, enablePassword=None) -> [dict[str, any]]:
        return self.getConfig(enablePassword=enablePassword)

    def getPAT(self, enablePassword=None) -> [dict[str, any]]:
        return self.getConfig(enablePassword=enablePassword)

    def getPortForward(self, enablePassword=None) -> [dict[str, any]]:
        return self.getConfig(enablePassword=enablePassword)

    def getVendor(self) -> str:
        return self.vendor

from src.commands.device.Router import Router
from src.commands.conf_commands.MikrotikCommands import commands
from src.api.validators.Validators import TypeOfValidation
from src.model.InterfaceModel import InterfaceIpModel
from src.model.NatModel import SNATModel, DNATModel, PATModel, PortRedirectionModel
from src.model.RoutingModel import OSPFModel, AddOSPFNetworkModel
from src.model.DhcpModel import DhcpModel, DhcpRemoveModel
from ipaddress import IPv4Network


class MikrotikRouter(Router):
    def __init__(self):
        self.vendor: str = 'mikrotik'

    def getRoutingTable(self) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['showCommands']['showRoutingTableDetail']}",
                'validation': TypeOfValidation.NONE
            }
        ]

    def getInterface(self, interface) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['showCommands']['interfaceDetail']} {interface}",
                'validation': TypeOfValidation.NONE

            }
        ]

    def getInterfacesBrief(self) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['showCommands']['showInterfacesAppend']}",
                'validation': TypeOfValidation.NONE
            }
        ]

    def showProtocols(self) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['showCommands']['showIpAddressesDetail']}",
                'validation': TypeOfValidation.NONE
            }
        ]

    def setInterfaceStatus(self, interface: str, enabled: bool, enablePass: str = None) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['enableInterface'].format(interface=interface) if enabled else commands['disableInterface'].format(interface=interface)}",
                'validation': TypeOfValidation.PORT
            }
        ]

    def setStaticRoute(self, network: str, networkMask: str, nextHop: str = None, nextHopInterface: str = None,
                       distance: int = None, enablePassword: str = None) -> [dict[str, any]]:
        staticRouteCommand: str = commands['staticRoute']['base'].format(network=network, networkMask=IPv4Network(
            '0.0.0.0/' + str(networkMask)).prefixlen)

        if nextHop is not None and nextHopInterface is not None:
            staticRouteCommand += commands['staticRoute']['fullNextHop'].format(
                                                                         nextHop=nextHop,
                                                                         nextHopInterface=nextHopInterface)
        else:
            if nextHop is None:
                staticRouteCommand += commands['staticRoute']['nextHopInterface'].format(nextHopInterface=nextHopInterface)
            else:
                staticRouteCommand += commands['staticRoute']['nextHop'].format(nextHop=nextHop)

        return [
            {
                'command': f"{staticRouteCommand}",
                'validation': TypeOfValidation.PORT
            }
        ]

    def dhcpParameters(self, enablePassword=None) -> [dict[str, any]]:
        return [
            {
                'command': commands['showCommands']['ipPool'],
                'validation': TypeOfValidation.NONE
            },
            {
                'command': commands['showCommands']['dhcpNetwork'],
                'validation': TypeOfValidation.NONE
            },
            {
                'command': commands['showCommands']['dhcp-server'],
                'validation': TypeOfValidation.NONE
            }
        ]

    def dhcpLeasedAddresses(self) -> [dict[str, any]]:
        return [
            {
                'command': commands['showCommands']['dhcpLease'],
                'validation': TypeOfValidation.NONE
            }
        ]

    def dhcpCreate(self, body: DhcpModel, enablePassword='') -> [dict[str, any]]:
        c: [dict[str, any]] = [
            {
                'command': commands['dhcp']['addPool'].format(poolName=body.poolName, start=body.addressRange.start, end=body.addressRange.end),
                'validation': TypeOfValidation.NONE
            }
        ]
        networkCommand = commands['dhcp']['addNetwork']['network'].format(network=body.network, mask=body.mask)
        if body.defaultRouter is not None:
            networkCommand += commands['dhcp']['addNetwork']['gateway'].format(defaultGateway=body.defaultRouter)
        if body.dnsServer is not None:
            networkCommand += commands['dhcp']['addNetwork']['dns-server'].format(dnsServer=body.dnsServer)
        if body.domainName is not None:
            networkCommand += commands['dhcp']['addNetwork']['domain-name'].format(domainName=body.domainName)
        c.append(
            {
                'command': networkCommand,
                'validation': TypeOfValidation.NONE
            }
        )
        c.append(
            {
                'command': commands['dhcp']['addServer'].format(poolName=body.poolName, interface=body.interface),
                'validation': TypeOfValidation.PORT
            }
        )
        return c

    def dhcpRemove(self, poolName: str, body: DhcpRemoveModel=None, enablePassword: str = None) -> [dict[str, any]]:
        # TODO: can't remove network always by ID 0 --> REFACTOR
        return [
            {
                'command': commands['dhcp']['removePool'].format(poolName=poolName),
                'validation': TypeOfValidation.DHCP_REMOVE
            },
            {
                'command': commands['dhcp']['removeNetwork'].format(network=body.network, mask=IPv4Network(f'0.0.0.0/{body.mask}').prefixlen),
                'validation': TypeOfValidation.DHCP_REMOVE
            },
            {
                'command': commands['dhcp']['removeServer'].format(poolName=poolName),
                'validation': TypeOfValidation.DHCP_REMOVE
            }
        ]

    def setSNAT(self, body: SNATModel, enablePassword='') -> [dict[str, any]]:
        return [
            {
                'command': commands['nat']['dst-nat'].format(oAddress=body.oAddress, iAddress=body.iAddress),
                'validation': TypeOfValidation.NONE
            },
            {
                'command': commands['nat']['src-nat'].format(oAddress=body.oAddress, iAddress=body.iAddress),
                'validation': TypeOfValidation.NONE
            }
        ]

    def setDNAT(self, body: DNATModel, enablePassword='') -> [dict[str, any]]:
        return [
            {
                'command': commands['nat']['dNat'].format(iAddress=body.inside.address, imask=body.inside.mask, oStart=body.outside.start, oEnd=body.outside.end),
                'validation': TypeOfValidation.NONE
            }
        ]

    def setPAT(self, body: PATModel, enablePassword=''):
        return [
            {
                'command': commands['nat']['pat'].format(interface=body.oInterface),
                'validation': TypeOfValidation.PORT
            }
        ]

    def setPortRedirection(self, body: PortRedirectionModel, enablePassword=''):
        return [
            {
                'command': commands['nat']['port-forward'].format(oAddress=body.outside.address, oPort=body.outside.port, protocol=body.protocol, iAddress=body.inside.address, iPort=body.inside.port),
                'validation': TypeOfValidation.NONE
            }
        ]

    def setOspf(self, body: OSPFModel, enablePassword='') -> [dict[str, any]]:
        areas = set(map(lambda x: x.area, body.networks))
        c: [dict[str, any]] = [
            {
                'command': commands['ospf']['createInstance'].format(name=body.name, routerId=body.routerId),
                'validation': TypeOfValidation.OSPF_INSTANCE_CREATION
            }
        ]

        if body.shareStatic:
            c.append({
                'command': commands['ospf']['shareStatic'].format(name=body.name),
                'validation': TypeOfValidation.OSPF_INSTANCE_CREATION
            })

        if body.internetRoute:
            c.append({
                'command': commands['ospf']['internetRoute'].format(name=body.name),
                'validation': TypeOfValidation.OSPF_INSTANCE_CREATION
            })

        for area in areas:
            c.append(
                {
                    'command': commands['ospf']['createArea'].format(area=area, instance=body.name),
                    'validation': TypeOfValidation.NONE
                }
            )

        for network in body.networks:
            c.append(
                {
                    'command': commands['ospf']['addNetwork'].format(network=network.network, mask=IPv4Network('0.0.0.0/'+str(network.mask)).prefixlen, area=network.area),
                    'validation': TypeOfValidation.NONE
                }
            )
        return c

    def getOspf(self, enablePassword: str = None) -> [dict[str, any]]:
        return [
            {
                'command': commands['ospf']['attributes'],
                'validation': TypeOfValidation.NONE
            }
        ]

    def deleteOspf(self, identifier: str, enablePassword: str = None) -> [dict[str, any]]:
        return [
            {
                'command': commands['ospf']['deleteInstance'].format(identifier=identifier),
                'validation': TypeOfValidation.OSPF_DELETION
            },
            {
                'command': commands['ospf']['deleteInactiveAreas'].format(identifier=identifier),
                'validation': TypeOfValidation.NONE
            },
            {
                'command': commands['ospf']['deleteInactiveNetworks'].format(identifier=identifier),
                'validation': TypeOfValidation.NONE
            }
        ]

    def addOspfNetwork(self, identifier: str, network: AddOSPFNetworkModel, enablePassword=''):
        return [
            {
                'command': commands['ospf']['createArea'].format(area=network.area, instance=identifier),
                'validation': TypeOfValidation.OSPF_NETWORK_ADDITION
            },
            {
                'command': commands['ospf']['addNetwork'].format(network=network.network, mask=IPv4Network(
                    '0.0.0.0/' + str(network.mask)).prefixlen, area=network.area),
                'validation': TypeOfValidation.NONE
            }
        ]

    def deleteOspfNetwork(self, identifier: str, network: AddOSPFNetworkModel, enablePassword=''):
        return [
            {
                'command': commands['ospf']['deleteNetwork'].format(network=network.network, mask=IPv4Network(
                    '0.0.0.0/' + str(network.mask)).prefixlen),
                'validation': TypeOfValidation.OSPF_DELETION
            }
        ]

    def setIpaddress(self, body: InterfaceIpModel, enablePassword='') -> [dict[str, any]]:
        return [
            {
                'command': commands['setIpAddress'].format(address=body.address, mask=IPv4Network('0.0.0.0/' + str(body.mask)).netmask, interface=body.interface),
                'validation': TypeOfValidation.IP_ADD
            }
        ]

    def deleteIpaddress(self, body: InterfaceIpModel, enablePassword='') -> [dict[str, any]]:
        return [
            {
                'command': commands['deleteIpAddress'].format(interface=body.interface),
                'validation': TypeOfValidation.IP_DELETION
            }
        ]

    def getConfig(self, enablePassword=None) -> [dict[str, any]]:
        return [
            {
                'command': commands['showCommands']['runningConfiguration'],
                'validation': TypeOfValidation.NONE
            }
        ]
    
    def getVersion(self) -> [dict[str, any]]:
        return [
            {
                'command': commands['showCommands']['version'],
                'validation': TypeOfValidation.NONE
            }
        ]

    def showNat(self) -> [dict[str, any]]:
        return [
            {
                'command': commands['showCommands']['nat'],
                'validation': TypeOfValidation.OUTPUT
            }
        ]

    def getSNAT(self, enablePassword=None) -> [dict[str, any]]:
        return self.showNat()

    def getDNAT(self, enablePassword=None) -> [dict[str, any]]:
        return self.showNat()

    def getPAT(self, enablePassword=None) -> [dict[str, any]]:
        return self.showNat()

    def getPortForward(self, enablePassword=None) -> [dict[str, any]]:
        return self.showNat()

    def getVendor(self) -> str:
        return self.vendor

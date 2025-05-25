import datetime
from ipaddress import IPv4Network

from src.model.DeviceModel import VersionModel
from src.model.InterfaceModel import InterfaceShort, LearnedBy
from src.model.NatModel import SNATModel, DNATModel, PATModel, PortRedirectionModel, InterfaceDNATModel, \
    AddressRangeModel, InterfacePortRedirectionModel
from src.model.RoutingModel import RoutingTableModel, RouteModel, NetworkModel, OSPFModel, OSPFNetworkModel, \
    OSPFModelResponse
from src.model.DhcpModel import DhcpStatusModel, AddressesRangeModel, DhcpLeasedAddressModel
from src.model.VlanModel import VlanModel
from src.parser.Parser import Parser
import re

routeIDs: str = '0123456789'

routeProtocolMappings: dict[str, str] = {
    'c': 'Directly connected',
    's': 'Static',
    'r': 'RIP',
    'm': 'Modem',
    'b': 'BGP',
    'd': 'DHCP',
    'o': 'OSPF'
}


class MikrotikParser(Parser):

    def parsePortForward(self, nats) -> [PortRedirectionModel]:
        portForward: [PortRedirectionModel] = []
        nats = self.prepareOutput(nats, 0, 0)
        nats = list(map(lambda x: x.strip().lstrip(routeIDs).strip(), nats))
        nats = list(filter(None, nats))

        pf_reg = re.compile(r'chain=dstnat action=dst-nat to-addresses=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) to-ports=\d+ protocol=([a-z]){3} dst-address=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) dst-port=\d+')
        pf = list(filter(lambda x: pf_reg.match(x) is not None, nats))
        for n in pf:
            protocol: str = parseParameter(n, 'protocol')
            inside: InterfacePortRedirectionModel = InterfacePortRedirectionModel(address=parseParameter(n, 'to-addresses'),
                                                                                  port=parseParameter(n, 'to-ports'))
            outside: InterfacePortRedirectionModel = InterfacePortRedirectionModel(
                address=parseParameter(n, 'dst-address'),
                port=parseParameter(n, 'dst-port'))
            portForward.append(PortRedirectionModel(
                protocol=protocol,
                inside=inside,
                outside=outside
            ))
        return portForward

    def parsePAT(self, nats) -> [PATModel]:
        pat: [PATModel] = []
        nats = self.prepareOutput(nats, 0, 0)
        nats = list(map(lambda x: x.strip().lstrip(routeIDs).strip(), nats))
        nats = list(filter(None, nats))

        pat_reg = re.compile(r'chain=srcnat action=masquerade out-interface=')
        pn: [str] = list(filter(lambda x: pat_reg.match(x) is not None, nats))
        for n in pn:
            aclId: str = '0'
            acceptedAddresses: [NetworkModel] = []
            oInterface: str = parseInterface(n, 0)
            pat.append(PATModel(
                aclId=aclId,
                acceptedAddresses=acceptedAddresses,
                oInterface=oInterface
            ))
        return pat

    def parseDNAT(self, nats) -> [DNATModel]:
        dnat: [DNATModel] = []
        nats = self.prepareOutput(nats, 0, 0)
        nats = list(map(lambda x: x.strip().lstrip(routeIDs).strip(), nats))
        nats = list(filter(None, nats))

        dnat_reg = re.compile(r'chain=srcnat action=src-nat to-addresses=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) src-address=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/\d+')
        dn: [str] = list(filter(lambda x: dnat_reg.match(x) is not None, nats))
        for d in dn:
            poolName: str = ''
            aclId: int = 0
            inside: InterfaceDNATModel = InterfaceDNATModel(address=parseNetwork(d, 2),
                                                            mask=str(IPv4Network('0.0.0.0/' + parseNetworkWithMask(d, 0).split('/')[1]).netmask))
            outside: AddressRangeModel = AddressRangeModel(start=parseNetwork(d, 0),
                                                           end=parseNetwork(d, 1),
                                                           mask='255.255.255.255')
            dnat.append(DNATModel(
                poolName=poolName,
                aclId=aclId,
                inside=inside,
                outside=outside
            ))
        return dnat

    def parseSNAT(self, nats) -> [SNATModel]:
        snat: [SNATModel] = []
        nats = self.prepareOutput(nats, 0, 0)
        nats = list(map(lambda x: x.strip().lstrip(routeIDs).strip(), nats))
        nats = list(filter(None, nats))


        snat_reg = re.compile(r'chain=dstnat action=dst-nat to-addresses=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) dst-address=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        sn: [str] = list(filter(lambda x: snat_reg.match(x) is not None, nats))
        for s in sn:
            snat.append(SNATModel(
                iAddress=parseNetwork(s, 0),
                oAddress=parseNetwork(s, 1)
            ))
        return snat

    def parseVersion(self, iVersion) -> VersionModel:
        iVersion = self.prepareOutput(iVersion, 0, 0)
        iVersion = list(filter(None, iVersion))
        iVersion = list(map(lambda x: x.strip(), iVersion))

        fVersion: [str] = list(filter(lambda x: x.find('version:') != -1, iVersion))
        fMemoryFree: [str] = list(filter(lambda x: x.find('free-memory:') != -1, iVersion))
        fMemoryTotal: [str] = list(filter(lambda x: x.find('total-memory:') != -1, iVersion))

        version: str = fVersion[0].split(': ')[1]
        freeMemory: str = fMemoryFree[0].split(': ')[1]
        totalMemory: str = fMemoryTotal[0].split(': ')[1]
        return VersionModel(version=version, freeMemory=freeMemory, totalMemory=totalMemory)

    def prepareOutput(self, pOutput, delUpperLines: int, delBellowLines: int):
        pOutput = re.sub(' +', ' ', pOutput)
        pOutput = pOutput.split('\r\n')
        for i in range(delUpperLines):
            pOutput.pop(0)
        for i in range(delBellowLines):
            pOutput.pop(len(pOutput) - 1)
        return pOutput

    def parseInterfaceBrief(self, pOutput) -> [InterfaceShort]:
        pOutput = self.prepareOutput(pOutput, 0, 0)
        lInterfaces: [str] = list(filter(lambda x: parseInterface(x, 0) != '', pOutput))
        interfaces = []
        for line in lInterfaces:
            interfaces.append(InterfaceShort(
                interface=parseInterface(line, 0),
                enabled=True if line.find(' R ') != -1 else False
            ))
        return interfaces

    def parseShowProtocols(self, pOutput, interfaces: [InterfaceShort]) -> [InterfaceShort]:
        pOutput = self.prepareOutput(pOutput, 0, 0)
        linesWithIp: [str] = list(filter(lambda x: parseNetwork(x, 0) != '', pOutput))

        for line in linesWithIp:
            inter: str = parseInterface(line, 0)
            netMask: str = parseNetworkWithMask(line, 0)
            learnedBy: str = LearnedBy.DYNAMIC.name if line.find(' D ') != -1 else LearnedBy.STATIC.name
            for interface in interfaces:
                if inter == interface.interface:
                    interface.ipaddress = parseNetwork(netMask, 0)
                    interface.mask = str(IPv4Network('0.0.0.0/' + netMask.split('/')[1].strip()).netmask)
                    interface.learnedBy = learnedBy
                    break
                # interfaceName = (attributes[4] if len(attributes) == 6 else attributes[5]).split('=')[1]
                # if interfaceName == interface.interface:
                #     ipAddress = (attributes[2] if len(attributes) == 6 else attributes[3]).split('=')[1]
                #     mask = str(IPv4Network('0.0.0.0/' + ipAddress.split('/')[1].strip()).netmask)
                #     ipAddress = ipAddress.split('/')[0]
                #     learnedBy = LearnedBy.DYNAMIC.name if (
                #             len(attributes) == 7 and attributes[2] == 'D') else LearnedBy.STATIC.name
                #     interface.ipaddress = ipAddress
                #     interface.mask = mask
                #     interface.learnedBy = learnedBy
                #     break
        return interfaces

    def parseGetInterfaceDetail(self, pOutput):
        pass

    def parseRoutingTable(self, input) -> RoutingTableModel:
        input = self.prepareOutput(input, 0, 0)
        input = list(filter(lambda x: parseNetwork(x, 0) != '', input))
        input = list(filter(None, input))
        input = list(map(lambda x: x.strip(), input))
        input = list(map(lambda x: x.lstrip(routeIDs).strip(), input))
        input = list(filter(lambda x: x.find('] >') == -1, input))
        rt: RoutingTableModel = RoutingTableModel()

        # check if there is set default route
        defaultGateWay = list(filter(lambda x: x.find('0.0.0.0/0'), input))
        if len(defaultGateWay) > 0:
            rt.defaultGateway = parseNetwork(defaultGateWay[0], 1)

        networks = list(filter(lambda x: x.find('0.0.0.0/0') == -1, input))
        for n in networks:
            network: str = parseNetwork(n, 0)
            address: str = parseDestinationAddress(n)
            gw: str = parseGateWay(n)
            learned: str = n.split(' ')[0]
            for key in routeProtocolMappings.keys():
                if learned.find(key) != -1:
                    learned = routeProtocolMappings.get(key)
                    break
            rt.networks.append(NetworkModel(
                network=network,
                mask=str(IPv4Network('0.0.0.0/' + address.split('/')[1].strip()).netmask),
                interface=parseInterface(gw, 0),
                nextHop=parseNetwork(gw, 0),
                learned=learned
            ))
        return rt

    def parseDhcpParams(self, input) -> [DhcpStatusModel]:
        # preparation
        dhcp: [DhcpStatusModel] = []
        input = self.prepareOutput(input, 0, 0)
        input = list(filter(None, input))
        input = list(filter(lambda x: x.find('] >') == -1, input))
        input = list(map(lambda x: x.strip(), input))
        input = list(filter(lambda x: parseNetwork(x, 0) != '' or parseInterface(x, 0) != '', input))

        # merging by pool
        pools: [[str]] = [[] * (len(input) % 3)]
        for pool in input:
            if int(pool[0]) >= len(pools):
                pools.insert(int(pool[0]), [])
            pools[int(pool[0])].append(pool)

        for pool in pools:
            if len(pool) != 3:
                break
            poolName: str = getValueFromLine(pool[2], 'name')
            network: str = getValueFromLine(pool[1], 'address')
            gateway: str = getValueFromLine(pool[1], 'gateway')
            dnsServer: str = getValueFromLine(pool[1], 'dns-server')
            domain: str = getValueFromLine(pool[1], 'domain')
            interface: str = getValueFromLine(pool[2], 'interface')
            dhcp.append(DhcpStatusModel(
                poolName=poolName,
                network=network.split('/')[0],
                mask=str(IPv4Network('0.0.0.0/' + network.split('/')[1]).netmask),
                defaultRouter=gateway,
                dnsServer=dnsServer,
                domainName=domain,
                interface=interface,
                addressRange=AddressesRangeModel
                    (
                    start=parseNetwork(pool[0], 0),
                    end=parseNetwork(pool[0], 1)
                )
            ))
        return dhcp

    def parseLeasedAddresses(self, leasedAddresses) -> [DhcpLeasedAddressModel]:
        leasedAddresses = self.prepareOutput(leasedAddresses, 0, 0)
        leasedAddresses = list(filter(None, leasedAddresses))
        leasedAddresses = groupSplitLines(leasedAddresses)
        leased: [DhcpLeasedAddressModel] = []
        timeStamp = datetime.datetime.now()
        for line in leasedAddresses:
            splitLine = line.split(' ')
            client = splitLine[3].split('=')[1]
            address = splitLine[2].split('=')[1]
            expiration = timeStamp + datetime.timedelta(minutes=int(splitLine[9].split('=')[1].split('m')[0]),
                                                        seconds=int(
                                                            splitLine[9].split('=')[1].split('m')[1].split('s')[0]))
            leased.append(DhcpLeasedAddressModel(
                client=client,
                address=address,
                expiration=str(expiration)
            ))
        return leased

    def parseOspf(self, ospf) -> OSPFModelResponse:
        ospf = self.prepareOutput(ospf, 0, 0)
        ospf = list(filter(None, ospf))

        fInstances: [str] = list(filter(lambda x: x.find('router-id') != -1, ospf))
        fAreas: [str] = list(filter(lambda x: x.find('instance') != -1, ospf))
        fNetworks: [str] = list(filter(lambda x: x.find('networks') != -1, ospf))

        name: str = getValueFromLine(fInstances[0] if len(fInstances) > 0 else '', 'name')
        routerId: str = getValueFromLine(fInstances[0] if len(fInstances) > 0 else '', 'router-id')
        networks = []
        for network in fNetworks:
            networks.append(OSPFNetworkModel(
                network=parseNetwork(network, 1),
                mask=IPv4Network('0.0.0.0/' + parseNetworkWithMask(network, 0).split('/')[1]).netmask,
                area=getValueFromLine(network, 'area')
            ))
        internetRoute: bool = False
        shareStatic: bool = False
        if len(fInstances) > 0:
            internetRoute = True if fInstances[0].find('originate-default') != -1 else False
            shareStatic = True if fInstances[0].find('redistribute') != -1 else False

        return OSPFModelResponse(
            name=name,
            routerId=routerId,
            networks=networks,
            passiveInterfaces=[],
            internetRoute=internetRoute,
            shareStatic=shareStatic,
        )

    def parseVlan(self, iVlan) -> [VlanModel]:
        vlan: [VlanModel] = []
        iVlan = self.prepareOutput(iVlan, 0, 0)
        iVlan = list(map(lambda x: x.strip().lstrip(routeIDs).strip(), iVlan))
        iVlan = list(filter(None, iVlan))

        ports: [str] = list(filter(lambda x: parseInterface(x, 0) != '', iVlan))
        vIDs: [str] = set(map(lambda x: x.split(' ')[3] if x.split(' ')[0].find('I') == -1 else x.split(' ')[4], ports))
        for vID in vIDs:
            vName: str = ''
            enabled: bool = True
            interfaces: [str] = []
            for interface in ports:
                if interface.split(' ')[3] == vID:
                    interfaces.append(parseInterface(interface, 0))
            vlan.append(VlanModel(
                id=vID,
                name=vName,
                enabled=enabled,
                interfaces=interfaces
            ))
        return vlan


#     function will return value of specified attribute
def getValueFromLine(line: str, keyValue: str) -> str:
    pLine = line.split(' ')
    attribute = list(filter(lambda x: x.find(keyValue) != -1, pLine))
    value = attribute[0].split('=')[1] if len(attribute) > 0 else ''
    return value


# this function will group lines which doesn't have a number in front of it
def groupSplitLines(input):
    output = []
    for lineIndex, inputLine in enumerate(input):
        input[lineIndex] = inputLine.strip()
    for lineIndex, inputLine in enumerate(input):
        line = ''
        if inputLine[0].isnumeric():
            line += inputLine + ' '
            for sameLine in input[lineIndex + 1:]:
                if sameLine[0].isnumeric():
                    break
                line += sameLine + ' '
            output.append(line)
    return output


def groupByEnter(input):
    output = []

    lines = ''
    for line in input:
        if line != '':
            lines += line + ' '
        else:
            output.append(lines)
            lines = ''
    return output


def updateInterface(interface: str):
    return interface.replace('.', '/')


def parseNetwork(line: str, indexOfNetwork: int) -> str:
    reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    ip = reg.findall(line)
    return ip[indexOfNetwork] if len(ip) > indexOfNetwork else ''


def parseNetworkWithMask(line: str, indexOfNetwork: int) -> str:
    reg = re.compile(r'(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}')
    ip = reg.findall(line)
    return ip[indexOfNetwork] if len(ip) > indexOfNetwork else ''


def parseInterface(line: str, indexOfInterface: int) -> str:
    reg_ether = re.compile(r'ether\d+')
    reg_vlan = re.compile(r'vlan\d+')
    reg_wlan = re.compile(r'wlan\d+')
    interfaces = reg_ether.findall(line)
    interfaces += reg_vlan.findall(line)
    interfaces += reg_wlan.findall(line)
    return interfaces[indexOfInterface] if len(interfaces) > indexOfInterface else ''


def parseDestinationAddress(line: str) -> str:
    dAdd: str = list(filter(lambda x: x.find('dst-address') != -1, line.split(' ')))[0]
    return parseNetworkWithMask(dAdd, 0)


def parseGateWay(line: str) -> str:
    gw: str = list(filter(lambda x: x.find('gateway') != -1, line.split(' ')))[0]
    return gw.split('=')[1]

def parseParameter(line: str, keyWord: str) -> str:
    w: str = list(filter(lambda x: x.find(keyWord) != -1, line.split(' ')))[0]
    return w.split('=')[1]

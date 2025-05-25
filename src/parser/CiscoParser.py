import ipaddress

from src.model.DeviceModel import VersionModel
from src.model.InterfaceModel import InterfaceShort, LearnedBy
from src.model.NatModel import SNATModel, DNATModel, InterfaceDNATModel, AddressRangeModel, PATModel, \
    PortRedirectionModel, InterfacePortRedirectionModel
from src.model.RoutingModel import RoutingTableModel, RouteModel, NetworkModel, OSPFModel, OSPFNetworkModel, \
    OSPFModelResponse
from src.model.DhcpModel import DhcpStatusModel, AddressesRangeModel, DhcpLeasedAddressModel
from src.model.VlanModel import VlanModel
from ipaddress import IPv4Network, IPv4Address
from src.parser.Parser import Parser
import re

routeProtocolMappings: dict[str, str] = {
    'C': 'Directly connected',
    'S': 'Static',
    'R': 'RIP',
    'M': 'Mobile',
    'B': 'BGP',
    'D': 'EIGRP',
    'EX': 'External EIGRP',
    'O': 'OSPF'
}


class CiscoParser(Parser):

    def parsePortForward(self, nats) -> [PortRedirectionModel]:
        portForward: [PortRedirectionModel] = []
        config = nats[nats.find('!'):]
        config = self.prepareOutput(config, 0, 0)
        nats = findInRunningConfig(config, 'ip nat', False)
        reg_portForward = re.compile(
            r'ip nat inside source static ([a-z]){3} (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \d+ (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \d+ extendable')
        pf: [str] = list(filter(lambda x: reg_portForward.match(x) is not None, nats[0]))

        for n in pf:
            protocol: str = n.split(' ')[5]
            inside: InterfacePortRedirectionModel = InterfacePortRedirectionModel(address=parseNetwork(n, 0),
                                                                                  port=re.findall(r' \d+ ', n)[0])
            outside: InterfacePortRedirectionModel = InterfacePortRedirectionModel(address=parseNetwork(n, 1),
                                                                                   port=re.findall(r' \d+ ', n)[1])
            portForward.append(PortRedirectionModel(protocol=protocol,
                                                    inside=inside,
                                                    outside=outside))
        return portForward

    def parsePAT(self, nats) -> [PATModel]:
        pat: [PATModel] = []
        config = nats[nats.find('!'):]
        config = self.prepareOutput(config, 0, 0)
        nats = findInRunningConfig(config, 'ip nat', False)
        acls = findInRunningConfig(config, 'access-list', False)

        reg_pat = re.compile(r'ip nat inside source list \d+ interface')
        if len(nats) > 0 and len(acls) > 0:
            for n in nats[0]:
                if reg_pat.match(n):
                    aclId: str = re.findall(r'\d+', n)[0]
                    interface: str = n.split(' ')[7]
                    pat_acls = list(filter(lambda x: x.split(' ')[1] == aclId, acls[0]))
                    acceptedAddresses: [NetworkModel] = []
                    for acl in pat_acls:
                        acceptedAddresses.append(NetworkModel(network=parseNetwork(acl, 0),
                                                              mask=str(IPv4Address(
                                                                  int(IPv4Address(parseNetwork(acl, 1))) ^ (
                                                                          2 ** 32 - 1)))))
                    pat.append(PATModel(aclId=aclId,
                                        acceptedAddresses=acceptedAddresses,
                                        oInterface=interface))
        return pat

    def parseDNAT(self, nats) -> [DNATModel]:
        dnat: [DNATModel] = []
        config = nats[nats.find('!'):]
        config = self.prepareOutput(config, 0, 0)
        nats = findInRunningConfig(config, 'ip nat', False)
        acls = findInRunningConfig(config, 'access-list', False)
        natPools = findInRunningConfig(config, 'ip nat pool', False)

        dn: [str] = []
        reg_dnat = re.compile(r'ip nat inside source list \d+ pool')
        if len(nats) > 0:
            for n in nats[0]:
                if reg_dnat.match(n):
                    poolName: str = n.split(' ')[len(n.split(' ')) - 1]
                    aclId: str = re.findall(r'\d+', n)[0]
                    natPool: str = list(filter(lambda x: x.find(poolName) != -1, natPools[0]))[0]
                    iAddress: str = ''
                    imask: str = ''
                    oStart: str = parseNetwork(natPool, 0)
                    oEnd: str = parseNetwork(natPool, 1)
                    omask: str = parseNetwork(natPool, 2)
                    for acl in acls[0]:
                        if re.compile(r'access-list ' + re.escape(
                                aclId) + r' permit (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})').match(
                            acl):
                            iAddress = parseNetwork(acl, 0)
                            imask = str(IPv4Address(int(IPv4Address(parseNetwork(acl, 1))) ^ (2 ** 32 - 1)))
                    dnat.append(DNATModel(
                        poolName=poolName,
                        aclId=aclId,
                        inside=InterfaceDNATModel(
                            address=iAddress,
                            mask=imask
                        ),
                        outside=AddressRangeModel(
                            start=oStart,
                            end=oEnd,
                            mask=omask
                        )
                    ))
        return dnat

    def parseSNAT(self, nats) -> [SNATModel]:
        snat: [SNATModel] = []
        nats = nats[nats.find('!'):]
        nats = self.prepareOutput(nats, 0, 0)

        nats = findInRunningConfig(nats, 'ip nat', False)
        reg_snat = re.compile(
            r'ip nat inside source static (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        sn: [str] = []
        if len(nats) > 0:
            for s in nats[0]:
                if reg_snat.match(s):
                    snat.append(SNATModel(
                        iAddress=parseNetwork(s, 0),
                        oAddress=parseNetwork(s, 1)
                    ))
        return snat

    def parseVersion(self, iVersion) -> VersionModel:
        iVersion = self.prepareOutput(iVersion, 0, 0)
        fVersionLine: [str] = list(filter(lambda x: x.lower().find(', version') != -1, iVersion))
        fMemoryLine: [str] = list(filter(lambda x: x.lower().find('memory.') != -1, iVersion))

        version: str = list(filter(lambda x: x.lower().find('version') != -1, fVersionLine[0].split(', ')))[0]
        memory: str = list(filter(lambda x: x.lower().find('/') != -1, fMemoryLine[0].split(' ')))[0]
        return VersionModel(version=version.replace('Version ', ''), freeMemory=memory.split('/')[1],
                            totalMemory=memory.split('/')[0])

    def prepareOutput(self, pOutput, delUpperLines: int, delBellowLines: int):
        pOutput = re.sub(' +', ' ', pOutput)
        pOutput = pOutput.split('\r\n')
        for i in range(delUpperLines):
            if len(pOutput) > 0:
                pOutput.pop(0)
        for i in range(delBellowLines):
            if len(pOutput) > 0:
                pOutput.pop(len(pOutput) - 1)
        return pOutput

    def parseInterfaceBrief(self, pOutput) -> [InterfaceShort]:
        pOutput = pOutput[pOutput.find('show ip interface'):]
        pOutput = self.prepareOutput(pOutput, 0, 1)
        lInterfaces: [str] = list(filter(lambda x: parseInterface(x, 0) != '', pOutput))
        interfaces: [InterfaceShort] = []
        for l in lInterfaces:
            interface: str = parseInterface(l, 0)
            ipaddress: str = parseNetwork(l, 0)
            enabled: bool = True if (len(l.split(' ')) == 7) else False
            learnedBy: str = l.split(' ')[3]
            interfaces.append(InterfaceShort(
                interface=interface,
                ipaddress=ipaddress,
                mask='',
                learnedBy=learnedBy,
                enabled=enabled
            ))
        return interfaces

    def parseShowProtocols(self, pOutput, interfaces: [InterfaceShort]) -> [InterfaceShort]:
        pOutput = self.prepareOutput(pOutput, 2, 0)
        for interfaceModel in interfaces:
            for lineIndex, line in enumerate(pOutput):
                if line.find(interfaceModel.interface) != -1 and parseNetwork(pOutput[lineIndex + 1], 0) != '':
                    try:
                        interfaceModel.mask = str(IPv4Network(f"0.0.0.0/{pOutput[lineIndex + 1].split('/')[1]}").netmask)
                    except ipaddress.NetmaskValueError as e:
                        interfaceModel.mask = '0.0.0.0'
            if interfaceModel.mask == '1.1.1.1':
                interfaceModel.mask = 'UNSET'
        return interfaces

    def parseGetInterfaceDetail(self, pOutput):
        pOutput = self.prepareOutput(pOutput, 2, 1)
        inteterface: dict[str, str] = {'interface': (pOutput[0].split(' '))[0]}
        pOutput.pop(0)
        for line in pOutput:
            if ' is ' in line:
                splitted = line.split(' is ')
            elif ' by ' in line:
                splitted = line.split(' by ')
            else:
                splitted = line.split(' are ')

            if len(splitted) == 2:
                inteterface[splitted[0]] = splitted[1]
            else:
                inteterface[splitted[0]] = 'true'
        return inteterface

    def parseRoutingTable(self, output) -> RoutingTableModel:
        rt: RoutingTableModel = RoutingTableModel()
        output = output[output.find('\r\n\r\n'):]
        output = self.prepareOutput(output, 0, 1)
        output = list(filter(None, output))
        output = list(map(lambda x: x.strip(), output))

        # check if there is default route
        defaultGateWay = list(filter(lambda x: x.find('0.0.0.0/0') != -1, output))
        if len(defaultGateWay) > 0:
            rt.defaultGateway = parseNetwork(defaultGateWay[0], 1)
            output.pop(0)
        networks = list(filter(lambda x: not x[0].isnumeric() and x[0] != 'L', output))
        networks = list(filter(None, networks))

        for n in networks:
            network: str = parseNetwork(n, 0)
            interface: str = parseInterface(n, 0)
            address: str = parseNetworkWithMask(n, 0)
            mask: str = str(IPv4Network('0.0.0.0/' + address.split('/')[1].strip()).netmask) if len(
                address.split('/')) > 1 else ''
            nextHop: str = parseNetwork(n, 1)
            learned: str = routeProtocolMappings.get(n[0], 'Unknown')
            rt.networks.append(NetworkModel(
                network=network,
                mask=mask,
                interface=interface,
                nextHop=nextHop,
                learned=learned
            ))
        return rt

    def parseDhcpParams(self, runningConfig) -> [DhcpStatusModel]:
        runningConfig = runningConfig[runningConfig.find('!'):]
        runningConfig = self.prepareOutput(runningConfig, 0, 0)

        params: [DhcpStatusModel] = []
        excludedAddresses = findInRunningConfig(runningConfig, 'ip dhcp excluded-address', False)
        dhcpPools = findInRunningConfig(runningConfig, 'ip dhcp pool')

        eAddresses: [AddressesRangeModel] = []
        if len(excludedAddresses) > 0:
            for address in excludedAddresses[0]:
                eAddresses.append(AddressesRangeModel(
                    start=address.split(' ')[3],
                    end=address.split(' ')[4]
                ))
        for pool in dhcpPools:
            dhModel = DhcpStatusModel()
            poolName = list(filter(lambda param: param.find('ip dhcp pool') != -1, pool))
            network = list(filter(lambda param: param.find('network') != -1, pool))
            default_router = list(filter(lambda param: param.find('default-router') != -1, pool))
            dns_server = list(filter(lambda param: param.find('dns-server') != -1, pool))
            domain_name = list(filter(lambda param: param.find('domain-name') != -1, pool))
            dhModel.poolName = poolName[0].split(' ')[3]
            if len(network) > 0:
                dhModel.network = network[0].split(' ')[2]
                dhModel.mask = network[0].split(' ')[3]
            if len(default_router) > 0:
                dhModel.defaultRouter = default_router[0].split(' ')[2]
            if len(dns_server) > 0:
                dhModel.dnsServer = dns_server[0].split(' ')[2]
            if len(domain_name) > 0:
                dhModel.domainName = domain_name[0].split(' ')[2]
            dhModel.excludedAddresses = list(filter(lambda x: x.start in ipaddress.ip_network(f"{dhModel.network}/{dhModel.mask}"), eAddresses))
            params.append(dhModel)
        return params

    def parseLeasedAddresses(self, leasedAddresses) -> [DhcpLeasedAddressModel]:
        leasedAddresses = self.prepareOutput(leasedAddresses, 1, 1)
        leasedAddresses = removeMultipleSpaces(leasedAddresses)
        leasedAddresses: [str] = list(filter(lambda x: parseNetwork(x, 0) != '', leasedAddresses))
        leased: [DhcpLeasedAddressModel] = []
        for line in leasedAddresses:
            splitLine = line.split(' ')
            client = splitLine[1]
            address = splitLine[0]
            expiration = '{month}-{day}-{year}-{time}-{part}'.format(month=splitLine[2],
                                                                     day=splitLine[3],
                                                                     year=splitLine[4],
                                                                     time=splitLine[5],
                                                                     part=splitLine[6])
            leased.append(DhcpLeasedAddressModel(
                client=client,
                address=address,
                expiration=expiration
            ))
        return leased

    def parseOspf(self, config) -> OSPFModelResponse:
        config = config[config.find('!'):]
        config = self.prepareOutput(config, 0, 0)
        ospf = findInRunningConfig(config, 'router ospf')
        if len(ospf) > 0:
            ospf = list(map(lambda x: x.strip(), ospf[0]))

        fProcessId: [str] = list(filter(lambda x: x.find('router ospf') != -1, ospf))
        fRouterId: [str] = list(filter(lambda x: x.find('router-id') != -1, ospf))
        fPassiveInterfaces: [str] = list(filter(lambda x: x.find('passive-interface') != -1, ospf))
        fNetworks: [str] = list(filter(lambda x: x.find('network') != -1, ospf))
        fInternetRoute: [str] = list(filter(lambda x: x.find('default-information') != -1, ospf))
        fStaticRoutes: [str] = list(filter(lambda x: x.find('redistribute static') != -1, ospf))

        processId: str = fProcessId[0].split(' ')[2] if len(fProcessId) > 0 else '0'
        routerId: str = fRouterId[0].split(' ')[1] if len(fRouterId) > 0 else ''
        passiveInterfaces: [str] = []
        for interface in fPassiveInterfaces:
            if interface.lower().find('ether') != -1 or interface.lower().find('serial'):
                passiveInterfaces.append(interface.split(' ')[1])
        networks = []
        for network in fNetworks:
            networks.append(OSPFNetworkModel(
                network=parseNetwork(network, 0),
                mask=IPv4Address(int(IPv4Address(parseNetwork(network, 1)))^(2**32-1)),
                area=parseNetwork(network, 2)
            ))
        internetRoute: bool = True if len(fInternetRoute) > 0 else False
        staticRoutes: bool = True if len(fStaticRoutes) > 0 else False

        return OSPFModelResponse(
            processId=processId,
            routerId=routerId,
            networks=networks,
            passiveInterfaces=passiveInterfaces,
            internetRoute=internetRoute,
            shareStatic=staticRoutes,
        )

    def parseVlan(self, iVlan) -> [VlanModel]:
        vlan: [VlanModel] = []
        iVlan = iVlan[iVlan.find('----'):]
        iVlan = iVlan[:iVlan.find('VLAN Type')]
        iVlan = self.prepareOutput(iVlan, 1, 1)
        iVlan = removeMultipleSpaces(iVlan)
        iVlan = groupSplitLinesVlan(iVlan)

        for vl in iVlan:
            lSplit = vl.split(' ')
            vlanId: int = lSplit[0]
            name: str = lSplit[1]
            enabled: bool = True if lSplit[2].find('active') != -1 else False
            interfaces: [str] = parseInterfacesFromVlan(vl)
            vlan.append(VlanModel(
                id=vlanId,
                name=name,
                enabled=enabled,
                interfaces=interfaces
            ))

        return vlan


def removeMultipleSpaces(input) -> [str]:
    input = list(filter(None, input))
    for lineIndex, inputLine in enumerate(input):
        input[lineIndex] = inputLine.strip()
    return input


def findInRunningConfig(runningConfig, keyWord, wholeConfig=True) -> [[str]]:
    l: [[str]] = []
    for lineIndex, line in enumerate(runningConfig):
        if re.match(f"^{keyWord}", line):
            o: [str] = []
            for insertLine in runningConfig[lineIndex:]:
                if insertLine == '!':
                    break
                o.append(insertLine)
            l.append(o)
            if not wholeConfig:
                break
    return l


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


# will merge lines where on start is missing number
def groupSplitLinesVlan(input: [str]) -> [str]:
    output: [str] = []
    for l in input:
        if l[0].isnumeric():
            output.append(l)
        else:
            output[len(output) - 1] += ', ' + l

    return output


def parseInterfacesFromVlan(vlan: str) -> [str]:
    interfaces: [str]
    gi = re.compile(r'Gi[0-9]\/[0-9]')
    fa = re.compile(r'Fa[0-9]\/[0-9]')
    interfaces = gi.findall(vlan)
    interfaces += fa.findall(vlan)
    return interfaces


def parseInterface(line: str, indexOfInterface: int) -> str:
    interfaces: [str] = list(filter(
        lambda x: x.lower().find('ether') != -1 or x.lower().find('serial') != -1 or x.lower().find(
            'loop') != -1 or x.lower().find('nvi') != -1 or x.lower().find('vlan') != -1, line.split(' ')))
    return interfaces[indexOfInterface] if len(interfaces) > indexOfInterface else ''

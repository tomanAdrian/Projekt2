commands: dict[str:any] = {
    'execMode': 'enable',
    'confMode': 'configure terminal',
    'configureInterface': 'interface {interface}',
    'enableInterface': 'no shutdown',
    'disableInterface': 'shutdown',
    'setStaticRouteIpPort': 'ip route {network} {networkMask} {nextHopInterface} {nextHop}',
    'setStaticRoute': 'ip route {network} {networkMask} {nextHop}',
    'setIpAddress': 'ip address {address} {mask}',
    'deleteIpAddress': 'no ip address {address} {mask}',
    'terminalLength': 'terminal length 0',
    'saveConfiguration': 'copy running start',
    'vlan': {
        'accessMode': 'switchport mode access',
        'acceptVlan': 'switchport access vlan {vlanId}',
        'trunkEncapsulation': 'switchport trunk encapsulation dot1q',
        'trunkMode': 'switchport mode trunk',
        'create': 'vlan {vlanId}',
        'setName': 'name {name}',
        'delete': 'no vlan {vlanId}'
    },
    'dhcp': {
        'createDHCP': 'ip dhcp pool {poolName}',
        'network': 'network {network} {mask}',
        'default-gateway': 'default-router {defaultGateway}',
        'domain-name': 'domain-name {domainName}',
        'dns-server': 'dns-server {dnsServer}',
        'excluded-addresses': 'ip dhcp excluded-address {start} {end}',
        'remove': 'no ip dhcp pool {poolName}'
    },
    'nat': {
        'iLocation': 'ip nat inside',
        'oLocation': 'ip nat outside',
        'snat': 'ip nat inside source static {iAddress} {oAddress}',
        'natPool': 'ip nat pool {poolName} {start} {end} netmask {mask}',
        'natAcl': 'access-list {aclId} permit {address} {mask}',
        'dNat': 'ip nat inside source list {aclId} pool {poolName}',
        'pat': 'ip nat inside source list {aclId} interface {interface} overload',
        'pForward': 'ip nat inside source static {protocol} {iAddress} {iPort} {oAddress} {oPort}'
    },
    'ospf': {
        'confOspf': 'router ospf {processId}',
        'network': 'network {address} {wildcard} area {area}',
        'routerId': 'router-id {routerId}',
        'passiveInterface': 'passive-interface {interface}',
        'internetRoute': 'default-information originate',
        'sendStatic': 'redistribute static',
        'enableSummaryAddress': 'summary-address',
        'disableSummaryAddress': 'no summary-address',
        'deleteOspf': 'no router ospf {identifier}',
        'deleteNetwork': 'no network {address} {wildcard} area {area}'
    },
    'showCommands': {
        'vlan': 'show vlan',
        'dhcpLeasedAddresses': 'show ip dhcp binding',
        'runningConfig': 'show running-config',
        'routingTable': 'show ip route',
        'interfacesBrief': 'show ip interface brief',
        'interfaceDetail': 'show ip interface',
        'showProtocols': 'show protocols',
        'version': 'show version | include Cisco IOS Software',
        'memory': 'show version | include memory'
    }
}

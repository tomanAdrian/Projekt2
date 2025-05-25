commands: dict[str:any] = {
    'enableInterface': 'interface set {interface} disabled=no',
    'disableInterface': 'interface set {interface} disabled=yes',
    'staticRoute': {
        'base': 'ip route add dst-address={network}/{networkMask} ',
        'fullNextHop': 'gateway={nextHop}%{nextHopInterface}',
        'nextHop': 'gateway={nextHop}',
        'nextHopInterface': 'gateway={nextHopInterface}'
    },
    'setStaticRoute': 'ip route add dst-address={network}/{networkMask} gateway={nextHop}%{nextHopInterface}',
    'setIpAddress': 'ip address add address={address}/{mask} interface={interface}',
    'deleteIpAddress': 'ip address remove [find interface={interface}]',
    'dhcp': {
        'addPool': 'ip pool add name={poolName} ranges={start}-{end}',
        'addNetwork': {
            'network': 'ip dhcp-server network add address={network}/{mask}',
            'gateway': ' gateway={defaultGateway}',
            'dns-server': ' dns-server={dnsServer}',
            'domain-name': ' domain={domainName}'
        },
        'addServer': 'ip dhcp-server add name={poolName} interface={interface} address-pool={poolName}',
        'removePool': 'ip pool remove {poolName}',
        'removeNetwork': 'ip dhcp-server network remove [find address="{network}/{mask}"]',
        'removeServer': 'ip dhcp-server remove {poolName}'
    },
    'nat': {
        'dst-nat': 'ip firewall nat add chain=dstnat dst-address={oAddress} action=dst-nat to-addresses={iAddress}',
        'src-nat': 'ip firewall nat add chain=srcnat src-address={iAddress} action=src-nat to-addresses={oAddress}',
        'pat': 'ip firewall nat add chain=srcnat action=masquerade out-interface={interface}',
        'port-forward': 'ip firewall nat add chain=dstnat dst-address={oAddress} dst-port={oPort} protocol={protocol} action=dst-nat to-addresses={iAddress} to-port={iPort}',
        'dNat': 'ip firewall nat add chain=srcnat src-address={iAddress}/{imask} action=src-nat to-addresses={oStart}-{oEnd}'
    },
    'ospf': {
        'createInstance': 'routing ospf instance add name={name} version=2 router-id={routerId}',
        'createArea': 'routing ospf area add name={area} area-id={area} instance={instance}',
        'addNetwork': 'routing ospf interface-template add networks={network}/{mask} area={area}',
        'shareStatic': 'routing ospf instance set {name} redistribute=static',
        'internetRoute': 'routing ospf instance set {name} originate-default=if-installed',
        'attributes': 'routing ospf export',
        'deleteInstance': 'routing ospf instance remove {identifier}',
        'deleteInactiveAreas': 'routing ospf area remove [find inactive]',
        'deleteInactiveNetworks': 'routing ospf interface-template remove [find inactive]',
        'deleteNetwork': 'routing ospf interface-template remove [find networks={network}/{mask}]'
    },
    'vlan': {
        'createBridge': 'interface bridge add name={name} frame-types=admit-only-vlan-tagged vlan-filtering=yes',
        'accessMode': 'interface bridge port add bridge={name} interface={interface} pvid={id} frame-types=admit-only-untagged-and-priority-tagged',
        'trunkMode': 'interface bridge port add bridge={name} interface={interface} frame-types=admit-only-vlan-tagged',
        'removeVlan': 'interface bridge port remove [find where pvid={id}]'
    },
    'showCommands': {
        'ipPool': 'ip pool print terse',
        'dhcpNetwork': 'ip dhcp-server network print detail terse',
        'dhcp-server': 'ip dhcp-server print detail terse',
        'dhcpLease': 'ip dhcp-server lease print detail',
        'showInterfacesAppend': 'interface print append',
        'showInterfacesDetail': 'interface print detail',
        'showIpAddressesDetail': 'ip address print detail',
        'showRoutingTableDetail': 'ip route print detail terse',
        'runningConfiguration': 'export',
        'version': 'system resource print',
        'nat': 'ip firewall nat print terse',
        'vlan': 'interface bridge port print'
    }
}
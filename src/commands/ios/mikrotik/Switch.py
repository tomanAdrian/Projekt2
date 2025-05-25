from src.commands.device.Switch import Switch
from src.commands.conf_commands.MikrotikCommands import commands
from src.api.validators.Validators import TypeOfValidation
from src.model.VlanModel import CreateVlanModel, AcceptVlanModel, TrunkModeModel


class MikrotikSwitch(Switch):
    def __init__(self):
        self.vendor = 'mikrotik'

    def showVlan(self) -> [dict[str, any]]:
        return [
            {
                'command': commands['showCommands']['vlan'],
                'validation': TypeOfValidation.OUTPUT
            }
        ]

    def createVlan(self, body: CreateVlanModel, enablePassword='') -> [dict[str, any]]:
        pass

    def createBridge(self, name: str) -> [dict[str, any]]:
        return [
            {
                'command': commands['vlan']['createBridge'].format(name=name),
                'validation': TypeOfValidation.OUTPUT
            }
        ]

    def acceptVlan(self, body: AcceptVlanModel, enablePassword='') -> [dict[str, any]]:
        return [
            {
                'command': commands['vlan']['accessMode'].format(name=body.bridgeName, interface=body.interface, id=body.id),
                'validation': TypeOfValidation.PORT
            }
        ]

    def trunkMode(self, body: TrunkModeModel, enablePassword='') -> [dict[str, any]]:
        return [
            {
                'command': commands['vlan']['trunkMode'].format(name=body.bridgeName, interface=body.interface),
                'validation': TypeOfValidation.PORT
            }
        ]

    def deleteVlan(self, vlanId: int, enablePassword: str = None):
        return [
            {
                'command': commands['vlan']['removeVlan'].format(id=vlanId),
                'validation': TypeOfValidation.PORT
            }
        ]

    def getVendor(self) -> str:
        return self.vendor
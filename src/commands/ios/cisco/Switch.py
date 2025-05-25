from src.commands.device.Switch import Switch
from src.commands.conf_commands.CiscoCommands import commands
from src.api.validators.Validators import TypeOfValidation
from src.model.VlanModel import AcceptVlanModel, TrunkModeModel, CreateVlanModel


class CiscoSwitch(Switch):
    def __init__(self):
        self.vendor = 'cisco'

    def trunkMode(self, body: TrunkModeModel, enablePassword='') -> [dict[str, any]]:
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
                'command': f"{commands['vlan']['trunkEncapsulation']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['vlan']['trunkMode']}\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    def acceptVlan(self, body: AcceptVlanModel, enablePassword='') -> [dict[str, any]]:
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
                'command': f"{commands['vlan']['acceptVlan'].format(vlanId=body.id)}\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    def showVlan(self) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['showCommands']['vlan']}\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    def createVlan(self, body: CreateVlanModel, enablePassword='') -> [dict[str, any]]:
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
                'command': f"{commands['vlan']['create'].format(vlanId=body.id)}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"{commands['vlan']['setName'].format(name=body.name)}\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    def deleteVlan(self, vlanId: int, enablePassword: str = None):
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
                'command': f"{commands['vlan']['delete'].format(vlanId=vlanId)}\n",
                'validation': TypeOfValidation.NONE
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
                'validation': TypeOfValidation.NONE
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
                'validation': TypeOfValidation.NONE
            }
        ]

    def saveConfig(self, enablePassword=None) -> [dict[str, any]]:
        return [
            {
                'command': f"{commands['saveConfiguration']}\n",
                'validation': TypeOfValidation.NONE
            },
            {
                'command': f"\r\n",
                'validation': TypeOfValidation.NONE
            }
        ]

    def createBridge(self, name: str):
        pass

    def getVendor(self) -> str:
        return self.vendor

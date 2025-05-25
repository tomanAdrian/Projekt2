from abc import ABC, abstractmethod


class BaseCommands(ABC):
    @abstractmethod
    def getVersion(self) -> [dict[str, any]]:
        pass

    @abstractmethod
    def getConfig(self, enablePassword: str = None) -> [dict[str, any]]:
        pass

    @abstractmethod
    def saveConfig(self, enablePassword: str = None) -> [dict[str, any]]:
        pass

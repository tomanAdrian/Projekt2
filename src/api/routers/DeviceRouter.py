from fastapi import APIRouter, status, Query
from src.api.controllers.DeviceController import DeviceController
from src.model.DeviceModel import ConfigurationModel, VersionModel
from src.api.validators.Validators import HTTPError, CommandExecutionError
from src.core.config import TypeOfConnection, Vendors, QueryDescription
from ipaddress import IPv4Address

deviceRouter = APIRouter()
deviceController = DeviceController()


@deviceRouter.get('/device/config', response_model=ConfigurationModel, tags=['Device'],
                  name='Get running configuration of device',
                  description='Get running configuration of device',
                  status_code=status.HTTP_202_ACCEPTED,
                  responses={
                      status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                  })
def getRunningConfiguration(host: IPv4Address = Query(description=QueryDescription.HOST),
                            vendor: Vendors = Query(description=QueryDescription.VENDOR),
                            connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                            user: str = Query(default='', description=QueryDescription.NAME),
                            password: str = Query(default='', description=QueryDescription.PASSWORD),
                            port: int = Query(default=22, description=QueryDescription.PORT),
                            enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        config = deviceController.getConfiguration(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                                   connection=connection, enablePassword=enablePassword)
    except CommandExecutionError as e:
        return e.json()
    return config


@deviceRouter.get('/device/version', response_model=VersionModel, tags=['Device'],
                  summary='Get version of device with its free memory',
                  description='It will return software version of device and also devices memory status',
                  status_code=status.HTTP_202_ACCEPTED,
                  responses={
                      status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                  })
def getVersion(host: IPv4Address = Query(description=QueryDescription.HOST),
               vendor: Vendors = Query(description=QueryDescription.VENDOR),
               connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
               user: str = Query(default='', description=QueryDescription.NAME),
               password: str = Query(default='', description=QueryDescription.PASSWORD),
               port: int = Query(default=22, description=QueryDescription.PORT)):
    try:
        version = deviceController.getVersion(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                              connection=connection)
    except CommandExecutionError as e:
        return e.json()
    return version


@deviceRouter.post('/device/saveConfiguration', tags=['Device'],
                   summary='Save running configuration of Cisco devices',
                   description='On Cisco devices is not defaultly possible to auto save configured changes '
                               'for this problem is solution this endpoint',
                   status_code=status.HTTP_204_NO_CONTENT,
                   responses={
                       status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                   })
def saveRunning(host: IPv4Address = Query(description=QueryDescription.HOST),
                vendor: Vendors = Query(description=QueryDescription.VENDOR),
                connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                user: str = Query(default='', description=QueryDescription.NAME),
                password: str = Query(default='', description=QueryDescription.PASSWORD),
                port: int = Query(default=22, description=QueryDescription.PORT),
                enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        deviceController.saveConfiguration(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                           connection=connection, enablePassword=enablePassword)
    except CommandExecutionError as e:
        return e.json()
    return {}

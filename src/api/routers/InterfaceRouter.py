from fastapi import APIRouter, status, Body, Query
from src.api.controllers.InterfaceController import InterfaceController
from src.model.InterfaceModel import InterfaceShort, InterfaceStatusModel, InterfaceIpModel
from src.api.validators.Validators import HTTPError, CommandExecutionError
from src.core.config import TypeOfConnection, Vendors, QueryDescription

from pydantic import ValidationError
from ipaddress import IPv4Address
from src.api.validators.Validators import missingRequiredAttribute

interfaceRouter = APIRouter()
interfaceController = InterfaceController()


@interfaceRouter.get('/interface', response_model=list[InterfaceShort], tags=['Interface'],
                     summary='Get all interfaces',
                     description='Return list of all interfaces with brief info',
                     status_code=status.HTTP_202_ACCEPTED,
                     responses={
                         status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                     })
def getInterfacesBrief(host: IPv4Address = Query(description=QueryDescription.HOST),
                       vendor: Vendors = Query(description=QueryDescription.VENDOR),
                       connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                       user: str = Query(default='', description=QueryDescription.NAME),
                       password: str = Query(default='', description=QueryDescription.PASSWORD),
                       port: int = Query(default=22, description=QueryDescription.PORT)):
    try:
        output = interfaceController.getInterfacesBrief(host=str(host), user=user, password=password, vendor=vendor,
                                                        port=port, connection=connection)
    except CommandExecutionError as e:
        return e.json()
    return output


@interfaceRouter.post('/interface/status', tags=['Interface'],
                      summary='Turn off/on interface',
                      description='Set status of interface. If it is enabled or disabled',
                      status_code=status.HTTP_204_NO_CONTENT,
                      responses={
                          status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                      },
                      response_model='')
def setInterfaceStatus(host: IPv4Address = Query(description=QueryDescription.HOST),
                       vendor: Vendors = Query(description=QueryDescription.VENDOR),
                       connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                       interface: InterfaceStatusModel = Body(
                           examples=InterfaceStatusModel.Config.schema_extra["examples"]),
                       user: str = Query(default='', description=QueryDescription.NAME),
                       password: str = Query(default='', description=QueryDescription.PASSWORD),
                       port: int = Query(default=22, description=QueryDescription.PORT),
                       enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        interfaceController.setInterfaceStatus(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                               interface=interface, connection=connection,
                                               enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()


@interfaceRouter.post('/interface/ipaddress', tags=['Interface'],
                      summary='Set IP address',
                      description='Set IP address of interface',
                      status_code=status.HTTP_204_NO_CONTENT,
                      responses={
                          status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                          status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                      })
def setIpaddress(host: IPv4Address = Query(description=QueryDescription.HOST),
                 vendor: Vendors = Query(description=QueryDescription.VENDOR),
                 connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                 body: InterfaceIpModel = Body(examples=InterfaceIpModel.Config.schema_extra["examples"]),
                 user: str = Query(default='', description=QueryDescription.NAME),
                 password: str = Query(default='', description=QueryDescription.PASSWORD),
                 port: int = Query(default=22, description=QueryDescription.PORT),
                 enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        interfaceController.setIpaddress(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                         body=body, connection=connection, enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()


@interfaceRouter.delete('/interface/ipaddress', tags=['Interface'],
                        summary='Delete IP address',
                        description='Delete IP address of interface',
                        status_code=status.HTTP_204_NO_CONTENT,
                        responses={
                            status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                            status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                        })
def deleteIpaddress(host: IPv4Address = Query(description=QueryDescription.HOST),
                    vendor: Vendors = Query(description=QueryDescription.VENDOR),
                    connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                    body: InterfaceIpModel = Body(examples=InterfaceIpModel.Config.schema_extra["examples"]),
                    user: str = Query(default='', description=QueryDescription.NAME),
                    password: str = Query(default='', description=QueryDescription.PASSWORD),
                    port: int = Query(default=22, description=QueryDescription.PORT),
                    enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        interfaceController.deleteIpaddress(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                            body=body, connection=connection, enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()

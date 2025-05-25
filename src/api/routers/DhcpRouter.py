from fastapi import APIRouter, status, Body, Query
from ipaddress import IPv4Address
from fastapi.exceptions import ValidationError
from src.api.controllers.DhcpController import DhcpController
from src.model.DhcpModel import DhcpModel, DhcpStatusModel, DhcpLeasedAddressModel, DhcpRemoveModel
from src.api.validators.Validators import validateEnablePassword, HTTPError, CommandExecutionError, \
    missingRequiredAttribute
from src.core.config import TypeOfConnection, Vendors, QueryDescription

dhcpRouter = APIRouter()
dhcpController = DhcpController()


@dhcpRouter.get('/dhcp/status', tags=['DHCP'], status_code=status.HTTP_202_ACCEPTED,
                response_model=list[DhcpStatusModel],
                summary='Returns main parameters of DHCP server',
                description='Returns main parameters of DHCP server',
                responses={
                    status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                })
def getDhcpStatus(host: IPv4Address = Query(description=QueryDescription.HOST),
                  vendor: Vendors = Query(description=QueryDescription.VENDOR),
                  connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                  user: str = Query(default='', description=QueryDescription.NAME),
                  password: str = Query(default='', description=QueryDescription.PASSWORD),
                  port: int = Query(default=22, description=QueryDescription.PORT),
                  enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        validateEnablePassword(vendor=vendor, enablePassword=enablePassword)
        params = dhcpController.getDhcpStatus(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                              enablePassword=enablePassword, connection=connection)
    except CommandExecutionError as e:
        return e.json()
    return params


@dhcpRouter.get('/dhcp/leases', tags=['DHCP'], status_code=status.HTTP_202_ACCEPTED,
                response_model=list[DhcpLeasedAddressModel],
                summary='Get status of leased addresses',
                description='Returns leased addresses with Clients MAC addresses and date of expiration',
                responses={
                    status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                })
def getDhcpLeasesAddresses(host: IPv4Address = Query(description=QueryDescription.HOST),
                           vendor: Vendors = Query(description=QueryDescription.VENDOR),
                           connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                           user: str = Query(default='', description=QueryDescription.NAME),
                           password: str = Query(default='', description=QueryDescription.PASSWORD),
                           port: int = Query(default=22, description=QueryDescription.PORT)):
    try:
        leased = dhcpController.getDhcpLeasesAddresses(host=str(host), user=user, password=password, vendor=vendor,
                                                       port=port, connection=connection)
    except CommandExecutionError as e:
        return e.json()
    return leased


@dhcpRouter.post('/dhcp', tags=['DHCP'], status_code=status.HTTP_204_NO_CONTENT,
                 summary='Create DHCP server',
                 description='Create DHCP-server with defined parameters',
                 responses={
                     status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                 })
def dhcpCreate(host: IPv4Address = Query(description=QueryDescription.HOST),
               connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
               vendor: Vendors = Query(description=QueryDescription.VENDOR),
               user: str = Query(default='', description=QueryDescription.NAME),
               password: str = Query(default='', description=QueryDescription.PASSWORD),
               port: int = Query(default=22, description=QueryDescription.PORT),
               dhcp: DhcpModel = Body(examples=DhcpModel.Config.schema_extra["examples"]),
               enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        dhcpController.dhcpCreate(host=str(host), user=user, password=password, vendor=vendor, port=port, dhcp=dhcp,
                                  connection=connection, enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()


@dhcpRouter.delete('/dhcp/{poolName}', tags=['DHCP'], status_code=status.HTTP_204_NO_CONTENT,
                   summary='Delete DHCP-server',
                   description='Deletes DHCP-server by specified pool name',
                   responses={
                       status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                   })
def dhcpDelete(host: IPv4Address = Query(description=QueryDescription.HOST),
               connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
               vendor: Vendors = Query(description=QueryDescription.VENDOR),
               poolName: str = Query(description=QueryDescription.POOL_NAME),
               body: DhcpRemoveModel = Body(examples=DhcpRemoveModel.Config.schema_extra["examples"]),
               user: str = Query(default='', description=QueryDescription.NAME),
               password: str = Query(default='', description=QueryDescription.PASSWORD),
               port: int = Query(default=22, description=QueryDescription.PORT),
               enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        validateEnablePassword(vendor=vendor, enablePassword=enablePassword)
        dhcpController.dhcpRemove(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                  enablePassword=enablePassword, poolName=poolName, connection=connection, body=body)
    except CommandExecutionError as e:
        return e.json()

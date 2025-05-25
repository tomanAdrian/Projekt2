from src.model.NatModel import SNATModel, DNATModel, PATModel, PortRedirectionModel, LocationModel
from src.api.validators.Validators import HTTPError, missingRequiredAttribute, CommandExecutionError
from src.api.controllers.NatController import NatController
from src.core.config import TypeOfConnection, Vendors, QueryDescription
from fastapi import APIRouter, status, Body, Query
from pydantic import ValidationError
from ipaddress import IPv4Address

natRouter = APIRouter()
natController = NatController()


@natRouter.get('/nat/snat', tags=['NAT'], status_code=status.HTTP_202_ACCEPTED,
               summary='Get SNAT',
               description='GET static NAT',
               response_model=list[SNATModel],
               responses={
                   status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                   status.HTTP_403_FORBIDDEN: {"model": HTTPError}
               })
def getSNAT(host: IPv4Address = Query(description=QueryDescription.HOST),
            vendor: Vendors = Query(description=QueryDescription.VENDOR),
            connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
            user: str = Query(default='', description=QueryDescription.NAME),
            password: str = Query(default='', description=QueryDescription.PASSWORD),
            port: int = Query(default=22, description=QueryDescription.PORT),
            enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        snat = natController.getSNAT(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                     connection=connection, enablePassword=enablePassword)
    except CommandExecutionError as e:
        return e.json()
    return snat


@natRouter.get('/nat/dnat', tags=['NAT'], status_code=status.HTTP_202_ACCEPTED,
               summary='Get DNAT',
               description='Get Dynamic NAT',
               response_model=list[DNATModel],
               responses={
                   status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                   status.HTTP_403_FORBIDDEN: {"model": HTTPError}
               })
def getDNAT(host: IPv4Address = Query(description=QueryDescription.HOST),
            vendor: Vendors = Query(description=QueryDescription.VENDOR),
            connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
            user: str = Query(default='', description=QueryDescription.NAME),
            password: str = Query(default='', description=QueryDescription.PASSWORD),
            port: int = Query(default=22, description=QueryDescription.PORT),
            enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        dnat = natController.getDNAT(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                     connection=connection, enablePassword=enablePassword)
    except CommandExecutionError as e:
        return e.json()
    return dnat


@natRouter.get('/nat/pat', tags=['NAT'], status_code=status.HTTP_202_ACCEPTED,
               summary='Get PAT',
               description='Get PAT',
               response_model=list[PATModel],
               responses={
                   status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                   status.HTTP_403_FORBIDDEN: {"model": HTTPError}
               })
def getPAT(host: IPv4Address = Query(description=QueryDescription.HOST),
           vendor: Vendors = Query(description=QueryDescription.VENDOR),
           connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
           user: str = Query(default='', description=QueryDescription.NAME),
           password: str = Query(default='', description=QueryDescription.PASSWORD),
           port: int = Query(default=22, description=QueryDescription.PORT),
           enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        pat = natController.getPAT(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                   connection=connection, enablePassword=enablePassword)
    except CommandExecutionError as e:
        return e.json()
    return pat


@natRouter.get('/nat/portForward', tags=['NAT'], status_code=status.HTTP_202_ACCEPTED,
               summary='Get PortForward',
               description='Get PortForward',
               response_model=list[PortRedirectionModel],
               responses={
                   status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                   status.HTTP_403_FORBIDDEN: {"model": HTTPError}
               })
def getPAT(host: IPv4Address = Query(description=QueryDescription.HOST),
           vendor: Vendors = Query(description=QueryDescription.VENDOR),
           connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
           user: str = Query(default='', description=QueryDescription.NAME),
           password: str = Query(default='', description=QueryDescription.PASSWORD),
           port: int = Query(default=22, description=QueryDescription.PORT),
           enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        pf = natController.getPortForward(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                          connection=connection, enablePassword=enablePassword)
    except CommandExecutionError as e:
        return e.json()
    return pf


@natRouter.post('/nat/snat', tags=['NAT'], status_code=status.HTTP_204_NO_CONTENT,
                summary='Set SNAT',
                description='Set Static NAT',
                responses={
                    status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                    status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                })
def setSNAT(host: IPv4Address = Query(description=QueryDescription.HOST),
            vendor: Vendors = Query(description=QueryDescription.VENDOR),
            connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
            body: SNATModel = Body(examples=SNATModel.Config.schema_extra["examples"]),
            user: str = Query(default='', description=QueryDescription.NAME),
            password: str = Query(default='', description=QueryDescription.PASSWORD),
            port: int = Query(default=22, description=QueryDescription.PORT),
            enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        natController.setSNAT(host=str(host), user=user, password=password, vendor=vendor, port=port, body=body,
                              connection=connection, enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()


@natRouter.post('/nat/dnat', tags=['NAT'], status_code=status.HTTP_204_NO_CONTENT,
                summary='Set DNAT',
                description='Set dynamic NAT',
                responses={
                    status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                    status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                })
def setDNAT(host: IPv4Address = Query(description=QueryDescription.HOST),
            vendor: Vendors = Query(description=QueryDescription.VENDOR),
            connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
            body: DNATModel = Body(examples=DNATModel.Config.schema_extra["examples"]),
            user: str = Query(default='', description=QueryDescription.NAME),
            password: str = Query(default='', description=QueryDescription.PASSWORD),
            port: int = Query(default=22, description=QueryDescription.PORT),
            enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        natController.setDNAT(host=str(host), user=user, password=password, vendor=vendor, port=port, body=body,
                              connection=connection, enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()


@natRouter.post('/nat/pat', tags=['NAT'], status_code=status.HTTP_204_NO_CONTENT,
                summary='Set PAT',
                description='Set PAT',
                responses={
                    status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                    status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                })
def setPAT(host: IPv4Address = Query(description=QueryDescription.HOST),
           vendor: Vendors = Query(description=QueryDescription.VENDOR),
           connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
           body: PATModel = Body(examples=PATModel.Config.schema_extra["examples"]),
           user: str = Query(default='', description=QueryDescription.NAME),
           password: str = Query(default='', description=QueryDescription.PASSWORD),
           port: int = Query(default=22, description=QueryDescription.PORT),
           enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        natController.setPAT(host=str(host), user=user, password=password, vendor=vendor, port=port, body=body,
                             connection=connection, enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()


@natRouter.post('/nat/portForward', tags=['NAT'], status_code=status.HTTP_204_NO_CONTENT,
                summary='Set PortForward',
                description='Add port forward',
                responses={
                    status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                    status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                })
def setPAT(host: IPv4Address = Query(description=QueryDescription.HOST),
           vendor: Vendors = Query(description=QueryDescription.VENDOR),
           connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
           body: PortRedirectionModel = Body(examples=PortRedirectionModel.Config.schema_extra["examples"]),
           user: str = Query(default='', description=QueryDescription.NAME),
           password: str = Query(default='', description=QueryDescription.PASSWORD),
           port: int = Query(default=22, description=QueryDescription.PORT),
           enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        natController.setPortRedirection(host=str(host), user=user, password=password, vendor=vendor, port=port, body=body,
                                         connection=connection, enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()


@natRouter.post('/nat/location', tags=['NAT'], status_code=status.HTTP_204_NO_CONTENT,
                summary='Set location',
                description='Set interface location for Cisco routers',
                responses={
                    status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                    status.HTTP_403_FORBIDDEN: {
                        "Detail": "This method is not implemented for particular vendors. Vendor: Mikrotik"}
                })
def setLocation(host: IPv4Address = Query(description=QueryDescription.HOST),
                vendor: Vendors = Query(description=QueryDescription.VENDOR),
                connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                body: LocationModel = Body(examples=LocationModel.Config.schema_extra["examples"]),
                user: str = Query(default='', description=QueryDescription.NAME),
                password: str = Query(default='', description=QueryDescription.PASSWORD),
                port: int = Query(default=22, description=QueryDescription.PORT),
                enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        natController.setLocation(host=str(host), user=user, password=password, vendor=vendor, port=port, body=body,
                                  connection=connection, enablePassword=enablePassword)
    except CommandExecutionError as e:
        return e.json()
    return {}

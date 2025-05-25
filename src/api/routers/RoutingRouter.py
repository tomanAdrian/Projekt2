from fastapi import APIRouter, status, Body, Query
from src.model.RoutingModel import RoutingTableModel, StaticRouteModel, OSPFModel, OSPFModelResponse, \
    AddOSPFNetworkModel
from src.api.controllers.RoutingController import RoutingController
from src.api.validators.Validators import HTTPError, missingRequiredAttribute, \
    CommandExecutionError
from src.core.config import TypeOfConnection, Vendors, QueryDescription
from pydantic import ValidationError
from ipaddress import IPv4Address

routingRouter = APIRouter()
routingController = RoutingController()


@routingRouter.get('/routing/table', tags=['Routing'], response_model=RoutingTableModel,
                   status_code=status.HTTP_202_ACCEPTED,
                   summary='Get routing table',
                   description='Get routing table of router',
                   responses={
                       status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                   })
def getRoutingTable(host: IPv4Address = Query(description=QueryDescription.HOST),
                    vendor: Vendors = Query(description=QueryDescription.VENDOR),
                    connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                    user: str = Query(default='', description=QueryDescription.NAME),
                    password: str = Query(default='', description=QueryDescription.PASSWORD),
                    port: int = Query(default=22, description=QueryDescription.PORT)):
    try:
        output = routingController.getRoutingTable(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                                   connection=connection)
    except CommandExecutionError as e:
        return e.json()
    return output


@routingRouter.post('/routing/staticRoute', tags=['Routing'], response_model={},
                    status_code=status.HTTP_204_NO_CONTENT,
                    summary='Set static route',
                    description='Set static route',
                    responses={
                        status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                    })
def postStaticRoute(host: IPv4Address = Query(description=QueryDescription.HOST),
                    vendor: Vendors = Query(description=QueryDescription.VENDOR),
                    connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                    route: StaticRouteModel = Body(examples=StaticRouteModel.Config.schema_extra["examples"]),
                    user: str = Query(default='', description=QueryDescription.NAME),
                    password: str = Query(ddefault='', escription=QueryDescription.PASSWORD),
                    port: int = Query(default=22, description=QueryDescription.PORT),
                    enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        routingController.postStaticRoute(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                          route=route, connection=connection, enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()


@routingRouter.post('/routing/ospf', tags=['Routing'],
                    summary='Set OSPF',
                    description='Initiate OSPF routing protocol',
                    status_code=status.HTTP_204_NO_CONTENT,
                    responses={
                        status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                        status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                    })
def setOspf(host: IPv4Address = Query(description=QueryDescription.HOST),
            vendor: Vendors = Query(description=QueryDescription.VENDOR),
            connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
            body: OSPFModel = Body(examples=OSPFModel.Config.schema_extra["examples"]),
            user: str = Query(default='', description=QueryDescription.NAME),
            password: str = Query(default='', description=QueryDescription.PASSWORD),
            port: int = Query(default=22, description=QueryDescription.PORT),
            enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        routingController.setOspf(host=str(host), user=user, password=password, vendor=vendor, port=port, body=body,
                                  connection=connection, enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()


@routingRouter.get('/routing/ospf', tags=['Routing'],
                   summary='Get OSPF attributes',
                   description='Get OSPF attributes',
                   response_model=OSPFModelResponse,
                   status_code=status.HTTP_202_ACCEPTED,
                   responses={
                       status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                       status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                   })
def getOspf(host: IPv4Address = Query(description=QueryDescription.HOST),
            vendor: Vendors = Query(description=QueryDescription.VENDOR),
            connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
            user: str = Query(default='', description=QueryDescription.NAME),
            password: str = Query(default='', description=QueryDescription.PASSWORD),
            port: int = Query(default=22, description=QueryDescription.PORT),
            enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        parameters = routingController.getOspf(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                               enablePassword=enablePassword, connection=connection)
    except CommandExecutionError as e:
        return e.json()
    return parameters


@routingRouter.delete('/routing/ospf/{identifier}', tags=['Routing'],
                      summary='Delete OSPF',
                      description='Delete OSPF by its identifier Cisco(processId)/Mikrotik(name)',
                      status_code=status.HTTP_204_NO_CONTENT,
                      responses={
                          status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                          status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                      })
def deleteOspf(host: IPv4Address = Query(description=QueryDescription.HOST),
               vendor: Vendors = Query(description=QueryDescription.VENDOR),
               connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
               identifier: str = Query(description=QueryDescription.CONNECTION),
               user: str = Query(default='', description=QueryDescription.NAME),
               password: str = Query(default='', description=QueryDescription.PASSWORD),
               port: int = Query(default=22, description=QueryDescription.PORT),
               enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        routingController.deleteOspf(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                     enablePassword=enablePassword, identifier=identifier, connection=connection)
    except CommandExecutionError as e:
        return e.json()


@routingRouter.post('/routing/ospf/{identifier}/network', tags=['Routing'],
                    summary='Add network',
                    description='Add OSPF network by its identifier Cisco(processId)/Mikrotik(name)',
                    status_code=status.HTTP_204_NO_CONTENT,
                    responses={
                        status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                        status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                    })
def addOspfNetwork(host: IPv4Address = Query(description=QueryDescription.HOST),
                   vendor: Vendors = Query(description=QueryDescription.VENDOR),
                   connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                   identifier: str = Query(description=QueryDescription.CONNECTION),
                   network: AddOSPFNetworkModel = Body(examples=AddOSPFNetworkModel.Config.schema_extra["examples"]),
                   user: str = Query(default='', description=QueryDescription.NAME),
                   password: str = Query(default='', description=QueryDescription.PASSWORD),
                   port: int = Query(default=22, description=QueryDescription.PORT),
                   enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        routingController.addOspfNetwork(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                         identifier=identifier, network=network, connection=connection,
                                         enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()


@routingRouter.delete('/routing/ospf/{identifier}/network', tags=['Routing'],
                      summary='Delte OSPF network',
                      description='Delete OSPF network by its identifier Cisco(processId)/Mikrotik(name)',
                      status_code=status.HTTP_204_NO_CONTENT,
                      responses={
                          status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                          status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                      })
def deleteOspfNetwork(host: IPv4Address = Query(description=QueryDescription.HOST),
                      vendor: Vendors = Query(description=QueryDescription.VENDOR),
                      connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                      identifier: str = Query(description=QueryDescription.CONNECTION),
                      network: AddOSPFNetworkModel = Body(examples=AddOSPFNetworkModel.Config.schema_extra["examples"]),
                      user: str = Query(default='', description=QueryDescription.NAME),
                      password: str = Query(default='', description=QueryDescription.PASSWORD),
                      port: int = Query(default=22, description=QueryDescription.PORT),
                      enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        routingController.deleteOspfNetwork(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                            identifier=identifier, network=network, connection=connection,
                                            enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()

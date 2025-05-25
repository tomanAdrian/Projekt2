from fastapi import APIRouter, status, Body, Query
from src.api.controllers.VlanController import VlanController
from src.model.VlanModel import VlanModel
from src.api.validators.Validators import HTTPError
from src.api.validators.Validators import validateEnablePassword, missingRequiredAttribute, CommandExecutionError
from src.model.VlanModel import AcceptVlanModel, TrunkModeModel, CreateVlanModel
from src.core.config import TypeOfConnection, Vendors, QueryDescription
from pydantic import ValidationError
from ipaddress import IPv4Address

vlanRouter = APIRouter()
vlanController = VlanController()


@vlanRouter.get('/vlan', tags=['VLAN'], response_model=list[VlanModel],
                summary='Get VLANs',
                description='Get all VLANs',
                status_code=status.HTTP_202_ACCEPTED,
                responses={
                    status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                })
def getVlan(host: IPv4Address = Query(description=QueryDescription.HOST),
            vendor: Vendors = Query(description=QueryDescription.VENDOR),
            connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
            user: str = Query(default='', description=QueryDescription.NAME),
            password: str = Query(default='', description=QueryDescription.PASSWORD),
            port: int = Query(default=22, description=QueryDescription.PORT)):
    try:
        vlan = vlanController.showVlan(host=str(host), user=user, password=password, vendor=vendor, port=port,
                                       connection=connection)
    except CommandExecutionError as e:
        return e.json()
    return vlan


@vlanRouter.post('/vlan/acceptVlan', tags=['VLAN'],
                 summary='Accept VLAN',
                 description='Set interface to accept certain VLAN',
                 status_code=status.HTTP_204_NO_CONTENT,
                 responses={
                     status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                     status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                 })
def acceptVlan(host: IPv4Address = Query(description=QueryDescription.HOST),
               vendor: Vendors = Query(description=QueryDescription.VENDOR),
               connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
               body: AcceptVlanModel = Body(examples=AcceptVlanModel.Config.schema_extra["examples"]),
               user: str = Query(default='', description=QueryDescription.NAME),
               password: str = Query(default='', description=QueryDescription.PASSWORD),
               port: int = Query(default=22, description=QueryDescription.PORT),
               enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        vlanController.acceptVlan(host=str(host), user=user, password=password, vendor=vendor, port=port, body=body,
                                  connection=connection, enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()


@vlanRouter.post('/vlan/trunkMode', tags=['VLAN'],
                 summary='Set TRUNK',
                 description='Set interface to trunk mode',
                 status_code=status.HTTP_204_NO_CONTENT,
                 responses={
                     status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                     status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                 })
def trunkMode(host: IPv4Address = Query(description=QueryDescription.HOST),
              vendor: Vendors = Query(description=QueryDescription.VENDOR),
              connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
              body: TrunkModeModel = Body(examples=TrunkModeModel.Config.schema_extra["examples"]),
              user: str = Query(default='', description=QueryDescription.NAME),
              password: str = Query(default='', description=QueryDescription.PASSWORD),
              port: int = Query(default=22, description=QueryDescription.PORT),
              enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        vlanController.trunkMode(host=str(host), user=user, password=password, vendor=vendor, port=port, body=body,
                                 connection=connection, enablePassword=enablePassword)
    except ValidationError as e:
        return missingRequiredAttribute(error=e)
    except CommandExecutionError as e:
        return e.json()


@vlanRouter.post('/vlan', tags=['VLAN'],
                 summary='Set VLAN',
                 description='Create Vlan supported only for Cisco devices\nMikrotik has to use create bridge endpoint',
                 status_code=status.HTTP_204_NO_CONTENT,
                 responses={
                     status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                     status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                 })
def createVlan(host: IPv4Address = Query(description=QueryDescription.HOST),
               vendor: Vendors = Query(description=QueryDescription.VENDOR),
               connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
               body: CreateVlanModel = Body(examples=CreateVlanModel.Config.schema_extra["examples"]),
               user: str = Query(default='', description=QueryDescription.NAME),
               password: str = Query(default='', description=QueryDescription.PASSWORD),
               port: int = Query(default=22, description=QueryDescription.PORT),
               enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    try:
        vlanController.createVlan(host=str(host), user=user, password=password, vendor=vendor, port=port, body=body,
                                  connection=connection, enablePassword=enablePassword)
    except CommandExecutionError as e:
        return e.json()


@vlanRouter.post('/vlan/bridge/{name}', tags=['VLAN'],
                 summary='Create bridge',
                 description='Create Vlan for Mikrotik devices',
                 status_code=status.HTTP_204_NO_CONTENT,
                 responses={
                     status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                     status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                 })
def createBridge(host: IPv4Address = Query(description=QueryDescription.HOST),
                 vendor: Vendors = Query(description=QueryDescription.VENDOR),
                 connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
                 name: str = Query(description=QueryDescription.ENABLE),
                 user: str = Query(default='', description=QueryDescription.NAME),
                 password: str = Query(default='', description=QueryDescription.PASSWORD),
                 port: int = Query(default=22, description=QueryDescription.PORT)):
    try:
        vlanController.createBridge(host=str(host), user=user, password=password, vendor=vendor, port=port, name=name,
                                    connection=connection)
    except CommandExecutionError as e:
        return e.json()


@vlanRouter.delete('/vlan/{vlanId}', tags=['VLAN'],
                   summary='Delete VLAN',
                   description='Delete Vlan',
                   status_code=status.HTTP_204_NO_CONTENT,
                   responses={
                       status.HTTP_401_UNAUTHORIZED: {"Detail": "Unable to init SSH communication"},
                       status.HTTP_403_FORBIDDEN: {"model": HTTPError}
                   })
def deleteVlan(host: IPv4Address = Query(description=QueryDescription.HOST),
               vendor: Vendors = Query(description=QueryDescription.VENDOR),
               connection: TypeOfConnection = Query(description=QueryDescription.CONNECTION),
               vlanId: int = Query(description=QueryDescription.PORT),
               user: str = Query(default='', description=QueryDescription.NAME),
               password: str = Query(default='', description=QueryDescription.PASSWORD),
               port: int = Query(default=22, description=QueryDescription.PORT),
               enablePassword: str = Query(default='', description=QueryDescription.ENABLE)):
    validateEnablePassword(vendor=vendor, enablePassword=enablePassword)
    vlanController.deleteVlan(host=str(host), user=user, password=password, vendor=vendor, port=port, vlanId=vlanId,
                              enablePassword=enablePassword, connection=connection)
    return

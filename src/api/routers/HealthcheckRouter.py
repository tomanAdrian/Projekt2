from fastapi import APIRouter

healthcheckRouter = APIRouter()


@healthcheckRouter.get('/healthcheck', status_code=200, tags=['Healthcheck'],
                       summary='Verify that app is running')
def healthCheck():
    return {'message': 'App is running'}

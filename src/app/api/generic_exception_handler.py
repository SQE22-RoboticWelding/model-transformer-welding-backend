from typing import Callable

from fastapi import HTTPException, Request, Response
from fastapi.routing import APIRoute, APIRouter


class APIRouterWithGenericExceptionHandler(APIRouter):
    """
    The custom route_class gets overridden everytime a new APIRouter is added. This wrapper class adds the
    generic exception handler route class by default. Needs to be used for all APIRouter as replacement in the
    application to work.
    """
    def __init__(self):
        super().__init__(route_class=GenericExceptionHandler)


class GenericExceptionHandler(APIRoute):
    """
    Custom route to catch unhandled exceptions to convert them into HTTPExceptions. The original exception message is
    added to the detail of the HTTPException. If an HTTPException is already thrown, it is passed on without
    intervention. HTTPExceptions are handled by the default exception handler of FastAPI, if not changed.
    """
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except HTTPException as ex:
                raise ex
            except Exception as ex:
                raise HTTPException(status_code=400, detail=repr(ex))

        return custom_route_handler

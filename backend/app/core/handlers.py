from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import StudioPilotException
from app.core.responses import error_response


async def studio_exception_handler(
    request: Request,
    exc: StudioPilotException
):
    return JSONResponse(
        status_code=400,
        content=error_response(exc.message)
    )
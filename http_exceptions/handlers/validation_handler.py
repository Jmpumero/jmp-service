from typing import Dict, Any
from logging import getLogger

from fastapi import responses, exceptions
from starlette.requests import Request

logger = getLogger("uvicorn")


async def validation_handler(
    request: Request, exc: exceptions.RequestValidationError
) -> responses.JSONResponse:
    error: Dict[str, Any] = exc.errors()[0]

    if len(error["loc"]) < 2:
        return responses.JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": f"body is empty",
            },
        )

    if error["type"] == "value_error.str.regex" and error["loc"][1] == "email":
        return responses.JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": f"please enter a valid email address",
            },
        )

    if error["type"] == "value_error.missing":
        logger.warn(
            f'\u001b[33m {request.url.path} - missing value : {error["loc"][1]}'
        )
        return responses.JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": f"wrong request",
            },
        )

    if error["type"] == "value_error.extra":
        return responses.JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": f"the field '{error['loc'][1]}' is unknown",
            },
        )

    if error["type"] == "value_error.any_str.min_length":
        return responses.JSONResponse(
            status_code=400, content={"message": error["msg"]}
        )

    return responses.JSONResponse(
        status_code=400, content={"code": 400, "message": "unknown validation error"}
    )

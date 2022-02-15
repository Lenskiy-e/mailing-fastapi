from fastapi.responses import JSONResponse
from fastapi import Request


class FailedRequestException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


def failed_request_exception_handler(request: Request, exception: FailedRequestException):
    return JSONResponse(
        status_code=500,
        content={
            'error': 'Auth request failed'
        }
    )


def unauthorized_exception_handler(request: Request, exception: FailedRequestException):
    return JSONResponse(
        status_code=401,
        content={
            'error': 'Auth failed'
        }
    )
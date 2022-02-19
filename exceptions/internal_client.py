from fastapi.responses import JSONResponse
from fastapi import Request, status


class FailedRequestException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


def failed_request_exception_handler(request: Request, exception: FailedRequestException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'error': 'Auth request failed'
        }
    )


def unauthorized_exception_handler(request: Request, exception: FailedRequestException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            'error': 'Auth failed'
        }
    )
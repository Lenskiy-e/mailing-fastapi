from fastapi import Request, status
from fastapi.responses import JSONResponse


class AuthKeyHeaderNotFound(Exception):
    pass


def auth_key_header_not_found_exception_handler(request: Request, exception: AuthKeyHeaderNotFound):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            'error': 'auth-key header not found!'
        }
    )
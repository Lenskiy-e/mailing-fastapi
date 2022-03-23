from fastapi import Request, status
from fastapi.responses import JSONResponse


class InvalidStatusToChange(Exception):
    def __init__(self, status_name: str):
        self.status_name = status_name


class SmsLengthLimitExceeded(Exception):
    pass


def invalid_status_to_change_exception_handler(request: Request, exception: InvalidStatusToChange):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'error': f"status {exception.status_name} can't be changed!"
        }
    )


def sms_length_limit_exceeded_handler(exception: SmsLengthLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'error': "Sms limit exceeded!"
        }
    )

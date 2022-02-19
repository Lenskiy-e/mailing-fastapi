from fastapi import Request
from fastapi.responses import JSONResponse


class GroupBelongsToAffiliateException(Exception):
    def __init__(self, group_id: int, affiliate_id: int):
        self.group = group_id
        self.affiliate = affiliate_id


class GroupIsNotNamed(Exception):
    def __init__(self, group_id: int):
        self.group = group_id


def group_belongs_to_affiliate_exception_handler(request: Request, exception: GroupBelongsToAffiliateException):
    return JSONResponse(
        status_code=403,
        content={
            'error': f'Group {exception.group} doesn\'t belongs to affiliate {exception.affiliate}'
        }
    )


def group_is_not_named_exception_handler(request: Request, exception: GroupIsNotNamed):
    return JSONResponse(
        status_code=400,
        content={
            'error': f'Group {exception.group} is not named'
        }
    )
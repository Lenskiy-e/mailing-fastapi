from fastapi import FastAPI
from db.database import engine
from models import group, mailing
from api.routes import phone as phone_routes, group as group_routes
from exceptions import internal_client as internal_client_exceptions, group as group_exceptions

app = FastAPI()


app.include_router(group_routes.router)
app.include_router(phone_routes.router)

group.Base.metadata.create_all(engine)
mailing.Base.metadata.create_all(engine)

app.add_exception_handler(
    internal_client_exceptions.FailedRequestException,
    internal_client_exceptions.failed_request_exception_handler
)

app.add_exception_handler(
    internal_client_exceptions.UnauthorizedException,
    internal_client_exceptions.unauthorized_exception_handler
)

app.add_exception_handler(
    group_exceptions.GroupBelongsToAffiliateException,
    group_exceptions.group_belongs_to_affiliate_exception_handler
)

app.add_exception_handler(
    group_exceptions.GroupIsNotNamed,
    group_exceptions.group_is_not_named_exception_handler
)

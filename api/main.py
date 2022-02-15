from fastapi import FastAPI
from db.database import engine
from models import group, mailing
from api.routes import phone as phone_routes, group as group_routes
from exceptions import internal_client

app = FastAPI()


app.include_router(group_routes.router)
app.include_router(phone_routes.router)

group.Base.metadata.create_all(engine)
mailing.Base.metadata.create_all(engine)

app.add_exception_handler(
    internal_client.FailedRequestException,
    internal_client.failed_request_exception_handler
)

app.add_exception_handler(
    internal_client.UnauthorizedException,
    internal_client.unauthorized_exception_handler
)

from fastapi import FastAPI
from db.database import engine
from models import group, mailing, phone
from routes import group as group_routes, phone as phone_routes

app = FastAPI()


app.include_router(group_routes.router)
app.include_router(phone_routes.router)

group.Base.metadata.create_all(engine)
mailing.Base.metadata.create_all(engine)
phone.Base.metadata.create_all(engine)

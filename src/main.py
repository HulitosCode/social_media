from fastapi import FastAPI

from .api import router
from .database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='Social Media App',
    description='Engine Behind Social Media App',
    version='0.1',
)
app.include_router(router)

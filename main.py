from fastapi import FastAPI #if not installed pip install fastapi
from fastapi.middleware.cors import CORSMiddleware

#selfcreated classes
from router import *


app = FastAPI()

#include all routers
app.include_router(person.router)
app.include_router(freeAsset.router)
app.include_router(income.router)


# Server starten: uvicorn main:app --reload

from fastapi import FastAPI #if not installed pip install fastapi
from fastapi.middleware.cors import CORSMiddleware

#import all generated classes
from router import *
from generalClasses import *

app = FastAPI()

#include all routers
app.include_router(person.router)
app.include_router(freeAsset.router)
app.include_router(income.router)
app.include_router(expense.router)


# Server starten: uvicorn main:app --reload

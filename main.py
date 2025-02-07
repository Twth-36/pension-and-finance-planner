from fastapi import FastAPI #if not installed pip install fastapi
from fastapi.middleware.cors import CORSMiddleware

#import all generated classes
from router import *
from generalClasses import *

# Start app
app = FastAPI()

#include all routers
app.include_router(credit.router)
app.include_router(expense.router)
app.include_router(freeAsset.router)
app.include_router(income.router)
app.include_router(incomeTaxPos.router)
app.include_router(manualIncomeTaxPos.router)
app.include_router(mainRouter.router)
app.include_router(pensionFund.router)
app.include_router(person.router)
app.include_router(pillar3a.router)
app.include_router(realEstate.router)
app.include_router(scenario.router)

# Server starten: uvicorn main:app --reload

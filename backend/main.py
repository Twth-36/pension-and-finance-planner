from contextlib import asynccontextmanager
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

#import all generated classes
from router import *
from generalClasses import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: all modules are loaded here.
    # Import Income and Cashflow for initialization within the lifespan function to avoid circular dependencies.
    from router.income import Income
    from router.cashflow import Cashflow
    from router.expense import Expense

    # Initialize generally needed positions for every plan
    # here not in the classes because of (1) circular imports, (2) mutliple objects get used by multiple variables of other classes
    savingCF = Cashflow.create(name="Einkommensüberschuss / -defizit")
    Expense.cashflowPos = savingCF


    yield  # Application runs until shutdown is triggered

    #Optional Code before shutting down TODO ask if saved?



# Start app
app = FastAPI()

#include all routers
app.include_router(cashflow.router)
app.include_router(credit.router)
app.include_router(expense.router)
app.include_router(freeAsset.router)
app.include_router(income.router)
app.include_router(incomeTaxPos.router)
app.include_router(manualExpense.router)
app.include_router(manualIncome.router)
app.include_router(manualIncomeTaxPos.router)
app.include_router(mainRouter.router)
app.include_router(pensionFund.router)
app.include_router(person.router)
app.include_router(pillar3a.router)
app.include_router(realEstate.router)
app.include_router(scenario.router)





# Server starten: uvicorn main:app --reload



from fastapi import FastAPI #if not installed pip install fastapi
from fastapi.middleware.cors import CORSMiddleware

#selfcreated classes
from router import *


app = FastAPI()

# Allow all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(person.router)
app.include_router(freeAsset.router)


# Server starten: uvicorn main:app --reload

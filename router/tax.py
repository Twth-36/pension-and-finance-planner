""" Router for all tax purposes (not for detailed calculations --> see folder tax)"""

from enum import Enum
from fastapi import APIRouter
from pydantic import BaseModel

from router.person import *

class Confession(Enum):
    "keine/andere" = 0
    "röm-kath" = 1
    "ev-ref" = 2

class Canton(Enum):
    "BE" = 1
    "BS" = 2



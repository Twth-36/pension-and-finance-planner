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

class taxSubject:
    canton: Canton
    person: Optional[Person] = None
    confession: Optional[Confession] = 0

    # Class-attributes
    instanceDic: ClassVar[dict] = {}
    
    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "taxSubject":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic
        return obj


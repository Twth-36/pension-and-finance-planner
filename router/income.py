""" Class Income for planning all possible incomes except automatic generated """

from planningposition import *
from scenario import *
from person import*

class Income(Planningposition):
    name: str
    person_id: int
    
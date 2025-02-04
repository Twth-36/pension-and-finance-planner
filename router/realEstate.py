""" realEstates inclusive mortgages  """

from planningposition import *
from scenario import *
from person import*

class RealEstate(Planningposition):
    realEstatesList = []
    realEstatesCounter = 0

    def __init__(self, name, initialValue, person, taxValue, taxRate):
        super().__init__(RealEstate.realEstatesCounter, name, initialValue, person)
        self.changeHistory = []
        self.taxValue = taxValue
        self.taxRate = taxRate
        RealEstate.realEstatesCounter += 1
        RealEstate.realEstatesList.append(self)


class Mortgage(Planningposition):
    mortgagesList = []
    mortgagesCounter = 0

    def __init__(self, name, initialValue, person, mortgageObj: RealEstate, interestRate: float, expirydate, refinInterestRate):
        super().__init__(Mortgage.mortgagesCounter, name, initialValue, person)
        self.mortgageObj = mortgageObj
        self.interestRate = interestRate
        self.expirydate = expirydate
        self.refinInterestRate = refinInterestRate
        self.changeHistory = []
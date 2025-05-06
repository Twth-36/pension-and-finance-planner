from backend.classes.cashflow import Cashflow
from backend.classes.incomeTaxPos import IncomeTaxPos

from backend.classes.manualIncomeTaxPos import ManualIncomeTaxPos
from backend.classes.person import Person
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario
from backend.classes.taxes import Taxes
from backend.tax.capPayoutTax import clc_capPayoutTax
from backend.tax.incomeTax import clc_incomeTax
from backend.tax.taxproperties import Taxation
from backend.utils.monthYear import MonthYear


def exe_clcIncomeTax(period: MonthYear, scenario: Scenario):

    person_counter = len(Person.instanceDic)

    # get Expense pos
    taxExpense_pos = Planningposition.get_item(
        period=period, scenario=scenario, list=Taxes.incTaxExpense.planValue
    )

    # case if incometax can get calculated together and must not be distinghuished by person
    if person_counter == 1 or Taxes.taxation == Taxation.together:
        person1 = next(iter(Person.instanceDic.values()))
        person2 = (
            list(Person.instanceDic.values())[1]
            if len(Person.instanceDic) > 1
            else None
        )
        income = 0
        for m in MonthYear.create_range(
            startDate=MonthYear(month=1, year=period.year), endDate=period
        ):
            for obj in list(ManualIncomeTaxPos.instanceDic.values()) + list(
                IncomeTaxPos.instanceDic.values()
            ):

                obj_pos = Planningposition.get_item(
                    period=m, scenario=scenario, list=obj.planValue
                )
                if obj_pos:
                    income += obj_pos.value

        taxExpense_pos.value -= clc_incomeTax(
            income=income,
            canton=Taxes.canton,
            place=Taxes.place,
            taxation=Taxes.taxation,
            conf1=person1.conf,
            conf2=person2.conf if person2 else None,
            childrenCnt=Taxes.childrenCnt,
        )
    else:  # case if multiple person with "alleinstehenden Satz"

        for p in Person.instanceDic.values():
            income = 0
            for m in MonthYear.create_range(
                startDate=MonthYear(month=1, year=period.year), endDate=period
            ):
                for obj in list(ManualIncomeTaxPos.instanceDic.values()) + list(
                    IncomeTaxPos.instanceDic.values()
                ):
                    obj_pos = Planningposition.get_item(
                        period=m, scenario=scenario, list=obj.planValue
                    )

                    if obj_pos:
                        if obj.person == p:
                            income += obj_pos.value

                        elif (
                            obj.person is None
                        ):  # case if only a part need to be accounted for the person
                            income += obj_pos.value / person_counter

            taxExpense_pos.value -= clc_incomeTax(
                income=income,
                canton=Taxes.canton,
                place=Taxes.place,
                taxation=Taxes.taxation,
                conf1=p.conf,
                childrenCnt=Taxes.childrenCnt,
            )


def exe_clcCapPayoutTax(period: MonthYear, scenario: Scenario):

    person_counter = len(Person.instanceDic)

    # get Expense pos
    taxExpense_pos = Planningposition.get_item(
        period=period, scenario=scenario, list=Taxes.capPayoutTaxExpense.planValue
    )

    # case if incometax can get calculated together and must not be distinghuished by person
    if person_counter == 1 or Taxes.taxation == Taxation.together:
        person1 = next(iter(Person.instanceDic.values()))
        person2 = (
            list(Person.instanceDic.values())[1]
            if len(Person.instanceDic) > 1
            else None
        )
        payoutValue = 0
        for m in MonthYear.create_range(
            startDate=MonthYear(month=1, year=period.year), endDate=period
        ):
            for obj in Cashflow.instanceDic.values():

                obj_pos = Planningposition.get_item(
                    period=m, scenario=scenario, list=obj.planValue
                )
                if obj_pos:
                    payoutValue += obj_pos.value * obj.taxablePortion / 100

        taxExpense_pos.value -= clc_capPayoutTax(
            payoutValue=payoutValue,
            canton=Taxes.canton,
            place=Taxes.place,
            taxation=Taxes.taxation,
            conf1=person1.conf,
            conf2=person2.conf if person2 else None,
            childrenCnt=Taxes.childrenCnt,
        )
    else:  # case if multiple person with "alleinstehenden Satz"

        for p in Person.instanceDic.values():
            payoutValue = 0
            for m in MonthYear.create_range(
                startDate=MonthYear(month=1, year=period.year), endDate=period
            ):
                for obj in Cashflow.instanceDic.values():

                    obj_pos = Planningposition.get_item(
                        period=m, scenario=scenario, list=obj.planValue
                    )
                    if obj_pos:
                        if obj.person == p:
                            payoutValue += obj_pos.value * obj.taxablePortion / 100

                        elif (
                            obj.person is None
                        ):  # case if only a part need to be accounted for the person
                            payoutValue += (
                                obj_pos.value
                                * obj.taxablePortion
                                / 100
                                / person_counter
                            )

            taxExpense_pos.value -= clc_incomeTax(
                payoutValue=payoutValue,
                canton=Taxes.canton,
                place=Taxes.place,
                taxation=Taxes.taxation,
                conf1=p.conf,
                childrenCnt=Taxes.childrenCnt,
            )

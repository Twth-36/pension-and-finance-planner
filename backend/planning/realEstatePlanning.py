from backend.classes.planningposition import Planningposition
from backend.classes.realEstate import RealEstate
from backend.classes.scenario import Scenario
from backend.utils.monthYear import MonthYear


def exe_realEstatePlanning(period: MonthYear, scenario: Scenario):

    # work through every object in instanceDic:
    for obj in RealEstate.instanceDic.values():

        # create new Planningposition for planValue
        new_pos = Planningposition(scenario=scenario, period=period)

        # find previous Planningposition planValue
        prev_pos = Planningposition.get_item(
            period=period.nextMonth(-1), scenario=scenario, list=obj.planValue
        )

        if prev_pos is None:  # case if first planningMonth
            new_pos.value = obj.baseValue
        else:
            new_pos.value = prev_pos.value

        """handle pruchase"""
        purchase_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.purchase
        )
        if purchase_pos:  # when purchase_pos is available

            # get planValue-position of CF-position
            purchaseCF_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.purchaseCF.planValue
            )
            purchaseCF_pos.value -= purchase_pos.value  # payment of the purchase

            new_pos.value += purchase_pos.value  # add value

            if purchase_pos.description:
                if new_pos.description:
                    new_pos.description += purchase_pos.description
                else:
                    new_pos.description = purchase_pos.description

        """handle renovation"""
        renovation_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.renovations
        )
        if renovation_pos:  # when purchase_pos is available
            # get planValue-position of renovationExpense
            renovationExpense_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.renovationExpense.planValue
            )
            renovationExpense_pos.value -= (
                renovation_pos.value
            )  # add expense for renovation

            if renovation_pos.description:
                if new_pos.description:
                    new_pos.description += "; " + renovation_pos.description
                else:
                    new_pos.description = renovation_pos.description

        """handle sale"""
        sale_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.sale
        )
        if sale_pos:
            # get planValue-position of saleCF
            saleCF_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.saleCF.planValue
            )
            saleCF_pos.value += sale_pos.value  # add payment from sale

            # set planValue to zero
            new_pos.value = 0

            if sale_pos.description:
                if new_pos.description:
                    new_pos.description += "; " + sale_pos.description
                else:
                    new_pos.description = sale_pos.description

        """handle taxValue"""
        # create new Planningposition for taxValue
        new_TaxValuepos = Planningposition(scenario=scenario, period=period)

        # find previous Planningposition planValue
        prev_TaxValuepos = Planningposition.get_item(
            period=period.nextMonth(-1), scenario=scenario, list=obj.taxPlanValue
        )

        if prev_TaxValuepos is None:  # case if first planningMonth
            new_TaxValuepos.value = obj.baseTaxValue if obj.baseTaxValue else 0
        else:
            new_TaxValuepos.value = prev_TaxValuepos.value

        # if there was a sale set taxValue to zero
        if sale_pos:
            new_TaxValuepos.value = 0

        # check if fixValue exisist and overwrite it
        taxFixValue_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.taxFixValue
        )
        if taxFixValue_pos:
            new_TaxValuepos.value = taxFixValue_pos.value
            new_TaxValuepos.description = taxFixValue_pos.description

        # add new position to taxPlanValue
        new_TaxValuepos.add_toList(obj.taxPlanValue)

        # calculate taxes and add it to the expense pos if end of year
        # get planValue position of taxExpense
        if period.month == 12:
            taxExpense_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.taxExpense.planValue
            )

            taxExpense_pos.value += (
                new_TaxValuepos.value * obj.taxRate / 100 if obj.taxRate else 0
            )

        """handle imputedRental"""
        # create new Planningposition for imputedRental
        new_imputedRentpos = Planningposition(scenario=scenario, period=period)

        # find previous Planningposition planValue
        prev_imputedRentpos = Planningposition.get_item(
            period=period.nextMonth(-1),
            scenario=scenario,
            list=obj.imputedRentalPlanValue,
        )

        if prev_imputedRentpos is None:  # case if first planningMonth
            new_imputedRentpos.value = (
                obj.baseImputedRentalValue if obj.baseImputedRentalValue else 0
            )
        else:
            new_imputedRentpos.value = prev_imputedRentpos.value

        # if there was a sale set imputedRental to zero
        if sale_pos:
            new_imputedRentpos.value = 0

        # check if fixValue exisist and overwrite it
        imputedRentFixValue_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.imputedRentalFixValue
        )
        if imputedRentFixValue_pos:
            new_imputedRentpos.value = imputedRentFixValue_pos.value
            new_imputedRentpos.description = imputedRentFixValue_pos.description

        # add new position to taxPlanValue
        new_imputedRentpos.add_toList(obj.imputedRentalPlanValue)

        # if end of year get incomeTaxPos and add imputedRental
        # get planValue of incomeTaxPos
        if period.month == 12:
            imputedRentIncomeTax_pos = Planningposition.get_item(
                period=period,
                scenario=scenario,
                list=obj.imputedRentalValueIncomeTaxPos.planValue,
            )
            imputedRentIncomeTax_pos.value += new_imputedRentpos.value
            if new_imputedRentpos.description:
                if imputedRentIncomeTax_pos.description:
                    imputedRentIncomeTax_pos.description += (
                        "; " + new_imputedRentpos.description
                    )
                else:
                    imputedRentIncomeTax_pos.description = (
                        new_imputedRentpos.description
                    )

        """handle maintenanceCost"""
        maintenanceExpense_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.maintenanceExpense.planValue
        )

        maintenanceExpense_pos.value += (
            new_pos.value * obj.maintCostRate / 100 / 12 if obj.maintCostRate else 0
        )

        # add new position to planValue of realEstate object
        new_pos.add_toList(obj.planValue)

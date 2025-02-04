""" Class for different scenarios in the planning """

class Scenario:

    scenarioList = []
    scenarioCounter = 0

    def __init__(self, name):
        self.name = name
        self.id = Scenario.scenarioCounter
        Scenario.scenarioCounter += 1
        Scenario.scenarioList.append(self)
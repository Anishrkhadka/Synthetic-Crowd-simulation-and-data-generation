import AgentsManager
import FileManager
import LogManager

class getCrowdSimulator:

    def __init__(self, InSettings):
        self.settings = InSettings
        self.agent = AgentsManager.getAgents(InSettings)
        self.agentList = None
        self.OutAgentList = None
        self.OutAgentsPosition = None
        self.OutAgentRotation = None

    def init(self):
        FileManager.cleanupSimulationResult(self.settings.getPathForSimulationResults())

        # self.agent.setSimulationSettings(self.settings)
        # self.agent.setTotalNumberOfAgents(self.settings.getTotalNumberOfAgentsForSimulation())

        self.agent.getGripMapAndItsProperties()
        self.agentList = self.agent.createAgentDetail()

    def run(self):
        import time
        start = time.time()
        self.OutAgentList, self.OutAgentsPosition, self.OutAgentRotation = self.agent.updateAgents(self.agentList)
        end = time.time()
        LogManager.displayLog(f'Total Time = {round(end - start)} Second', InColor='blue')

    def saveResult(self):
        FileManager.saveSimulationResultsToFile(self.OutAgentList,
                                                self.OutAgentsPosition,
                                                self.OutAgentRotation,
                                                self.settings,
                                                self.agent)

import Utility
import LogManager
import FileManager


class getSettings:

    def __init__(self):
        # -- For Perspective Extraction -- #
        self.backgroundImageName= None
        self.backgroundImage = None
        self.userDefinePointPath = None
        # self.IsDisplayPlotEnable = False

        # -- For Simulation -- #
        self.frameRate = 2
        self.frameNumber = 0
        self.outputFrameCount = 1
        self.timeRate = 0.03333333333
        self.totalNumberOfFrameForSimulation = 0
        self.startFrame = 1

        self.totalNumberOfAgents = 0

        self.gridMapUnitSize = 1
        self.gripMapFilePath = None

        self.maxDistanceForInAndOutForAgent = 1

        self.ratioXToYForGridPlaneScale = None

        self.pathForPerspectiveExtractionData = None
        self.pathForSimulationResults = None

    @staticmethod
    def setIsDisplayPythonWarningMsg(InBool):
        Utility.setIsDisplayWarningMsg(InBool)

    def setBackgroundImageForPerspectiveExtraction(self, InPath):
        splitImageExtension = InPath.split('.')
        if splitImageExtension[1] != 'png':
            # -- convertToPngFormat returns path to png instead of loading image --#
            self.backgroundImage =  Utility.convertToPngFormat(splitImageExtension)
        else:
            self.backgroundImage = InPath

    def getBackgroundImageForPerspectiveExtraction(self):
        return self.backgroundImage

    # def setIsDisplayPlotEnable(self, InBool):
    #     self.IsDisplayPlotEnable = InBool

    # def getIsDisplayPlotEnable(self):
    #     return self.IsDisplayPlotEnable

    def setPathForPerspectiveExtraction(self, InPath):
        self.backgroundImageName = InPath
        path = f'PerspectiveData/{InPath}'
        if FileManager.checkIfFileExist(path) is False:
            FileManager.createFolder(path)
        self.pathForPerspectiveExtractionData = path
        self.gripMapFilePath= f'{self.pathForPerspectiveExtractionData}gridMap.txt'
        self.userDefinePointPath = f'{self.pathForPerspectiveExtractionData}setOfPoints.txt'

    def getBackgroundImageName(self):
        return self.backgroundImageName

    def getPathForPerspectiveExtraction(self):
        return self.pathForPerspectiveExtractionData

    def setUserDefinePointPath(self, InPath):
        self.userDefinePointPath = InPath

    def getUserDefinePointPath(self):
        return self.userDefinePointPath

    def getTimeRate(self):
        return self.timeRate

    def setGridMapUnitSize(self, InGridMapSize):
        self.gridMapUnitSize = InGridMapSize

    def getGridMapUnitSize(self):
        return self.gridMapUnitSize

    def setFrameRateToExportToUnity(self, InFrameRate):
        self.frameRate = round(InFrameRate)
        LogManager.displayLog(InValue=self.frameRate, InName='Exporting to Unity at FPS')

    def getSimulationFrameRate(self):
        return self.frameRate

    def getInitialFrameNumber(self):
        return self.frameNumber

    def setTotalSimulationTimeInSecond(self, InSecond):
        self.totalNumberOfFrameForSimulation = InSecond * self.frameRate * self.frameRate
        LogManager.displayLog(InValue=InSecond * self.frameRate,
                              InName='Total Simulated Frame')

    # def setTotalNumberOfFrameForSimulation(self,InNumber):
    #     self.totalNumberOfFrameForSimulation = InNumber
    #     LogManager.log(InValue=round(self.totalNumberOfFrameForSimulation/self.frameRate), InName='Total Simulated Frame')

    def getTotalNumberOfFrameForSimulation(self):
        return self.totalNumberOfFrameForSimulation

    def getTotalNumberOfSimulatedFrame(self):
        return round(self.totalNumberOfFrameForSimulation / self.frameRate) - 1

    def setTotalNumberOfAgentsForSimulation(self, InTotalNo):
        self.totalNumberOfAgents = InTotalNo

    def getTotalNumberOfAgentsForSimulation(self):
        return self.totalNumberOfAgents

    def setMapUnitSize(self, InSize):
        self.gridMapUnitSize = InSize

    def getMapUnitSize(self):
        return self.gridMapUnitSize

    def setMaxDistanceForInAndOutForAgent(self, InValue):
        self.maxDistanceForInAndOutForAgent = InValue

    def getMaxDistanceForInAndOutForAgent(self):
        return self.maxDistanceForInAndOutForAgent

    def setGridMapFilePath(self, InFilePath):
        self.gripMapFilePath = InFilePath

    def getGridMapFilePath(self):
        return self.gripMapFilePath

    def getRatioXToYForGridPlaneScale(self):
        point = FileManager.loadTextFile(self.userDefinePointPath)
        self.ratioXToYForGridPlaneScale = Utility.getEuclideanDistance(point[5, :], point[1, :]) / \
                                          Utility.getEuclideanDistance(point[6, :], point[1, :])
        return self.ratioXToYForGridPlaneScale

    def setPathForSimulationResults(self, InPath):
        self.pathForSimulationResults = InPath

    def getPathForSimulationResults(self):
        return self.pathForSimulationResults

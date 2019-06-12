import PerspectiveManager
import CrowdSimulationManager
import SettingManager
import playground
import crowdCountingHelper

imageCollection = 'Data/images/PedistrianDetection_image/'
backgroundImageName, backgroundImageFileType = 'IMG_1640', 'JPG'

fpsPal = 24/8
fpsNtsc = 30/6

totalAgent = 15
totalSimulationTime = 40


OutSettings = SettingManager.getSettings()
OutSettings.setIsDisplayPythonWarningMsg(False)

OutSettings.setBackgroundImageForPerspectiveExtraction(f"{imageCollection}{backgroundImageName}.{backgroundImageFileType}")
OutSettings.setPathForPerspectiveExtraction(f'{backgroundImageName}/')

OutSettings.setFrameRateToExportToUnity(fpsNtsc)
OutSettings.setTotalSimulationTimeInSecond(totalSimulationTime)
OutSettings.setTotalNumberOfAgentsForSimulation(totalAgent)
OutSettings.setPathForSimulationResults(f'{backgroundImageName}_{totalAgent}_{totalSimulationTime}_{round(fpsNtsc)}/')
OutSettings.setGridMapUnitSize(1)
OutSettings.setMaxDistanceForInAndOutForAgent(30)

perspective = PerspectiveManager.getPerspective(OutSettings)
perspective.init()
perspective.run(InIsGetPerspective=True, InIsGetGridMap=True,  InIsPlotDisplay=False)

# crowdSimulation = CrowdSimulationManager.getCrowdSimulator(OutSettings)
# crowdSimulation.init()
# crowdSimulation.run()
# crowdSimulation.saveResult()


# import FileManager
# FileManager.sendFileToUnity(backgroundImageName,
#                             f'{backgroundImageName}_{totalAgent}_{totalSimulationTime}_{round(fpsNtsc)}',
#                             imageCollection,IsSendSave=False)

# playground.checkHeadPositionOfAvatar(145, 'Brussels_the_Grand-Place_5_1000_30_5', 'Ori')

# #
# crowdCountingHelper.generatedDensityMap(145,'Brussels_the_Grand-Place_5_1000_30_5','Ori')

# # playground.checkHeadPositionOfAvatar(145, 'Brussels_the_Grand-Place_5_1000_30_5', 'Ori')
# # playground.checkHeadPositionOfAvatar(35,'Lemgo_1_1200_45_5', 'Ori')
# # playground.checkHeadPositionOfAvatar(135,'Markt_1_1000_30_5', 'Ori')

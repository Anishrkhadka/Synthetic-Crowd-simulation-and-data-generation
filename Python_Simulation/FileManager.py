import LogManager
import numpy as np
import Utility
import cv2
import MapManager
from pathlib import Path
import os
import shutil




def saveSimulationResultsToFile(InAgentList, InPosition, InRotation, InSettings, InAgents):
    path = f'SimulationResult/{InSettings.getPathForSimulationResults()}'
    # -- Write Agents.txt with ID and Radius info --#
    file = open(f'{path}AgentIDAndRadius.txt', 'w')
    file.write('ID\tRadius \n')
    for i in range(0, InSettings.getTotalNumberOfAgentsForSimulation()):
        file.write(f"{i}\t{np.squeeze(InAgentList[:][i]['Radius'])}\n")
    file.close()

    # -- Write Pos and Rot in file -- #pip insta
    saveToTextFile(InFileName=f'{path}AgentPosition.txt', InValue=InPosition.astype(np.float))
    saveToTextFile(InFileName=f'{path}AgentRotation.txt', InValue=InRotation.astype(np.float))

    # -- Write Sets -- #
    file = open(f'{path}SimulationSetting.txt', 'w')
    file.write(f"{InSettings.getTotalNumberOfSimulatedFrame()}\n")
    file.write(f"{InSettings.getTotalNumberOfAgentsForSimulation()}\n")
    file.write(f"{InSettings.getRatioXToYForGridPlaneScale()}\n")
    file.write(f"{InSettings.getMapUnitSize()}\n")
    file.write(f'{InSettings.getPathForSimulationResults()[:-1]}\n')
    file.write(f'{InSettings.getBackgroundImageName()[:-1]}')
    file.close()

    # -- Save_Brussels_the_Grand-Place_5.txt -- #
    file = open(f'{path}Save_{InSettings.getBackgroundImageName()[:-1]}.txt', 'w')
    cameraXPos = cameraYPos = MapManager.getGridMapFromFile(InSettings.getGridMapFilePath(), InDisplayLog=False).shape[
                                  0] / 2
    file.write(f"{cameraXPos}\n")
    file.write(f"{cameraYPos / 2}\n")
    file.write(f"{0}\n")
    cameraXRot = 30
    file.write(f"{cameraXRot}\n")
    file.write(f"{0}\n")
    file.write(f"{0}\n")
    cameraFOV = 55
    file.write(f"{cameraFOV}\n")
    cameraBackgroundScale = 1
    file.write(f"{cameraBackgroundScale}\n")
    avaterScale = 1
    file.write(f"{avaterScale}\n")
    avatarPosition = cameraXPos
    file.write(f"{avatarPosition}\n")
    file.write(f"{0}\n")
    file.write(f"{0}\n")
    animationSpeed = 12
    file.write(f"{animationSpeed}\n")
    file.close()
    # import matplotlib.pyplot as plt
    # imageWidth = plt.imread(InSettings.getBackgroundImageForPerspectiveExtraction()).shape[1]
    # cameraFocalLength = getCameraFocalLengthEstimation(InImageWidth=imageWidth, InFOV=cameraFOV)
    # file.write(f'{cameraFocalLength}')

    saveGridMapToImage(InFileName=f'{path}map.png', InGridMapArray=InAgents.gridMapForPathFinder)

def cleanupSimulationResult(InSimulationResultPath):
    LogManager.displayLog(f'Cleaning /SimulationResultfolder')
    simulationResultPath = f'SimulationResult/{InSimulationResultPath}'
    try:
        shutil.rmtree(simulationResultPath)
    except:
        LogManager.displayLog(f'Folder {simulationResultPath} not found!')

    createFolder(simulationResultPath)

def sendFileToUnity(InImageName, InSimulatedFolderPath,
                    InBackgroundImageFolderPath,
                    IsSendSave=False, IsResultFolderDelete=False):

    # -- len(Python_Simulation) = 17-- #
    basePath = os.getcwd()[:-17]

    targetPath = f'{basePath}Unity_Visual/Compositing/'
    simulatedFolderPath = f'{basePath}Python_Simulation/SimulationResult/{InSimulatedFolderPath}/'

    backgroundImageFolder = f'{basePath}Python_Simulation/{InBackgroundImageFolderPath}'
    backgroundImageForUnity = [streetImage for streetImage in os.listdir(backgroundImageFolder) if streetImage.endswith(".jpg")]
    backgroundImageForUnity.sort()

    # -- find the crowd clean version of background in image folder --#
    crowdCleanedBackgroundImage = [mask for mask in os.listdir(backgroundImageFolder) if
                                   mask == f'{mask[0:len(backgroundImageForUnity[0].split(".")[0])]}_crowdCleanVersion.png']
    crowdCleanedBackgroundImage.sort()

    # -- Get the list of all txt file and image from simulation folder -- #
    moveSimulationResultToUnity = [moveFiles for moveFiles in os.listdir(simulatedFolderPath) if
                                   moveFiles.endswith(".txt")]
    moveSimulationResultToUnity.sort()

    moveGridMapImage = [moveFiles for moveFiles in os.listdir(simulatedFolderPath) if moveFiles.endswith(".png")]

    # -- if save files is false don't sent it to unity i.e remove it from the move list -- #
    if IsSendSave is False:
        moveSimulationResultToUnity.remove(f'Save_{InImageName}.txt')

    # -- Remove the previous resources files --#
    try:
        shutil.rmtree(f'{targetPath}Assets/Resources/')
    except:
        LogManager.displayLog(f'Folder {targetPath}Assets/Resources/ not found!')

    createFolder(f'{targetPath}Assets/Resources/')


    # -- Copy the file to unity simulation folder -- #
    # -- copy txt -- #
    for i in range(len(moveSimulationResultToUnity)):
        LogManager.displayLog(f'Copying file {moveSimulationResultToUnity[i]} to Unity->Data->Resource Folder')
        shutil.copy(f'{simulatedFolderPath}{moveSimulationResultToUnity[i]}',
                    f'{targetPath}Assets/Data/SimulationResult/')

    # -- copy image -- #
    for i in range(len(moveGridMapImage)):
        LogManager.displayLog(f'Copying file {moveGridMapImage[i]} to  Unity->Assets->Resource Folder')
        shutil.copy(f'{simulatedFolderPath}{moveGridMapImage[i]}', f'{targetPath}Assets/Resources/')

    # -- delete unity result folder -- #
    if IsResultFolderDelete:
        unityVisualisationResultPath = f'{basePath}Unity_Visual/Compositing/Result/'
        try:
            shutil.rmtree(unityVisualisationResultPath)
        except:
            LogManager.displayLog(f'Folder {unityVisualisationResultPath} not found!')

    if not crowdCleanedBackgroundImage:
        LogManager.displayLog(f'No crowd clean image found in {InBackgroundImageFolderPath}', InColor='red')
        LogManager.displayLog('Will try to clean crowd from background if Mask image is present!')
        if Utility.cleanCrowdFromBackground(backgroundImageFolder):
            crowdCleanedBackgroundImage = [mask for mask in os.listdir(backgroundImageFolder)
                                           if mask == f'{mask[0:len(backgroundImageForUnity[0].split(".")[0])]}_crowdCleanVersion.png']
            crowdCleanedBackgroundImage.sort()
        else:
            return

    for i in range(len(crowdCleanedBackgroundImage)):
        LogManager.displayLog(
            f'Copying file {crowdCleanedBackgroundImage[i]} to Unity->Assets->Resource->backgroundImage Folder', InColor='green')
        shutil.move(f'{backgroundImageFolder}{crowdCleanedBackgroundImage[i]}',
                    f'{targetPath}Assets/Resources/background_{i}.png')


def renameFileSequence(InPath, InSearchByExt, InSequenceName):
    fileList = [fileName for fileName in os.listdir(InPath) if fileName.endswith(f".{InSearchByExt}")]
    fileList.sort()

    for i in range(0,len(fileList)):
        extension = fileList[i].split(".")
        name = f'{InPath}{InSequenceName}_{i+1:05}.{extension[1]}'
        LogManager.displayLog( f'Rename file {fileList[i]} to {name} ')
        shutil.move(f'{InPath}{fileList[i]}',name )


def loadTextFile(InName):
    if checkIfFileExist(InName):
        return np.loadtxt(InName)
    else:
        # -- Stop the python -- /
        import sys
        sys.exit(f'Could not find {InName}')

def createFolder(InPath):
    # -- Create folder -- #
    import os
    if not os.path.exists(InPath):
        os.makedirs(InPath)
        LogManager.displayLog(f'Folder {InPath} is created',InColor='green')

# -- saveToTextFile by default use tab to separate the data -- #
def saveToTextFile(InFileName, InValue, InDelimiter='\t'):
    np.savetxt(InFileName, InValue, delimiter=InDelimiter, fmt='%f')

    if checkIfFileExist(InFileName):
        LogManager.displayLog(f"{InFileName} Saved")
        return True
    return False

def checkIfFileExist(InName):
    file = Path(InName)
    if file.is_file():
        return True
    return False


def saveGridMapToImage(InFileName, InGridMapArray, IsFlipMap=False):
    x1 = Utility.getNormalisedMatrix(InGridMapArray)

    x1 = 255 * x1  # Now scale by 255
    x1 = np.rot90(np.fliplr(x1))
    img = x1.astype(np.uint8)
    if IsFlipMap:
        img = cv2.flip(img, 0)
    cv2.imwrite(InFileName, img)

def removeFile(InPath):
    os.remove(InPath)



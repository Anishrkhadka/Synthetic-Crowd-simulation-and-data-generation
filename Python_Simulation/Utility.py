import math
import warnings
import matplotlib.pyplot as plt

import numpy as np
import cv2
import os

from PIL import Image

import LogManager
import FileManager
import matplotlib as mpl
import h5py
import shutil

def setIsDisplayWarningMsg(InValue):
    if InValue is False:
        warnings.filterwarnings("ignore")
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# -- Convert image to png format and return the png file path -- #
def convertToPngFormat(InPath):
    im = Image.open(f'{InPath[0]}.{InPath[1]}')
    pngPath= f'{InPath[0]}.png'
    im.save(pngPath)

    return pngPath


def getPointFromUser(InIndex=None):
    return np.asarray(plt.ginput(1, timeout=-1))


def plotPoint(InX, InY, Informat='ro', InMarkerSize=1):
    # plt.plot(InX, InY)
    plt.plot(InX, InY, Informat, markersize=InMarkerSize)

def plotBox(InX, InY, Informat='r'):
    plt.plot(InX, InY, Informat, markersize=1)
    # plt.fill(InX, InY, Informat, lw=2, alpha=0.8)

def plotLine(InX, InY, InLinewidth=2, Informat='ro'):
    plt.plot(InX, InY)


def plotImage(InImageArray, InFileName=None):
    plt.imshow(InImageArray, interpolation='nearest')
    plt.gca().invert_yaxis()
    plt.show()

    if InFileName:
        plt.imsave(InFileName, InImageArray)
        plt.close()

def plotPointOnImage(InImage, InX, InY, InIsFlip=False, InMarkerSize=1):
    # fig, ax = plt.subplots()
    # im = ax.imshow(InImage)
    if InIsFlip:
        plt.gca().invert_yaxis()
        # plt.gca().invert_xaxis()
    plotPoint(InX, InY, "o", InMarkerSize)

def plotPointOnImageAndSave(InImage, InX, InY, InIsFlip, InFileName=None):
        plotPointOnImage(InImage, InX, InY, InIsFlip)
        if InFileName:
            plt.savefig(InFileName,bbox_inches='tight')

# def saveImage(InFileName, InGridMapTOPathFinderFormat, IsFlipMap=False):
#     x1 = getNormalisedMatrix(InGridMapTOPathFinderFormat)
#
#     x1 = 255 * x1  # Now scale by 255
#     x1 = np.rot90(np.fliplr(x1))
#     img = x1.astype(np.uint8)
#     if IsFlipMap:
#         img = cv2.flip(img, 0)
#     cv2.imwrite(InFileName, img)


def getLineEquation(InPoints):
    OutLineEquation = np.zeros((1, 2), dtype=float)

    # -- Line Equation -- #
    # y = m*x + b
    # b = y-m*x
    # -- Point Slop Formula -- #
    # y - y1 = m(x-x1)
    # m = (x-x1)/(y-y1)

    # m = (x1 - x2) / (y1 - y2)
    # b = m * (0 - x2) + y2

    m = (InPoints[0, 1] - InPoints[1, 1]) / (InPoints[0, 0] - InPoints[1, 0])
    b = m * (0 - InPoints[1, 0]) + InPoints[1, 1]

    if np.isinf(m):
        LogManager.displayLog('LINE IS VERTICAL')
        m = InPoints[0, 0]
        b = np.inf

    OutLineEquation[0, 0] = m
    OutLineEquation[0, 1] = b

    return OutLineEquation


def getPointAlongLine(InLine, InPoint):
    m = InLine[0, 0]
    b = InLine[0, 1]

    OutX = None
    OutY = None

    if np.isinf(b):
        print('LINE IS VERTICAL')
    else:
        OutX = (InPoint[0] + (m * InPoint[1]) - (m * b)) / ((m ** 2) + 1)
        OutY = (m * OutX) + b

    return OutX, OutY


def getIntersectionPoint(InLineEquation):
    intercept = None
    x = None
    y = None

    # print(InLineEquation)

    if InLineEquation[0, 0] == InLineEquation[1, 0]:
        print('THE SLOPES OF THE LINE EQUATIONS ARE THE SAME, THEY ARE PARALLEL')
        intercept = False
        x = np.nan
        y = np.nan
        return intercept, x, y

    if np.sum(np.isinf(InLineEquation)) > 0:
        print('ONE OF THE LINES IS VERTICAL')
        intercept = True
        row, column = np.where(np.isinf(InLineEquation) > 0)
        x = InLineEquation[row, 0]

        if row == 1:
            y = (InLineEquation[1, 0] * InLineEquation[row, 0]) + InLineEquation[1, 1]
        else:
            y = (InLineEquation[0, 0] * InLineEquation[row, 0]) + InLineEquation(0, 1)
    else:
        intercept = True
        x = (InLineEquation[0, 1] - InLineEquation[1, 1]) / (InLineEquation[1, 0] - InLineEquation[0, 0])
        y = (InLineEquation[0, 0] * x) + InLineEquation[0, 1]

    return intercept, x, y


def getVectorMagnitude(InVector):
    return np.linalg.norm(InVector)


def getNormaliseData(InData, InDataMin, InDataMax):
    return (InData - InDataMin) / (InDataMax - InDataMin)


def getAtan2(InX, InY):
    return math.atan2(InY, InX)


def getWrapTo360(InRotation):
    OutRotation = InRotation

    positiveInput = OutRotation > 0
    OutRotation = np.mod(OutRotation, 360)
    if OutRotation == 0 and positiveInput:
        OutRotation = 360

    return OutRotation


# def checkIfFileExist(InName):
#     file = Path(InName)
#     if file.is_file():
#         return True
#     return False

# -- saveToTextFile by default use tab to separate the data -- #
# def saveToTextFile(InFileName, InValue, InDelimiter='\t'):
#     np.savetxt(InFileName, InValue, delimiter=InDelimiter, fmt='%f')
#
#     if checkIfFileExist(InFileName):
#         LogManager.displayLog(f"{InFileName} Saved")
#         return True
#     return False
#
# def loadTextFile(InName):
#     if checkIfFileExist(InName):
#         return np.loadtxt(InName)
#     else:
#         # -- Stop the python -- /
#         import sys
#         sys.exit(f'Could not find {InName}')

# -- returns the [row,col] when shape of matrix and index i for a cell is given -- #
# -- e.g [row, col] = matrix.shape, i, where i, is total element in matrix -- #
def ind2sub(shapeOFMatrix, index):
    return np.unravel_index(index, shapeOFMatrix, order='F')


def getListOfRandomNo(InRange, InNumberOfValue, InIsRepeatNo=False):
    return np.random.choice(range(InRange), InNumberOfValue, replace=InIsRepeatNo)


def mod(x, y):
    return x - np.floor(float(x) / y) * y
    # x - floor(x. / y). * y


def getRotateVector(InVector, InRotationAngle):
    OutRotationVector = np.array([0, 0], dtype='float')
    rotationAngle = np.deg2rad(InRotationAngle)

    OutRotationVector[0] = InVector[0] * np.cos(rotationAngle) - InVector[1] * np.sin(rotationAngle)
    OutRotationVector[1] = InVector[0] * np.sin(rotationAngle) + InVector[1] * np.cos(rotationAngle)

    return OutRotationVector


def getNormalisedVector(InVector):
    sqlen = np.dot(InVector, InVector)
    # -- if sqlen is 0 then dividing it any no will be inf so set sqlen to 0
    if sqlen == 0:
        return InVector * 0
    else:
        return InVector * (1.0 / np.sqrt(sqlen))


def getNormalisedMatrix(InMatrix):
    xmax, xmin = InMatrix.max(), InMatrix.min()
    InMatrix = (InMatrix - xmin) / (xmax - xmin)
    return InMatrix


def getEuclideanDistance(InVector1, InVector2):
    temp = InVector1 - InVector2
    temp = np.concatenate((temp, 0), axis=None)

    return np.linalg.norm(temp)


#
# def getRayIntersect(InRayOriginPoint, InRayEndPoint, InGridMapProperties, InRayID):
#     OutGripMapProperties = InGridMapProperties.copy()
#     hitsList = []
#     OutSeenList = []
#     ts = np.array([0])
#
#     LAB = getEuclideanDistance(InRayOriginPoint, InRayEndPoint)
#
#     # -- Direction from Vector InRayOriginPoint to InRayEndPoint -- #
#     Dx = (InRayEndPoint[0] - InRayOriginPoint[0]) / LAB
#     Dy = (InRayEndPoint[1] - InRayOriginPoint[1]) / LAB
#
#     # -- Check if Dx or Dy is NaN -- #
#     if LAB != 0:
#         for i in range(0, len(InGridMapProperties)):
#             # position = InGridMapProperties[i]['Position']
#             t = (Dx * (InGridMapProperties[i]['Position'][0] - InRayOriginPoint[0])) + \
#                 (Dy * (InGridMapProperties[i]['Position'][1] - InRayOriginPoint[1]))
#
#             Ex = t * Dx + InRayOriginPoint[0]
#             Ey = t * Dy + InRayOriginPoint[1]
#
#             LEC = getEuclideanDistance(np.array([Ex, Ey]), InGridMapProperties[i]['Position'])
#
#             if LEC < InGridMapProperties[i]['Radius'] * 1:
#                 if 0 <= t <= LAB:
#                     if OutGripMapProperties[i]['Seen'] == 0:
#                         OutGripMapProperties[i]['Seen'] = InRayID
#
#                     hitsList.append(OutGripMapProperties[i])
#                     ts = np.vstack([ts, t])
#     # - Remove the zero -- #
#     ts = ts[1:]
#
#     if ts.shape[0] > 0:
#         # -- Sort row --#
#         ts = ts[ts[:, 0].argsort(),]
#         inds = ts[:, 0].argsort()
#
#         visiableHeight = 0
#
#         for i in range(0, inds.shape[0] - 1):
#             if hitsList[inds[i]]['Height'] >= visiableHeight:
#                 if hitsList[inds[i]]['Seen'] == InRayID:
#                     hitsList[inds[i]]['Visibility'] = getVisiblity(InRayID)
#                     OutSeenList.append(hitsList[inds[i]])
#
#             if hitsList[inds[i]]['Height'] > visiableHeight:
#                 visiableHeight = hitsList[inds[i]]['Height']
#             pass
#
#             if visiableHeight >= 1:
#                 break
#         pass
#
#     return OutSeenList, OutGripMapProperties
#
# # - Simple switch case -- #
# def getVisiblity(InRayID):
#     switch = {
#         1: 1,
#         2: 0.6,
#         3: 0.6,
#         4: 0.6,
#         5: 0.6,
#         6: 0.4,
#         7: 0.4,
#         8: 0.4,
#         9: 0.3,
#         10: 0.3,
#         11: 0.3,
#         12: 0.2,
#         13: 0.2,
#         14: 0.2,
#         15: 0.2
#     }
#     return switch.get(InRayID)
#
def getIsPointInsideFOVCorn(InPointOfInterest, InApex, InConeBase, InAperture):
    coneHeight = getEuclideanDistance(InApex, InConeBase)

    if coneHeight != 0:
        halfApature = math.atan(InAperture / coneHeight)

        apexToXYZ = InApex - InPointOfInterest
        Axis = InApex - InConeBase

        a = np.dot(apexToXYZ, Axis) / np.linalg.norm(apexToXYZ)
        b = np.linalg.norm(Axis)
        c = np.cos(halfApature)
        d = np.dot(apexToXYZ, Axis) / np.linalg.norm(Axis)
        e = np.linalg.norm(apexToXYZ)

        if (a / b) > c and d < e:
            return True
        else:
            return False
    else:
        return False


def getCollisionTimeOfTwoObject(InPositionOfObject1, InVelocityOfObject1, InPositionOfObject2, InVelocityOfObject2):
    OutCPA_time = 0
    # esp = np.power(2.0, -52)
    eps = np.finfo(float).eps

    dv = InVelocityOfObject1 - InVelocityOfObject2
    dv2 = np.dot(dv, dv)

    if dv2 > eps:
        w0 = InPositionOfObject1 - InPositionOfObject2
        OutCPA_time = -np.dot(w0, dv) / dv2
    else:
        OutCPA_time = 0

    return OutCPA_time


def getDistanceBetweenTwoObjectWithTime(InPositionOfObject1, InVelocityOfObject1, InPositionOfObject2,
                                        InVelocityOfObject2, InCollisionTimeOfTwoObject):
    P1 = InPositionOfObject1 + (InVelocityOfObject1 * InCollisionTimeOfTwoObject)
    P2 = InPositionOfObject2 + (InVelocityOfObject2 * InCollisionTimeOfTwoObject)
    cpa_distance = getVectorMagnitude(P1 - P2)

    return cpa_distance


def getDirectionBetweenTwoObjectWithTime(InPositionOfObjectA, InVelocityOfObject1, InPositionOfObjectB,
                                         InVelocityOfObjectB, InCollisionTimeOfTwoObject):
    P1 = InPositionOfObjectA + (InVelocityOfObject1 * InCollisionTimeOfTwoObject)
    P2 = InPositionOfObjectB + (InVelocityOfObjectB * InCollisionTimeOfTwoObject)
    OutDirectionWithTime = getNormalisedVector(P1 - P2)

    return OutDirectionWithTime


def displayPath(InTempPath, InGridMap, InId, InSettings):
    tempPath = np.asarray(InTempPath)
    gridMap = InGridMap.copy()

    # -- Start and End has different highlight -- #
    gridMap[tempPath[0, 1], tempPath[0, 0]] = 4
    gridMap[tempPath[tempPath.shape[0] - 1, 1], tempPath[tempPath.shape[0] - 1, 0]] = 2.5

    # -- highlight path -- #
    for i in range(1, tempPath.shape[0] - 1):
        gridMap[tempPath[i, 1], tempPath[i, 0]] = 3
    # -- Correct the orientation of map -- #
    gridMap = np.rot90(gridMap, k=1)

    path = f'SimulationResult/{InSettings.getPathForSimulationResults()}agentMap'
    createSimulationResultsFolder(path)
    plotImage(gridMap, f'{path}/Map{InId}.png')


def createSimulationResultsFolder(InPath):
    # -- Create folder -- #

    if not os.path.exists(InPath):
        os.makedirs(InPath)
        LogManager.displayLog(f'Folder {InPath} is created')


# -- Clean the crowd from image when mask is provide --#
def cleanCrowdFromBackground(InPathToImageFolder):

    # basePath = os.getcwd()[:-17]
    # backgroundImageFolderPath = f'{basePath}Python_Simulation/{InPathToImageFolder}'


    backgroundImageFolderPath = InPathToImageFolder

    streetImageList = [streetImage for streetImage in os.listdir(backgroundImageFolderPath) if streetImage.endswith(".jpg")]
    streetImageList.sort()
    try:
        maskImageList = [mask for mask in os.listdir(backgroundImageFolderPath) if mask == f'{mask[0:len(streetImageList[0].split(".")[0])]}_Mask.png']
        # maskImageList = [mask for mask in os.listdir(simulatedFolderPath) if mask.endswith(".png")]
        maskImageList.sort()
    except:
        LogManager.displayLog('Could not find any mask image to clean crowd from background image!')
        return False

    cleanBackgroundList = []
    scale_percent = 1  # percent of original size

    for i in range(len(maskImageList)):
        # - Inpaint the image --##
        img = cv2.imread(f'{backgroundImageFolderPath}{streetImageList[i]}')
        mask = cv2.imread(f'{backgroundImageFolderPath}{maskImageList[i]}', 0)

        # -- Save it in list --#
        cleanBackgroundList.append(cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA))

        # -- resize image and make sure image is more than 1024x768 -- #
        while int(cleanBackgroundList[i].shape[1] * scale_percent / 100) < 1024 or int(cleanBackgroundList[i].shape[0] * scale_percent / 100) < 768:
            scale_percent +=20

        width = int(cleanBackgroundList[i].shape[1] * scale_percent / 100)
        height = int(cleanBackgroundList[i].shape[0] * scale_percent / 100)

        dim = (width, height)
        cleanBackgroundList[i] = cv2.resize(cleanBackgroundList[i], dim, interpolation=cv2.INTER_AREA)

        # -- Save Image -- #
        fileName = streetImageList[i].split('.')[0]
        cv2.imwrite(f'{backgroundImageFolderPath}{fileName}_crowdCleanVersion.png', cleanBackgroundList[i])

    # -- if file exist return true else false
    return FileManager.checkIfFileExist(f'{backgroundImageFolderPath}{streetImageList[0].split(".")[0]}_crowdCleanVersion.png')

# def readImage(InPath):
#     return plt.imread(InPath)


def roundInt(x):
    if x == float("inf") or x == float("-inf"):
        return float('nan') # or x or return whatever makes sense
    return int(round(x))

def saveImage(InImage, InFilePath):
    import matplotlib as mpll
    import matplotlib.pyplot as pltt
    mpll.rcParams['savefig.pad_inches'] = 0
    # figsize = None if width is None else (InImage.shape[1], InImage.shape[0])
    # fig = plt.figure(figsize=figsize)
    # fig, ax = plt.subplots()
    # import matplotlib.pyplot as plt
    ax = pltt.axes([0, 0, 1, 1], frameon=False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    pltt.autoscale(tight=True)
    ax.imshow(InImage, cmap=plt.get_cmap('jet'))
    pltt.savefig(InFilePath, bbox_inches='tight')
    pltt.close('all')



def rgb2GrayImage(InImagePath):

    # from PIL import Image
    # img = Image.open(InImagePath).convert('LA')
    # return img
    image = cv2.imread(InImagePath)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def brg2RgbImage(InImagePath):
    image = cv2.imread(InImagePath)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def readImage(InImagePath):
    img= cv2.imread(InImagePath)
    # return cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return img


def saveImageCv(InPath, InImage):
    LogManager.displayLog(f"Saving in {InPath}", InColor='blue')
    # InImage = cv2.applyColorMap(InImage, cv2.COLOR_BGR2RGB)
    cv2.imwrite(InPath,InImage)

def saveToH5File(h5pyFilePath, InDensityMap):
    with h5py.File(h5pyFilePath, 'w') as hf:
        hf['density'] = InDensityMap
        LogManager.displayLog(f"Saving in {h5pyFilePath}")

def saveToDensityMapToImage(DensityMapPath, InDensityMap):
    im_density_sampled = convertImageToRange(InDensityMap, 0, 255)
    InDensityMap = cv2.applyColorMap(im_density_sampled, cv2.COLORMAP_JET)
    saveImageCv(DensityMapPath, InDensityMap)


def normalizeImage(InImage):
    """
    Linear normalization
    http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
    """
    InImage = InImage.astype('float')
    # Do not touch the alpha channel
    for i in range(3):
        minval = InImage[..., i].min()
        maxval = InImage[..., i].max()
        if minval != maxval:
            InImage[..., i] -= minval
            InImage[..., i] *= (255.0 / (maxval - minval))
    return InImage


def convertImageToRange(InImage, InMin, InMax):
    return ((InImage-np.min(InImage)) * (InMax-InMin)/(np.max(InImage) - np.min(InImage)) + InMin).astype(np.uint8)

import pandas as pd
def readCSV(InPath):
    # outCSV = pd.read_csv(InPath, sep=',', header=0)
    outCSV = pd.read_csv(InPath, sep=',', header=0).as_matrix()
    outCSV = outCSV.astype(np.float32, copy=False)

    return outCSV
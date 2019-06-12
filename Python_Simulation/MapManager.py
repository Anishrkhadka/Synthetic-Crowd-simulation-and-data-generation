import Utility
import LogManager
import numpy as np
import FileManager


def saveGripMapToFile(InFilePath, InGridMap):
    return FileManager.saveToTextFile(InFilePath, InGridMap)


def getGridMapFromFile(InGridMapPath=None, InDisplayLog=True):
    gridPath = f'{InGridMapPath[0:len(InGridMapPath) - 4]}_orientationCorrected.txt'

    # -- Check if orientation corrected grid is in the folder. if not create one --#
    if FileManager.checkIfFileExist(gridPath) is False:
        setTheGripMapToRightOrientation(InGridMapPath)

    gridMap = FileManager.loadTextFile(gridPath)
    if InDisplayLog:
        LogManager.displayLog(f'Loading {gridPath}')
    return gridMap


def setTheGripMapToRightOrientation(InGridMapPath):
    if FileManager.checkIfFileExist(InGridMapPath):
        gridMap = FileManager.loadTextFile(InGridMapPath)
        gridMap = np.rot90(gridMap, k=3)
        gridMap = np.fliplr(gridMap)
        fixedGridMapPath = f'{InGridMapPath[0:len(InGridMapPath) - 4]}_orientationCorrected.txt'
        saveGripMapToFile(InFilePath=fixedGridMapPath, InGridMap=gridMap)
    else:
        LogManager.displayLog(f'No file {InGridMapPath} found!')


def getGripMapProperties(InGridMap, InMapUnitSize=1):
    gridMapProperties = {'Position': None,
                         'Radius': None,
                         'Height': None,
                         'Risk': None,
                         # -- seen field keeps record of ray that has seen it -- # Agents fov
                         'Seen': 0,
                         'Visibility': 0}
    gridMapPropertiesList = []

    height, width = InGridMap.shape

    # -- first add each column then check if those col is greater than 0, if yes = true else false -- #
    IsColWithValue = InGridMap.sum(axis=0) > 0
    findColIndex = (IsColWithValue[:] == True).nonzero()
    colFirst = findColIndex[0][0]
    colLast = findColIndex[0][-1]

    IsRowWithValue = InGridMap.sum(axis=1) > 0
    findRowIndex = (IsRowWithValue[:] == True).nonzero()
    rowFirst = findRowIndex[0][0]
    rowLast = findRowIndex[0][-1]

    # LogManager.log( IsColWithValue,InName="IsColWithValue")
    # LogManager.log( findColIndex, InName="findColIndex")
    # LogManager.log(cdim_f,InName="cdim_f")
    # LogManager.log(cdim_l, InName="cdim_l")
    #
    # LogManager.log(IsRowWithValue, InName="IsRowWithValue")
    # LogManager.log(findRowIndex, InName="findColIndex")
    # LogManager.log(rdim_f, InName="rdim_f")
    # LogManager.log(rdim_l, InName="rdim_l")

    for i in range(0, height * width):
        row, col = Utility.ind2sub(InGridMap.shape, i)
        if (rowFirst - 1) < row < (rowLast + 1) and (colFirst - 1) < col < (colLast + 1):
            if InGridMap[row, col] == 0.0 or InGridMap[row, col] == 3.0:
                tempGridMapProperties = gridMapProperties.copy()
                tempGridMapProperties['Position'] = np.array([row, col])
                tempGridMapProperties['Radius'] = InMapUnitSize
                tempGridMapProperties['Height'] = 1
                tempGridMapProperties['Risk'] = 0
                gridMapPropertiesList.append(tempGridMapProperties)

            elif InGridMap[row, col] == 1.0 or InGridMap[row, col] == 2.0:
                tempGridMapProperties = gridMapProperties.copy()
                tempGridMapProperties['Position'] = np.array([row, col])
                tempGridMapProperties['Radius'] = InMapUnitSize
                # if  InGridMap[row, col] == 1.0:
                tempGridMapProperties['Height'] = 0
                tempGridMapProperties['Risk'] = 0
                # else:
                #     tempGridMapProperties['Height'] = 0
                #
                # if InGridMap[row, col] == 2.0:
                #     tempGridMapProperties['Risk'] = 2.1
                # else:
                #     tempGridMapProperties['Risk'] = 0

                gridMapPropertiesList.append(tempGridMapProperties)

            elif InGridMap[row, col] == 1.0 or InGridMap[row, col] == 4.0:
                tempGridMapProperties = gridMapProperties.copy()
                tempGridMapProperties['Position'] = np.array([row, col])
                tempGridMapProperties['Radius'] = InMapUnitSize
                tempGridMapProperties['Height'] = 0.5
                tempGridMapProperties['Risk'] = 0

                gridMapPropertiesList.append(tempGridMapProperties)

            elif InGridMap[row, col] == 5.0 or InGridMap[row, col] == 2.0:
                tempGridMapProperties = gridMapProperties.copy()
                tempGridMapProperties['Position'] = np.array([row, col])
                tempGridMapProperties['Radius'] = InMapUnitSize
                tempGridMapProperties['Height'] = 0
                tempGridMapProperties['Risk'] = 2.1

                gridMapPropertiesList.append(tempGridMapProperties)

    return gridMapPropertiesList


def convertGripMapToPathFinderFormat(InGridMap):
    # -- Convert value 3 i.e obstacles to 0 to fit data for path finding, in path finder 0 is obstacles --##
    processedGridMapForPathFinder = InGridMap.copy()
    processedGridMapForPathFinder[processedGridMapForPathFinder > 2] = 0
    return processedGridMapForPathFinder


def updateGridMapWithRiskInfo(InGridMap, InRiskList, InIsBorderlarge=True):
    OutGridMap = InGridMap.copy()
    x = 1
    y = 2
    # check if the Risk['Position'] is entry/exit if not make it obstacle -- #
    if InGridMap[InRiskList['Position'][0], InRiskList['Position'][1]] != 2:
        OutGridMap[InRiskList['Position'][0], InRiskList['Position'][1]] = 0

    if InGridMap[InRiskList['Position'][0] - x, InRiskList['Position'][1]] != 2:
        OutGridMap[InRiskList['Position'][0] - x, InRiskList['Position'][1]] = 0

    if InGridMap[InRiskList['Position'][0] + x, InRiskList['Position'][1]] != 2:
        OutGridMap[InRiskList['Position'][0] + x, InRiskList['Position'][1]] = 0

    if InGridMap[InRiskList['Position'][0], InRiskList['Position'][1] - x] != 2:
        OutGridMap[InRiskList['Position'][0], InRiskList['Position'][1] - x] = 0

    if InGridMap[InRiskList['Position'][0], InRiskList['Position'][1] + x] != 2:
        OutGridMap[InRiskList['Position'][0], InRiskList['Position'][1] + x] = 0

    if InGridMap[InRiskList['Position'][0] - x, InRiskList['Position'][1] - x] != 2:
        OutGridMap[InRiskList['Position'][0] - x, InRiskList['Position'][1] - x] = 0

    if InGridMap[InRiskList['Position'][0] - x, InRiskList['Position'][1] + x] != 2:
        OutGridMap[InRiskList['Position'][0] - x, InRiskList['Position'][1] + x] = 0

    if InGridMap[InRiskList['Position'][0] + x, InRiskList['Position'][1] - x] != 2:
        OutGridMap[InRiskList['Position'][0] + x, InRiskList['Position'][1] - x] = 0

    if InGridMap[InRiskList['Position'][0] + x, InRiskList['Position'][1] + x] != 2:
        OutGridMap[InRiskList['Position'][0] + x, InRiskList['Position'][1] + x] = 0

    if InIsBorderlarge:
        if InGridMap[InRiskList['Position'][0] - y, InRiskList['Position'][1] - x] != 2:
            OutGridMap[InRiskList['Position'][0] - y, InRiskList['Position'][1] - x] = 0

        if InGridMap[InRiskList['Position'][0] + y, InRiskList['Position'][1] - x] != 2:
            OutGridMap[InRiskList['Position'][0] + y, InRiskList['Position'][1] - x] = 0

        if InGridMap[InRiskList['Position'][0] - x, InRiskList['Position'][1] - y] != 2:
            OutGridMap[InRiskList['Position'][0] - x, InRiskList['Position'][1] - y] = 0

        if InGridMap[InRiskList['Position'][0] - x, InRiskList['Position'][1] + y] != 2:
            OutGridMap[InRiskList['Position'][0] - x, InRiskList['Position'][1] + y] = 0

        if InGridMap[InRiskList['Position'][0] - y, InRiskList['Position'][1] + x] != 2:
            OutGridMap[InRiskList['Position'][0] - y, InRiskList['Position'][1] + x] = 0

        if InGridMap[InRiskList['Position'][0] + y, InRiskList['Position'][1] + x] != 2:
            OutGridMap[InRiskList['Position'][0] + y, InRiskList['Position'][1] + x] = 0

        if InGridMap[InRiskList['Position'][0] + x, InRiskList['Position'][1] - y] != 2:
            OutGridMap[InRiskList['Position'][0] + x, InRiskList['Position'][1] - y] = 0

        if InGridMap[InRiskList['Position'][0] + x, InRiskList['Position'][1] + y] != 2:
            OutGridMap[InRiskList['Position'][0] + x, InRiskList['Position'][1] + y] = 0

        if InGridMap[InRiskList['Position'][0] - y, InRiskList['Position'][1] + x] != 2:
            OutGridMap[InRiskList['Position'][0] - y, InRiskList['Position'][1]] = 0

        if InGridMap[InRiskList['Position'][0] + y, InRiskList['Position'][1] + x] != 2:
            OutGridMap[InRiskList['Position'][0] + y, InRiskList['Position'][1] + x] = 0

        if InGridMap[InRiskList['Position'][0] - x, InRiskList['Position'][1] - y] != 2:
            OutGridMap[InRiskList['Position'][0] + x, InRiskList['Position'][1] - y] = 0

        if InGridMap[InRiskList['Position'][0] - x, InRiskList['Position'][1] + y] != 2:
            OutGridMap[InRiskList['Position'][0] + x, InRiskList['Position'][1] + y] = 0

        if InGridMap[InRiskList['Position'][0] - y, InRiskList['Position'][1]] != 2:
            OutGridMap[InRiskList['Position'][0] + y, InRiskList['Position'][1]] = 0

        if InGridMap[InRiskList['Position'][0] + y, InRiskList['Position'][1]] != 2:
            OutGridMap[InRiskList['Position'][0] + y, InRiskList['Position'][1]] = 0

        if InGridMap[InRiskList['Position'][0], InRiskList['Position'][1] - y] != 2:
            OutGridMap[InRiskList['Position'][0], InRiskList['Position'][1] - y] = 0

        if InGridMap[InRiskList['Position'][0], InRiskList['Position'][1] + y] != 2:
            OutGridMap[InRiskList['Position'][0], InRiskList['Position'][1] + y] = 0

    return OutGridMap

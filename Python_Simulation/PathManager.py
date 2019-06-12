# -- https://github.com/brean/python-pathfinding --#
import numpy as np

import Utility
from _ExternalLib.pathfinding.core.diagonal_movement import DiagonalMovement
from _ExternalLib.pathfinding.core.grid import Grid
from _ExternalLib.pathfinding.finder.a_star import AStarFinder


class PathFinder:
    def __init__(self):
        self.gridMap = None
        self.path = None
        self.totalNoOfStartEndPoint = None

    def setGripMap(self, InMap):
        self.gridMap = InMap

    def getTotalNumberOfStartEndPointInGrid(self):
        return self.totalNoOfStartEndPoint

    def getStartPositionEndPositionAndMap(self):

        # -- get the list of index for start and end position and covert the value to 1 as required by grid -- #
        startEndIndex, OutMap = self.getRowColIndexOfStartEndAndConvertValue(self.gridMap, InGreaterThan=1)

        self.totalNoOfStartEndPoint = startEndIndex.shape[0]

        # IDForStartEndIndex =np.arange(start=1, stop=self.getTotalNumberOfStartEndPointInGrid(), step=1)
        # startEndIndexWithID = np.c_[IDForStartEndIndex,startEndIndex]

        # LogManager.log(startEndIndex, InName="StartEndIndex")

        # -- First create list of Non Repeating Random to be used for indexing startEndIndex Array --#
        setOfNonRepeatingRandomNo = Utility.getListOfRandomNo(InRange=startEndIndex.shape[0],
                                                              InNumberOfValue=startEndIndex.shape[0])

        # -- Second create another list of Non Repeating Random to be used for
        # -- indexing setOfNonRepeatingRandomNo Array  so that index are selected randomly--#
        setOfNonRepeatingRandomNoIndex = Utility.getListOfRandomNo(InRange=setOfNonRepeatingRandomNo.shape[0],
                                                                   InNumberOfValue=setOfNonRepeatingRandomNo.shape[0])

        OutStartPosition = startEndIndex[setOfNonRepeatingRandomNo[setOfNonRepeatingRandomNoIndex[0]], :]
        OutEndPosition = startEndIndex[setOfNonRepeatingRandomNo[setOfNonRepeatingRandomNoIndex[1]], :]

        # -- Covert OutMap which is in python List format to numpy array --#
        OutMap = np.asarray(OutMap)

        return OutStartPosition, OutEndPosition, OutMap

    @staticmethod
    def getRowColIndexOfStartEndAndConvertValue(InMatrix, InGreaterThan):
        # -- Get the Row and col which are higher than 1 -- ##
        OutMapToList = InMatrix.tolist()
        startEnd = np.array([0, 0])

        for x in range(0, len(OutMapToList)):
            for y in range(0, len(OutMapToList[0])):
                if OutMapToList[x][y] > InGreaterThan:
                    row, col = x, y
                    # -- col first as required by grid -- #
                    startEnd = np.vstack((startEnd, np.c_[col, row]))
                    # -- Convert StartEnd=2 to Floor=1 --#
                    OutMapToList[x][y] = 1

        # test= OutMapToList[startEnd[0]][]

        # --remove the first row -- #
        return startEnd[1:], OutMapToList

    def getPath(self, IsDisplayPath=False, InStartPosition=None, InEndPosition=None):

        startPosition, endPosition, InGridMap = self.getStartPositionEndPositionAndMap()

        # LogManager.log(InGrid.shape[0], InName="Grid")
        grid = Grid(matrix=InGridMap)

        # LogManager.log(startPosition, InName="startPosition")
        # LogManager.log(endPosition, InName="endPosition")

        if InStartPosition is not None:
            startPosition = grid.node(InStartPosition[0], InStartPosition[1])
        else:
            startPosition = grid.node(startPosition[0], startPosition[1])

        if InEndPosition is not None:
            endPosition = grid.node(InEndPosition[0], InEndPosition[1])
        else:
            endPosition = grid.node(endPosition[0], endPosition[1])

        # --- Start A* Path Finder  --- #
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(startPosition, endPosition, grid)

        # LogManager.log(path, InName="path")
        # LogManager.log(runs, InName="runs")

        # print('operations:', runs, 'path length:', len(path))
        # print(grid.grid_str(path=path, start=startPosition, end=endPosition))
        if IsDisplayPath:
            self.displayPath(np.asarray([path])[0])
        return np.asarray([path])[0]

    def getListOfPathForAgents(self, InTotalNoOfPath, InLengthOfPath, InStartPosition=None):
        pathList = []

        # -- Pre-generate path with longer distance -- ##
        for i in range(0, InTotalNoOfPath):
            tempPath = None
            while True:
                tempPath = self.getPath(InStartPosition=InStartPosition)
                # find path which is longer than InLengthOfPath length -- #
                if tempPath.any():
                    if tempPath.shape[0] > InLengthOfPath[i] or tempPath.shape[1] > InLengthOfPath[i]:
                        break
            pathList.append(tempPath)

        return pathList

    def displayPath(self, InPath):
        tempPath = InPath
        tempMap = self.gridMap
        for i in range(0, tempPath.shape[0] - 1):
            tempMap[tempPath[i, 1], tempPath[i, 0]] = 3
        Utility.plotImage(tempMap)

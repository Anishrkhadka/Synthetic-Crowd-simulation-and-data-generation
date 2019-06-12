# import matplotlib

# matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt


import numpy as np
import MapManager
import Utility
import LogManager
import threading
import FileManager
import GUIManager

class getPerspective:

    def __init__(self, InSettings):

        self.settings = InSettings
        self.backgroundImage = None
        self.backgroundImageWidth = None
        self.backgroundImageHeight = None
        self.extraNumPoints = 2

        self.enlargedImage = None
        self.setOfPoints = np.zeros((7, 2), dtype=float)

        self.loadPointFromFiles = False
        self.IsPlotDisplay = False

        self.filePathOfSetOfPoints = InSettings.getUserDefinePointPath()
        self.gridPoints = None
        self.userDefinedMap = None
        self.userDefineMapFilePath = InSettings.getGridMapFilePath()


        self.pathForPerspectiveExtractionData = InSettings.getPathForPerspectiveExtraction()
        self.waitForKeyBoard = True
        self.window = GUIManager.getWindow()
        # -- Read the image -- #

    def init(self):
        self.setBackgroundImage()
        self.getEnlargedImage()



    def setBackgroundImage(self):
        self.backgroundImage = plt.imread(self.settings.getBackgroundImageForPerspectiveExtraction())
        # -- Remove the converted png file from the disk -- #
        FileManager.removeFile(self.settings.getBackgroundImageForPerspectiveExtraction())

    def getEnlargedImage(self):

        self.backgroundImageHeight, self.backgroundImageWidth, channel = self.backgroundImage.shape

        halfImageHeight = self.backgroundImageHeight // 2
        halfImageWidth = self.backgroundImageWidth // 2

        self.enlargedImage = np.ones((halfImageHeight * 4, halfImageWidth * 4, channel))

        # -- Add image within the enlarged image -- ##
        self.enlargedImage[halfImageHeight:halfImageHeight * 3,
                           halfImageWidth:halfImageWidth * 3, :] = self.backgroundImage

    # def displayPlot(self):
    #     self.IsPlotDisplay = self.settings.getIsDisplayPlotEnable()

    def run(self, InIsGetPerspective=True, InIsGetGridMap=True, InIsPlotDisplay=True):
        self.IsPlotDisplay = InIsPlotDisplay

        if InIsGetPerspective:
            self.getUserDefinedPointFromImage()
        # -- By default load points from file -- #
        self.loadUserDefinePointsFromFile()
        if InIsGetGridMap:
            self.findPerspective()
            # self.window.closeFigure()
        # self.setPositionOfGridPoints()
        self.createPathFindingMap()
        self.loadUserDefineGridMapFromFile()

    def getUserDefinedPointFromImage(self):

        # fig, ax = plt.subplots()
        # im = ax.imshow(self.enlargedImage)

        # self.window.plotImage(self.enlargedImage)
        self.window.setBackground(self.enlargedImage)
        self.window.show()

        # -- Get the user input for the perspective -- #

        LogManager.displayLog("Start measurement")

        LogManager.displayLog('Click Bottom of Line to Measure')
        self.setOfPoints[1, :] = self.window.getPointFromUser()
        # Utility.plotPoint(self.setOfPoints[1, 0], self.setOfPoints[1, 1])
        self.window.plotPoint(self.setOfPoints[1, 0], self.setOfPoints[1, 1])

        LogManager.displayLog('Click Top of Line to Measure')
        self.setOfPoints[0, :] = self.window.getPointFromUser()
        # Utility.plotPoint(self.setOfPoints[0, 0], self.setOfPoints[0, 1])
        self.window.plotPoint(self.setOfPoints[1, 0], self.setOfPoints[1, 1])

        # -- Display tempLine -- #
        # Utility.plotLine(self.setOfPoints[:, 0:1][0:2], self.setOfPoints[:, 1:2][0:2])
        self.window.plotLine(self.setOfPoints[:, 0:1][0:2], self.setOfPoints[:, 1:2][0:2])

        LogManager.displayLog('Click Bottom of Line Parallel to previous. MUST BE PARALLEL IN THE IMAGE')
        self.setOfPoints[2, :] = self.window.getPointFromUser()
        # Utility.plotPoint(self.setOfPoints[2, 0], self.setOfPoints[2, 1])
        self.window.plotPoint(self.setOfPoints[2, 0], self.setOfPoints[2, 1])

        LogManager.displayLog('Click Top of Line Parallel to previous')
        self.setOfPoints[3, :] = self.window.getPointFromUser()
        # Utility.plotPoint(self.setOfPoints[3, 0], self.setOfPoints[3, 1])
        self.window.plotPoint(self.setOfPoints[3, 0], self.setOfPoints[3, 1])

        # Utility.plotLine(self.setOfPoints[:, 0:1][2:4], self.setOfPoints[:, 1:2][2:4])
        self.window.plotLine(self.setOfPoints[:, 0:1][2:4], self.setOfPoints[:, 1:2][2:4])

        LogManager.displayLog('Click Reference Point along first Line that defines a unit measure (preferably 1m)')
        # self.getPointFromUser(5)
        # self.setOfPoints[5, :] = Utility.getPointFromUser()
        self.setOfPoints[5, :] = self.window.getPointFromUser()

        # Utility.plotPoint(self.setOfPoints[5, 0], self.setOfPoints[5, 1], "co")
        self.window.plotPoint(self.setOfPoints[5, 0], self.setOfPoints[5, 1], "co")

        # -- Plot the bottom line (x1,x2), (y1,y2)--

        # Utility.plotLine(np.vstack((self.setOfPoints[1, 0], self.setOfPoints[2, 0])),
        #                  np.vstack((self.setOfPoints[1, 1], self.setOfPoints[2, 1])))

        self.window.plotLine(np.vstack((self.setOfPoints[1, 0], self.setOfPoints[2, 0])),
                         np.vstack((self.setOfPoints[1, 1], self.setOfPoints[2, 1])))

        # -- Send the first two point -- #
        tempLine = Utility.getLineEquation(self.setOfPoints[0:2, :])

        # -- get the reference point -- #
        self.setOfPoints[5, 0], self.setOfPoints[5, 1] = Utility.getPointAlongLine(tempLine, self.setOfPoints[5, :])

        LogManager.displayLog( 'Click Reference Point between bottom of two '
            'lines that defines a unit measure (the same'
            ' unit measure as previously defined.)')

        # --
        # self.setOfPoints[6, :] = Utility.getPointFromUser()
        self.setOfPoints[6, :] = self.window.getPointFromUser()

        # Utility.plotPoint(self.setOfPoints[6, 0], self.setOfPoints[6, 1], "yo")
        self.window.plotPoint(self.setOfPoints[6, 0], self.setOfPoints[6, 1], "yo")

        tempLine = Utility.getLineEquation(self.setOfPoints[1:3, :])
        self.setOfPoints[6, 0], self.setOfPoints[6, 1] = Utility.getPointAlongLine(tempLine, self.setOfPoints[6, :])

        if self.setOfPoints[1, 0] < self.setOfPoints[2, 0]:
            self.setOfPoints[4, 0] = self.setOfPoints[2, 0] + 200

            height = self.enlargedImage.shape[0]

            if self.setOfPoints[4, 0] > height:
                self.setOfPoints[4, 0] = height
            self.setOfPoints[4, 1] = self.setOfPoints[2, 1] - 200
        else:
            self.setOfPoints[4, 1] = self.setOfPoints[2, 1] - 200
            if self.setOfPoints[4, 1] < 0:
                self.setOfPoints[4.1] = 0
            self.setOfPoints[4, 1] = self.setOfPoints[2, 1] - 200

        # Utility.plotPoint(self.setOfPoints[4, 0], self.setOfPoints[4, 1], "go")
        self.window.plotPoint(self.setOfPoints[4, 0], self.setOfPoints[4, 1], "go")
        # --- close the plot -- #

        # ax.axis('off')
        # plt.show()

        # -- Save the points in file -- #
        if FileManager.saveToTextFile(f'{self.pathForPerspectiveExtractionData}setOfPoints.txt', self.setOfPoints):
            LogManager.displayLog(f'Points save in {self.filePathOfSetOfPoints}')

    def loadUserDefinePointsFromFile(self):
        pointPath = f'{self.pathForPerspectiveExtractionData}setOfPoints.txt'
        if FileManager.checkIfFileExist(pointPath):
            self.setOfPoints = FileManager.loadTextFile(pointPath)
            LogManager.displayLog(self.setOfPoints, InName=f'{pointPath}')
        else:
            LogManager.displayLog(f"Can't Find {pointPath}")
            # -- if no point is found user will be ask to new one -- #
            # self.getUserDefinedPointFromImage()

    def loadUserDefineGridMapFromFile(self):
        self.userDefinedMap = MapManager.getGridMapFromFile(f'{self.pathForPerspectiveExtractionData}gridMap.txt')
        self.window.plotImage(self.userDefinedMap)

    def findPerspective(self):

        # --- init parameter -- #
        # num_extra_points = 5
        extra_vanishing_points = 5
        self.extraNumPoints = 10
        # -- Get the image height --#
        imageHeight = self.enlargedImage.shape[0]
        setOfPoints = np.c_[self.setOfPoints[:, 0],
                            imageHeight - self.setOfPoints[:, 1]]

        # Utility.plotLine(setOfPoints[0:4,0], setOfPoints[0:4,1])

        LogManager.displayLog(setOfPoints, InName="NewSetOfPoints")
        previousPoint = setOfPoints[5, :]

        line1 = Utility.getLineEquation(setOfPoints[0:2, :])
        LogManager.displayLog(line1, InName="Line1")
        line2 = Utility.getLineEquation(setOfPoints[2:4, :])
        LogManager.displayLog(line2, InName="Line2")

        vanishingPoint = Utility.getIntersectionPoint(np.vstack((line1, line2)))[1:]
        LogManager.displayLog(vanishingPoint[0], InName="vanishing_point[0]")
        LogManager.displayLog(vanishingPoint[1], InName="vanishing_point[1]")

        line3 = Utility.getLineEquation(np.vstack((vanishingPoint, setOfPoints[4, :])))
        LogManager.displayLog(line3, InName="Line3")

        unitVectorLength = Utility.getVectorMagnitude(np.array([previousPoint[0] - setOfPoints[1, 0],
                                                                previousPoint[1] - setOfPoints[1, 1], 0]))
        LogManager.displayLog(unitVectorLength, InName="unitVectorLength")

        # get and arbitary point in line 2 -- #
        arbitaryPointInLine2 = np.array([setOfPoints[2, 0] - setOfPoints[3, 0],
                                         setOfPoints[2, 1] - setOfPoints[3, 1]])
        LogManager.displayLog(arbitaryPointInLine2, InName="arbitaryPointInLine2")

        # -- Get the unit vector of line2 and add it to the bottom point -- #
        unitVectorOfLine2 = (arbitaryPointInLine2 / np.linalg.norm(arbitaryPointInLine2)) * unitVectorLength
        LogManager.displayLog(unitVectorOfLine2, InName="unitVectorOfLine2")

        bottomPoint = np.array([setOfPoints[2, 0] + unitVectorOfLine2[0], setOfPoints[2, 1] + unitVectorOfLine2[1]])
        LogManager.displayLog(bottomPoint, InName="bottomPoint")

        # -- Get the source point -- #
        tempLineForSourcePoint1 = Utility.getLineEquation(np.vstack((setOfPoints[1, :], bottomPoint)))
        LogManager.displayLog(tempLineForSourcePoint1, InName="tempLineForSourcePoint1")

        source_point1 = Utility.getIntersectionPoint(np.vstack((tempLineForSourcePoint1, line3)))[1:]
        LogManager.displayLog(source_point1, InName="source_point1")

        tempLineForSourcePoint2 = Utility.getLineEquation(np.vstack((previousPoint, bottomPoint)))
        LogManager.displayLog(tempLineForSourcePoint2, InName="tempLineForSourcePoint2")

        source_point2 = Utility.getIntersectionPoint(np.vstack((tempLineForSourcePoint2, line3)))[1:]
        LogManager.displayLog(source_point2, InName="source_point2")

        # -- Plot -- #
        # if self.IsPlotDisplay:
        #     fig, ax = plt.subplots()
        #     Utility.plotLine(setOfPoints[0:2, 0], setOfPoints[0:2, 1])
        #     Utility.plotLine(setOfPoints[2:4, 0], setOfPoints[2:4, 1])
        #     Utility.plotLine(np.vstack((vanishingPoint[0], setOfPoints[4, 0])),
        #                      np.vstack((vanishingPoint[1], setOfPoints[4, 1])))
        #
        #     Utility.plotPoint(previousPoint[0], previousPoint[1], 'cd')
        #     Utility.plotPoint(source_point1[0], source_point1[1], 'bd')
        #     Utility.plotPoint(source_point2[0], source_point2[1], 'rd')
        #     Utility.plotPoint(bottomPoint[0], bottomPoint[1], 'gd')
        #
        #     ax.axis('on')
        #     plt.show()

        # --      -- #
        previousDistance = Utility.getVectorMagnitude(np.array([previousPoint[0] - setOfPoints[0, 0],
                                                                previousPoint[1] - setOfPoints[0, 1], 0]))
        LogManager.displayLog(previousDistance, InName="previousDistance")

        distances = Utility.getVectorMagnitude(np.array([previousPoint[0] - setOfPoints[1, 0],
                                                         previousPoint[1] - setOfPoints[1, 1], 0]))
        LogManager.displayLog(distances, InName="distances")

        # -- Get the impossible distance -- #
        impossibleDistance = previousDistance - 1
        count = 0

        # if self.IsPlotDisplay:
        #     fig, ax = plt.subplots()

        while impossibleDistance < previousDistance and count < extra_vanishing_points:

            previousDistance = impossibleDistance.copy()

            lineFoundPointAlongLine1ToSourcePoint1 = Utility.getLineEquation(np.vstack((previousPoint, source_point1)))

            tempPointOnLine2 = Utility.getIntersectionPoint(np.vstack((lineFoundPointAlongLine1ToSourcePoint1,
                                                                       line2)))[1:]

            tempLineForSourcePoint2 = Utility.getLineEquation(np.vstack((tempPointOnLine2, source_point2)))

            tempPreviousPoint = previousPoint
            previousPoint = Utility.getIntersectionPoint(np.vstack((tempLineForSourcePoint2, line1)))[1:]

            distances = np.append(distances,
                                  Utility.getVectorMagnitude(np.array([previousPoint[0] - tempPreviousPoint[0],
                                                                       previousPoint[1] - tempPreviousPoint[1], 0])))

            impossibleDistance = Utility.getVectorMagnitude(np.array([(previousPoint[0] - setOfPoints[0, 0]),
                                                                      (previousPoint[1] - setOfPoints[0, 1]), 0]))

            if impossibleDistance > previousDistance:
                count = count + 1
                impossibleDistance = previousDistance.copy() - 1

            # if self.IsPlotDisplay:
            #     # -- Plot the lines and points -- #
            #     Utility.plotLine(np.vstack((previousPoint[0], source_point1[0])),
            #                      np.vstack((previousPoint[1], source_point1[1])))
            #     Utility.plotLine(np.vstack((tempPointOnLine2[0], source_point2[0])),
            #                      np.vstack((tempPointOnLine2[1], source_point2[1])))
            #     Utility.plotPoint(previousPoint[0], previousPoint[1], 'bd')
            #     Utility.plotPoint(tempPointOnLine2[0], tempPointOnLine2[1], 'gd')

        # - End -- #
        # if self.IsPlotDisplay:
        #     ax.axis('on')
        #     plt.show()

        # -- Add the distances to vanishing point -- #
        distances = np.append(distances, Utility.getVectorMagnitude(np.array([previousPoint[0] - vanishingPoint[0],
                                                                              previousPoint[1] - vanishingPoint[1],
                                                                              0])))
        LogManager.displayLog(distances, InName="distances")

        estimatedLineLength = np.sum(distances)
        LogManager.displayLog(estimatedLineLength, InName="est_line_length")

        line_points = Utility.getNormaliseData(distances, 0, estimatedLineLength)
        LogManager.displayLog(line_points, InName="line_points")

        # - Add 0,0 at the index 0 -- #
        totalRowInLinePoints = line_points.shape[0] - 1
        line_points = np.insert(line_points, 0, 0, axis=0)
        # -- row to col matrix --#
        line_points = np.vstack(line_points[:totalRowInLinePoints])


        LogManager.displayLog(line_points, InName="line_points")

        numLine = totalRowInLinePoints + self.extraNumPoints
        LogManager.displayLog(numLine, InName="num_lines")

        base_line_points = np.zeros((numLine, 2))

        base_line_unit_point = setOfPoints[6, :]
        LogManager.displayLog(base_line_unit_point, InName="base_line_unit_point")

        base_line_unit_vector = np.array([base_line_unit_point[0] - setOfPoints[1, 0],
                                          base_line_unit_point[1] - setOfPoints[1, 1]])

        LogManager.displayLog(base_line_unit_vector, InName="base_line_unit_vector")
        count = 0 - ((numLine / 2.0) - 2)

        LogManager.displayLog(count, InName="count")

        for i in range(0, numLine):
            base_line_points[i, :] = np.array([setOfPoints[1, 0] + base_line_unit_vector[0] * count,
                                               setOfPoints[1, 1] + base_line_unit_vector[1] * count])
            count = count + 1
            # LogManager.log(count, InName="count")

        base_line_points = base_line_points

        LogManager.displayLog(base_line_points, InName="base_line_points")

        # if self.IsPlotDisplay:
        #     fig, ax = plt.subplots()
        #
        #     Utility.plotPoint(setOfPoints[1:3, 0], setOfPoints[1:3, 1])
        #     Utility.plotPoint(base_line_points[:, 0], base_line_points[:, 1], 'o')
        #
        #     ax.axis('on')
        #     plt.show()

        base_line_to_vanishing_vectors = np.c_[base_line_points[:, 0] - vanishingPoint[0],
                                               base_line_points[:, 1] - vanishingPoint[1]]

        LogManager.displayLog(base_line_to_vanishing_vectors, InName="base_line_to_vanishing_vectors")

        self.gridPoints = np.zeros((numLine, numLine, 2), dtype='float')

        # fig, ax = plt.subplots()
        # im = ax.imshow(self.enlargedImage)
        # ax.margins(x=-0.35, y=-0.35)

        # -- Plot the user define line --#
        self.window.plotLine(setOfPoints[0:2, 0], imageHeight - setOfPoints[0:2, 1], Informat="yellow")
        self.window.plotLine(setOfPoints[2:4, 0], imageHeight - setOfPoints[2:4, 1], Informat="green")

        # -- Display the grid -- ##
        # plotPerspectiveGrid = np.array([0, 0])

        for i in range(0, numLine):
            for j in range(0, totalRowInLinePoints):
                temp = base_line_to_vanishing_vectors[i, :] * np.sum(line_points[0:j])
                self.gridPoints[i, j + self.extraNumPoints, :] = base_line_points[i, :] - temp

                # # -- Add points in the plot -- #
                # plotPerspectiveGrid = np.vstack((plotPerspectiveGrid,
                # np.array([self.gridPoints[i, j + self.extraNumPoints, 0],
                #           self.gridPoints[i, j + self.extraNumPoints, 1]])))


        LogManager.displayLog(self.gridPoints, InName="gridPoint")



        # fig, ax = plt.subplots()
        # im = ax.imshow(self.enlargedImage)
        # # Utility.plotPoint(plotPerspectiveGrid[:, 0], plotPerspectiveGrid[:, 1], Informat="o")#
        # Utility.plotPoint(self.gridPoints[:, 0], self.gridPoints[:, 1], Informat="o")  #
        # Utility.plotPoint(x[0:9], self.enlargedImage.shape[0] -y[0:9], Informat="o")

        # Utility.plotPoint(self.gridPoints[:, :, 0], self.enlargedImage.shape[0] - self.gridPoints[:, :, 1], Informat="o")

        if self.extraNumPoints > 0:
            # lineRow, LineCol = line_points.shape[0:1]

            xdata = np.arange(0,totalRowInLinePoints-1)
            LogManager.displayLog(xdata, InName="xdata")

            ydata = np.fliplr(line_points[1:].T)
            # -covert to small 1D array -- #
            ydata = ydata.ravel()

            LogManager.displayLog(ydata, InName="ydata")

            model = np.polyfit(xdata, ydata, 8)
            LogManager.displayLog(model, InName="model")

            x1 = np.arange(totalRowInLinePoints, totalRowInLinePoints + self.extraNumPoints)
            LogManager.displayLog(x1, InName="x1")

            predicted = np.vstack(np.polyval(model, x1))
            predicted = np.flip(predicted,1)
            LogManager.displayLog(predicted, InName="predicted")

            for i in range(0, numLine):
                for j in range(1, predicted.shape[0]+1):
                    tempValue = -base_line_to_vanishing_vectors[i, :] * np.sum(predicted[0:j])
                    self.gridPoints[i, self.extraNumPoints - j, :] = base_line_points[i, :] - tempValue

        #             plotPerspectiveGrid = np.vstack((plotPerspectiveGrid,
        #                                              np.array([self.gridPoints[i, self.extraNumPoints - j, 0],
        #                                              imageHeight - self.gridPoints[i, self.extraNumPoints - j, 1]])))
        #
        # # -- Plot the Perspective grid; skip the first -- #
        # plotPerspectiveGrid = plotPerspectiveGrid[1:, :]
        # plotPerspectiveGrid= plotPerspectiveGrid.round()
        #
        # Utility.plotPoint(plotPerspectiveGrid[:, 0], plotPerspectiveGrid[:, 1], Informat="o")
        # for i in range(self.gridPoints.shape[0]-1):
        #     for j in range(self.gridPoints.shape[1]-1):
        #         point1 = np.array([self.gridPoints[i,j,0], self.gridPoints[i,j,1]])
        #         point2 = np.array([self.gridPoints[i+1,j+1,0], self.gridPoints[i+1,j+1,1]])
        # self.gridPoints.round()

        # self.gridPoints = self.gridPoints.round()
        LogManager.displayLog(self.gridPoints[:, :, 0], InName="gridPoint")

        FileManager.saveToTextFile(f'{self.pathForPerspectiveExtractionData}gridPointsX.txt', self.gridPoints[:,:,0])
        FileManager.saveToTextFile(f'{self.pathForPerspectiveExtractionData}gridPointsY.txt', self.gridPoints[:, :, 1])

        self.window.plotImage(self.enlargedImage, f'{self.pathForPerspectiveExtractionData}enlargedImage.png')

    # def setPositionOfGridPoints(self):
    #     self.gridPoints[:, :, 0] = FileManager.loadTextFile(f'{self.pathForPerspectiveExtractionData}gridPointsX.txt')
    #     self.gridPoints[:, :, 1] = FileManager.loadTextFile(f'{self.pathForPerspectiveExtractionData}gridPointsY.txt')
    #
    #     self.window.closeFigure()
    #     window = GUIManager.getWindow()
    #     window.setBackground(self.enlargedImage)
    #     window.setTitle('MoveGrid')
    #     window.plotGridMap(self.gridPoints, self.enlargedImage.shape[0])
    #     # window.showWidget()
    #     window.show()
    #
    #     while self.window.getWaitForKeyBoard():
    #         try:
    #             mousePosWidth, mousePosHeight = self.window.getPointFromUser()[0]
    #         except:
    #             break
    #
    #     FileManager.saveToTextFile(f'{self.pathForPerspectiveExtractionData}gridPointsX.txt',
    #                                    self.gridPoints[:, :, 0])
    #     FileManager.saveToTextFile(f'{self.pathForPerspectiveExtractionData}gridPointsY.txt',
    #                                    self.gridPoints[:, :, 1])


    def createPathFindingMap(self):
        # self.gridPoints[:, :, 0] = FileManager.loadTextFile(f'{self.pathForPerspectiveExtractionData}gridPointsX.txt')
        # self.gridPoints[:, :, 1] = FileManager.loadTextFile(f'{self.pathForPerspectiveExtractionData}gridPointsY.txt')
        #
        # gridPointsX = self.gridPoints[:, :, 0]
        # gridPointsY = self.gridPoints[:, :, 1]

        self.gridPoints = self.gridPoints.round()
        engLargeImageHeight = self.enlargedImage.shape[0]
        self.window.plotGridMap(self.gridPoints, engLargeImageHeight)


        LogManager.displayLog("--Start of Create path finding map -- ")
        gridY, gridX = self.gridPoints.shape[0:2]
        gridY -=1
        gridX -=1
        LogManager.displayLog(np.c_[gridX, gridY], InName="XBlock, YBlock")

        OutGridMap = np.zeros((gridY, gridX), dtype=float)

        xMinMax = np.zeros((gridX-1, 2), dtype=float)
        yMinMax = np.zeros((gridY-1, 2), dtype=float)

        for i in range(0, gridX-1):
            xMinMax[i, 0] = np.min(self.gridPoints[i, :, 0])
            xMinMax[i, 1] = np.max(self.gridPoints[i+1, :, 0])

        for i in range(0, gridY-1):
            yMinMax[i, 0] = np.min(self.gridPoints[:, i, 1])
            yMinMax[i, 1] = np.max(self.gridPoints[:, i+1, 1])

        LogManager.displayLog(xMinMax, InName="x_bounds")
        LogManager.displayLog(yMinMax, InName="y_bounds")

        # -- exchange place min to max --#
        if xMinMax[0, 0] > xMinMax[0, 1]:
            xMinMax = np.c_[xMinMax[:, 1], xMinMax[:, 0]]

        if yMinMax[0, 0] > yMinMax[0, 1]:
            yMinMax = np.c_[yMinMax[:, 1], yMinMax[:, 0]]

        LogManager.displayLog(
            'CLICK THE CELL ON A MAP TO DEFINE THE ENTRANCE POINTS FOR THE PLANE, PRESS SPACE TO FINISH')


        while self.window.getWaitForKeyBoard():
            try:
                mousePosWidth, mousePosHeight  = self.window.getPointFromUser()[0].round()
            except:
                break

            mousePosHeight = (engLargeImageHeight - mousePosHeight)
            LogManager.displayLog(np.c_[mousePosWidth, mousePosHeight], InName="map_x,map_y")


            # # -- find the box which include the user define click -- #
            tempClickBox = self.getUserDefineBox(gridX-1,gridY-1,
                                                 mousePosWidth, mousePosHeight,
                                                 xMinMax, yMinMax)

            lines = np.asarray(tempClickBox)


            LogManager.displayLog(lines, InName="lines")

            line = np.array([0, 0])

            if lines is not []:
                for i in range(0, lines.shape[0]-1):

                    a = lines[i, 0]
                    a1 = a + 1
                    b = lines[i, 1]
                    b1 = b + 1

                    temp_points = np.squeeze(self.gridPoints[a, b, :])
                    temp_points_next = np.squeeze(self.gridPoints[a1, b1, :])

                    temp_points[0], temp_points_next[0] = self.compareTwoPoints(temp_points[0], temp_points_next[0])
                    temp_points[1], temp_points_next[1] = self.compareTwoPoints(temp_points[1], temp_points_next[1])

                    if self.compare(mousePosWidth, mousePosHeight, temp_points, temp_points_next):
                        line = lines[i, :]
                        # a = lines[i, 0]
                        # a1 = a + 1
                        # b = lines[i, 1]
                        # b1 = b + 1

                        plot_cords = np.array([self.gridPoints[a, b, :], self.gridPoints[a1, b, :],
                                               self.gridPoints[a1, b, :], self.gridPoints[a1, b1, :],
                                               self.gridPoints[a1, b1, :], self.gridPoints[a, b1, :],
                                               self.gridPoints[a, b1, :], self.gridPoints[a, b, :]])


                        # -- Display Extracted Perspective Grid -- #
                        # Utility.plotPointOnImage(self.enlargedImage, self.gridPoints[:, :, 0],
                        #                          engLargeImageHeight - self.gridPoints[:, :, 1])
                        # Utility.plotBox(plot_cords[2:5, 0], (engLargeImageHeight - plot_cords[2:5, 1]), 'r')

                        # LogManager.log(plot_cords, InName="plot_cords")

                        OutGridMap[line[1], line[0]] += 1

                        if OutGridMap[line[1], line[0]] > 3:
                            OutGridMap[line[1], line[0]] = 0

                        # -- Ground -- ##
                        if OutGridMap[line[1], line[0]] == 1:
                            self.window.plotBox(plot_cords[:, 0], (engLargeImageHeight - plot_cords[:, 1]), 'r')


                        # -- Entry/Exit point -- #
                        elif OutGridMap[line[1], line[0]] == 2:
                            self.window.plotBox(plot_cords[:, 0], (engLargeImageHeight - plot_cords[:, 1]), 'g')


                        # - obstacle --#
                        elif OutGridMap[line[1], line[0]] == 3:
                            self.window.plotBox(plot_cords[:, 0], (engLargeImageHeight - plot_cords[:, 1]), 'y')


                        # -- Empty space -- #
                        elif OutGridMap[line[1], line[0]] == 0:
                            self.window.plotBox(plot_cords[:, 0], (engLargeImageHeight - plot_cords[:, 1]), 'b')


        # tempGridMap = np.zeros((np.max([gridCol, gridRow]), np.max([gridCol, gridRow])))
        tempGridMap= OutGridMap


        # -- Temp fix for no row 5 value -- #
        tempGridMap = np.delete(tempGridMap, 1, axis=0)

        self.userDefinedMap = tempGridMap                                                                                                                                                                                                                                                                                                               

        # -- Save the grid map in file -- #
        FileManager.saveToTextFile(f'{self.pathForPerspectiveExtractionData}gridMap.txt', self.userDefinedMap)
        Utility.plotImage(self.userDefinedMap)

    # self.getUserDefineBox(gridX - 1, gridY - 1,
    #                       mousePosWidth, mousePosHeight,
    #                       xMinMax, yMinMax)
    
    def getUserDefineBox(self, InTotalColInGrid, InTotalRowInGrid,
                               InMousePosWidth, InMousePosHeight,
                               InXMinMax, InYMinMax):
        # -- Get the possible line that user click might be -- #
        OutResult = {'getLineList': [None] * InTotalColInGrid * InTotalRowInGrid}

        parallelThreads = []
        for i in range(0, InTotalColInGrid * InTotalRowInGrid):
            threads = threading.Thread(target=self.getGridBox,
                                       args=(InTotalColInGrid, InTotalRowInGrid,
                                             InMousePosWidth, InMousePosHeight,
                                             InXMinMax, InYMinMax,i, OutResult))
            threads.setDaemon(True)
            parallelThreads.append(threads)
            threads.start()

        for tt in parallelThreads:
            tt.join()

        # for i in range(0, InTotalColInGrid*InTotalRowInGrid):
        #     self.getGridBox(InTotalColInGrid, InTotalRowInGrid,
        #                     InMousePosWidth, InMousePosHeight,
        #                     InXMinMax, InYMinMax, i, OutResult)


        # --remove empty list --- ##
        tempClickBox = [x for x in OutResult['getLineList'][:] if x != []]
        return tempClickBox

    # -- Paralleled grid box --#
    def getGridBox(self, InTotalColInGrid, InTotalRowInGrid,
                   InMousePosWidth, InMousePosHeight,
                   InXMinMax, InYMiniMax, i, OutResult):

        row, col = Utility.ind2sub([InTotalColInGrid, InTotalRowInGrid], i)
        if self.compare(InMousePosWidth, InMousePosHeight,
                        InXMinMax, InYMiniMax, row, col):
            OutResult['getLineList'][i] = np.array([row, col], dtype='int')
        else:
            OutResult['getLineList'][i] = []



    @staticmethod
    def compareTwoPoints(InPoint1, InPoint2):
        if InPoint1 > InPoint2:
            dif = np.abs(InPoint1 - InPoint2) * 1.2
            InPoint1 = InPoint1 - dif
            InPoint2 = InPoint2 + dif
            return InPoint1, InPoint2
        else:
            return InPoint1, InPoint2

    @staticmethod
    def compare(InMousePosWidth, InMousePosHeight, InPoint1, InPoint2, InRow=None, InCol=None):
        if InRow is not None:
            if InPoint1[InRow, 0] <= InMousePosWidth < InPoint1[InRow, 1] and InPoint2[InCol, 0] <= InMousePosHeight < InPoint2[InCol, 1]:
                return True
        else:
            if InPoint1[0] <= InMousePosWidth < InPoint2[0] and InPoint1[1] <= InMousePosHeight < InPoint2[1]:
                return True
        return False
        # if InRow is not None:
        #     if InPoint1[InRow, 0] <= InMousePosWidth < InPoint1[InRow, 1]:
        #         if InPoint2[InCol, 0] <= InMousePosHeight < InPoint2[InCol, 1]:
        #             return True
        #     return False
        # else:
        #     if InPoint1[0] <= InMousePosWidth < InPoint2[0]:
        #         if InPoint1[1] <= InMousePosHeight < InPoint2[1]:
        #             return True
        #         return False


        return False

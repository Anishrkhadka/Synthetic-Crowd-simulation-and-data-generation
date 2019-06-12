import FileManager
import MapManager
import PathManager
import PerspectiveManager
import Utility
import GUIManager
import scipy.spatial
import scipy.ndimage
import os
import h5py
import scipy
import numpy as np


def testPerspectiveExtraction(InSettings, IsGetUserPoints=False, IsGetUserDefineMap=False, IsDisplayPlotEnable=False):
    # -- Display Python Warning Massage or not -- #
    # Utility.setWarningMsg(False)
    # #
    backgroundImage = "Data/images/pic1.png"
    # IsGetUserPoints = False
    # IsGetUserDefineMap = False
    # IsDisplayPlotEnable= False

    perspective = PerspectiveManager.getPerspective(InSettings)
    perspective.setBackgroundImage()
    perspective.getEnlargedImage()
    # perspective.displayPlot(IsDisplayPlotEnable)

    if IsGetUserPoints:
        perspective.getUserDefinedPointFromImage()
    # -- By default load points from file -- #
    perspective.loadUserDefinePointsFromFile()
    if IsGetUserDefineMap:
        perspective.findPerspective()
    perspective.loadUserDefineGridMapFromFile()


def testPathFinder():
    userDefinedMap = MapManager.getGridMapFromFile()
    userDefinedMap[userDefinedMap > 2] = 0

    pathFinder = PathManager.PathFinder()
    pathFinder.setGripMap(userDefinedMap)
    path = pathFinder.getPath()

    # pathList = []
    # -- Pre-generate path with longer distance -- ##
    i: int
    for i in range(0, 10):
        tempPath = None
        tempMap = userDefinedMap.copy()
        while True:
            tempPath = pathFinder.getPath()
            if tempPath.shape[0] > 4 or tempPath.shape[1] > 4:
                break
        tempPath = np.asarray(tempPath)

        for i in range(0, tempPath.shape[0] - 1):
            tempMap[tempPath[i, 1], tempPath[i, 0]] = 3

        # LogManager.log(path,InName="Path")
        Utility.plotImage(tempMap)

        # LogManager.log(path, InName="Path")

    # -- Convert path list to numpy array -- #
    # path = np.asarray(path)

    # for i in range(0, path.shape[0]-1):
    #     userDefinedMap[path[i,1],path[i,0]] = 3
    #
    # LogManager.log(path,InName="Path")
    # LogManager.log(path[0][:], InName="Start")
    # LogManager.log(path[-1][:], InName="End")

    Utility.plotImage(userDefinedMap)

    # Utility.plotImage(path)


def testGridManager():
    OutGridMap = MapManager.getGridMapFromFile()
    MapManager.getGripMapProperties(OutGridMap)
    FileManager.saveGridMapToImage('MAP_Test.png', OutGridMap)


def checkHeadPositionOfAvatar(InFrameNo, InSimulationName, InImageFolder):
    import LogManager

    basePath = os.getcwd()[:-17]

    targetPath = f'{basePath}Unity_Visual/Compositing/Result/{InSimulationName}/'
    txtfilePath = f'{targetPath}joint/'
    depthImagePath = f'{targetPath}{InImageFolder}/'

    DepthImageList = [depthImage for depthImage in os.listdir(depthImagePath) if depthImage.endswith(".png")]
    DepthImageList.sort()

    jointInfoPerFrame = [txt for txt in os.listdir(txtfilePath) if txt.endswith(".txt")]
    jointInfoPerFrame.sort()

    headpointFolder = f'{targetPath}HeadPoint/'
    FileManager.createFolder(headpointFolder)

    # i = InFrameNo
    for i in range(2, InFrameNo):
        listOfXandYForAgentHead = []
        with open(f'{txtfilePath}{jointInfoPerFrame[i]}') as TxtFile:
            for line in TxtFile:
                line = np.asarray(line.rstrip("\n").split("\t"), dtype='float')
                # if line[0] == 0 or line[1]==0: continue
                listOfXandYForAgentHead.append(line)

        background = Utility.readImage(f'{depthImagePath}{DepthImageList[i]}')
        # background = cv2.imread(f'{depthImagePath}{DepthImageList[i]}')
        # background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)
        backroundHeight, backgroundWidth = background.shape[:2]

        window = GUIManager.getWindow()
        window.setBackground(background)
        LogManager.displayLog(f"Saving {i}.png in Unity->Result->{InSimulationName}->HeadPoint/{i}.png")

        XandYPositionOfHead = np.asarray(listOfXandYForAgentHead, dtype='float')

        window.plotPointOnImageAndSave(XandYPositionOfHead[:, 0], XandYPositionOfHead[:, 1], InIsFlip=False,
                                       InFileName=f'{headpointFolder}{i}.png')
        window.closeFigure()


def generatedDensityMap(InFrameNo, InSimulationName, InImageFolder):
    ## -- Image = Ori and GroundTruth = Joint i.e head location --##
    import LogManager

    basePath = os.getcwd()[:-17]

    targetPath = f'{basePath}Unity_Visual/Compositing/Result/{InSimulationName}/'
    groundTruthTxtFile = f'{targetPath}joint/'
    imagePath = f'{targetPath}{InImageFolder}/'

    imageList = [image for image in os.listdir(imagePath) if image.endswith(".png")]
    imageList.sort()

    groundTruthHeadPosList = [txt for txt in os.listdir(groundTruthTxtFile) if txt.endswith(".txt")]
    groundTruthHeadPosList.sort()

    densityMapPath = f'{targetPath}densityMap/'
    FileManager.createFolder(densityMapPath)
    FileManager.createFolder(f'{densityMapPath}/map/')
    FileManager.createFolder(f'{densityMapPath}/h5pyFiles/')

    # i = InFrameNo
    for i in range(2, InFrameNo):
        HeadPosXandY = []
        with open(f'{groundTruthTxtFile}{groundTruthHeadPosList[i]}') as TxtFile:
            for line in TxtFile:
                line = np.asarray(line.rstrip("\n").split("\t"), dtype='float')
                # if line[0] == 0 or line[1]==0: continue
                HeadPosXandY.append(line)

        image = Utility.readImage(f'{imagePath}{imageList[i]}')
        imageHeight, imageWidth = image.shape[:2]

        k = np.zeros((imageHeight, imageWidth))
        groundTruth = np.asarray(HeadPosXandY)

        for index in range(0, len(groundTruth)):
            if int(groundTruth[index][1]) < imageHeight and int(groundTruth[index][0]) < imageWidth:
                k[int(groundTruth[index][1]), int(groundTruth[index][0])] = 1
        k = gaussian_filter_density(k)

        with h5py.File(f'{densityMapPath}h5pyFiles/{imageList[i]}'.replace('.png', '.h5'), 'w') as hf:
            hf['density'] = k

        # h5pyFileList = [h5Files for h5Files in os.listdir(groundTruthTxtFile) if h5Files.endswith(".txt")]
        # h5pyFileList.sort()

        # gtFileList = [txt for txt in os.listdir(densityMapPath) if txt.endswith(".h5")]
        # groundTruthHeadPosList.sort()
        # gt_file = h5py.File(f'{densityMapPath}{gtFileList[0]}', 'r')
        gt_file = h5py.File(f'{densityMapPath}h5pyFiles/{imageList[i]}'.replace('.png', '.h5'), 'r')
        groundTruth = np.asarray(gt_file['density'])

        # plt.imshow(groundTruth, cmap=cm.jet)

        window = GUIManager.getWindow()
        window.setBackground(groundTruth)
        LogManager.displayLog(f"Saving {i}.png in Unity->Result->{InSimulationName}->DensityMap/map/{i}.png")
        window.saveImage(f'{densityMapPath}/map/{i}.png')
        window.closeFigure()

#
def gaussian_filter_density(InGroundTruth):

    density = np.zeros(InGroundTruth.shape, dtype=np.float32)
    groundTruthCount = np.count_nonzero(InGroundTruth)
    if groundTruthCount == 0:
        return density

    pts =np.array(list(zip(np.nonzero(InGroundTruth)[1], np.nonzero(InGroundTruth)[0])))
    leafsize = 2048
    # build kdtree
    tree = scipy.spatial.KDTree(pts.copy(), leafsize=leafsize)
    # query kdtree
    distances, locations = tree.query(pts, k=4)

    distances[np.isinf(distances[:])] = float('nan')

    print('generate density...')
    for i, pt in enumerate(pts):
        pt2d = np.zeros(InGroundTruth.shape, dtype=np.float32)
        pt2d[pt[1], pt[0]] = 1.
        if groundTruthCount > 1:
            sigma = (distances[i][1] + distances[i][2] + distances[i][3]) * 0.1
        else:
            sigma = np.average(np.array(InGroundTruth.shape)) / 2. / 2.  # case: 1 point
        density += scipy.ndimage.filters.gaussian_filter(pt2d, sigma, mode='constant')
    print('done.')

    return density

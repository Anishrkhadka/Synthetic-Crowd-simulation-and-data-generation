import os
import shutil
import threading

import cv2
import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.io as io
import scipy.ndimage
import scipy.spatial
from PIL import Image

import FileManager
import LogManager
import UtilityManager


def checkHeadPositionOfAvatar(InSimulationName, InImageFolder):
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

    InFrameNo = len(DepthImageList) - 1
    for i in range(2, InFrameNo):
        listOfXandYForAgentHead = []
        with open(f'{txtfilePath}{jointInfoPerFrame[i]}') as TxtFile:
            for line in TxtFile:
                line = np.asarray(line.rstrip("\n").split("\t"), dtype='float')
                # if line[0] == 0 or line[1]==0: continue
                listOfXandYForAgentHead.append(line)

        background = UtilityManager.readImage(f'{depthImagePath}{DepthImageList[i]}')
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


def gaussian_filter_density(InGroundTruth, InMethod=1):
    density = np.zeros(InGroundTruth.shape, dtype=np.float32)
    groundTruthCount = np.count_nonzero(InGroundTruth)
    if groundTruthCount == 0:
        return density

    pts = np.array(list(zip(np.nonzero(InGroundTruth)[1], np.nonzero(InGroundTruth)[0])))
    leafsize = 2048
    # build kdtree
    tree = scipy.spatial.KDTree(pts.copy(), leafsize=leafsize)
    # query kdtree
    distances, locations = tree.query(pts, k=20)

    distances[np.isinf(distances[:])] = float('nan')
    stdDistance = distances.copy()
    stdDistance -= np.mean(stdDistance)
    stdDistance /= np.std(stdDistance)
    stdDistance = np.clip(stdDistance, 0, 1)
    OutMeanDistance =np.mean(stdDistance)

    for i, pt in enumerate(pts):
        pt2d = np.zeros(InGroundTruth.shape, dtype=np.float32)
        pt2d[pt[1], pt[0]] = 1.

        sigma = compute_sigma(groundTruthCount,
                              distances, stdDistance[i], OutMeanDistance,
                              min_sigma=1, method=InMethod,
                              fixed_sigma=16)
        density += scipy.ndimage.filters.gaussian_filter(pt2d, sigma, mode='constant')

    return density


def compute_sigma(gt_count, distance=None, stddistance=None, InMeanDistance=None, min_sigma=1, method=3, fixed_sigma=4):
    """
    Compute sigma for gaussian kernel with different methods :
    * method = 1 : sigma = (sum of distance to 3 nearest neighbors) / 10
    * method = 2 : sigma = distance to nearest neighbor
    * method = 3 : sigma = fixed value
    ** if sigma lower than threshold 'min_sigma', then 'min_sigma' will be used
    ** in case of one point on the image sigma = 'fixed_sigma'
    """

    # if gt_count > 1 and distance is not None:
    #     if method == 1:
    #         sigma = np.mean(distance[1:10]) * 0.1
    #     elif method == 2:
    #         sigma = distance[1]
    #     elif method == 3:
    #         sigma = fixed_sigma
    # else:
    #     sigma = fixed_sigma
    # if sigma < min_sigma:
    #     sigma = min_sigma

    # method = 1
    if gt_count > 1 and distance is not None:
        method1 = np.mean(stddistance[1:20])
        if InMeanDistance / 2. <= method1 < InMeanDistance*2:
            sigma = np.mean(distance[1:20]) / 5.
        if InMeanDistance*2 <= method1 <= InMeanDistance * 8:
            sigma = np.mean(distance[1:20]) / 8.
        else:
            sigma = np.mean(distance[1:20]) / 10.
    else:
        sigma = fixed_sigma
    if sigma < min_sigma:
        sigma = min_sigma

    return sigma


def makeTrainSet(InPath):
    rootPath = InPath
    allFolderInRoot = [streetImage for streetImage in os.listdir(rootPath)]
    allFolderInRoot.sort()

    FileManager.createFolder(rootPath + '/train')
    FileManager.createFolder(rootPath + '/train/images')
    FileManager.createFolder(rootPath + '/train/ground_truth')
    allFolderInRoot.remove('.directory')
    try:
        allFolderInRoot.remove('train')
    except:
        pass

    # -- create a full path for each item in list --#
    for i in range(len(allFolderInRoot)):
        allFolderInRoot[i] = rootPath + "/" + allFolderInRoot[i] + "/"

    # -- create full path -- #
    counter = 1
    for i in range(len(allFolderInRoot)):
        # allFolderInRoot[i] = rootPath + "/" + allFolderInRoot[i] + "/"

        FileManager.renameFileSequence(allFolderInRoot[i] + 'Ori/', 'png', 'IMG')
        FileManager.renameFileSequence(allFolderInRoot[i] + 'joint/', 'txt', 'GT_IMG')

        allImages = [files for files in os.listdir(allFolderInRoot[i] + 'Ori/')]
        allImages.sort()
        allGTImages = [files for files in os.listdir(allFolderInRoot[i] + 'joint/')]
        allGTImages.sort()

        # -- copy file between 10 to end-10 --/
        for j in range(2, len(allImages) - 10):
            extension1 = allImages[j].split(".")
            extension2 = allGTImages[j].split(".")

            trainName = f'{rootPath}/train/images/IMG_{counter:05}.{extension1[1]}'
            groundTruthName = f'{rootPath}/train/ground_truth/GT_IMG_{counter:05}.{extension2[1]}'

            LogManager.displayLog(
                f'Copying file from {allFolderInRoot[i][len(rootPath):]} ===> {trainName[len(rootPath):]}')
            shutil.copy(f'{allFolderInRoot[i]}Ori/{allImages[j]}', trainName)

            LogManager.displayLog(
                f'Copying file from {allFolderInRoot[i][len(rootPath):]} ===> {groundTruthName[len(rootPath):]}')
            shutil.copy(f'{allFolderInRoot[i]}joint/{allGTImages[j]}', groundTruthName)

            counter += 1


def dataPreparation(InDatabaseName, InImagePath, InGroundTruthPath, InDataSetPart='A', InImageFormat='png',
                    InGroundTruthFormat='txt', InIsBlock=True, Inoutput=None, Is_Split_Train_val=0.1):
    # -- Reads the image and ground truth then convert image/ground truth into 9 different box and save it as jpg + h5 - #

    rand_seed = 95461354
    if rand_seed is not None:
        np.random.seed(rand_seed)
    if InIsBlock:
        N = InIsBlock
    else:
        N = 1
    dataset = InDataSetPart
    dataset_name = f'{InDatabaseName}_patches_{N}'

    imagePath = InImagePath
    groundTruthPath = InGroundTruthPath

    output_path = Inoutput

    densityPath = f'{output_path}/{dataset_name}/densityMap/'
    train_path_img = f'{output_path}/{dataset_name}/train/'
    train_path_den = f'{output_path}/{dataset_name}/train_den/'
    val_path_img = f'{output_path}/{dataset_name}/val/'
    val_path_den = f'{output_path}/{dataset_name}/val_den/'
    train_mask_path = f'{output_path}/{dataset_name}/train_mask/'
    val_mask_path = f'{output_path}/{dataset_name}/val_mask/'

    FileManager.createFolder(output_path)
    FileManager.createFolder(densityPath)
    FileManager.createFolder(train_path_img)
    FileManager.createFolder(train_path_den)
    FileManager.createFolder(val_path_img)
    FileManager.createFolder(val_path_den)
    FileManager.createFolder(train_mask_path)
    FileManager.createFolder(val_mask_path)

    imageList = [image for image in os.listdir(imagePath) if image.endswith(f".{InImageFormat}")]
    imageList.sort()

    groundTruthHeadPosList = [file for file in os.listdir(groundTruthPath) if file.endswith(f".{InGroundTruthFormat}")]
    groundTruthHeadPosList.sort()

    num_images = len(imageList)
    num_val = np.floor(num_images * Is_Split_Train_val)
    indices = UtilityManager.getListOfRandomNo(num_images, num_images)

    parallelThreads = []
    # -- if there are more than 500 images then break it down into 200 steps --#
    # -- to save memory --#
    if num_images > 100:
        for idx in range(0, num_images, 100):
            # _parallelThreadForGeneratingDensityMap(indices, idx, imagePath,
            #                                        imageList, groundTruthPath,
            #                                        groundTruthHeadPosList,num_val,
            #                                        val_path_img, val_path_den,
            #                                        train_path_img, train_path_den, N,num_val)
            parallelLoop = []
            for i in range(100):
                threads = threading.Thread(target=_parallelThreadForGeneratingDensityMap,
                                           args=(indices, idx + i, imagePath, imageList, groundTruthPath,
                                                 groundTruthHeadPosList,
                                                 num_val, val_path_img, val_path_den, train_path_img, train_path_den,
                                                 densityPath, train_mask_path, val_mask_path, N, num_val))
                parallelLoop.append(threads)
                threads.setDaemon(True)
                threads.start()
            for tt in parallelLoop:
                tt.join()
    else:
        for idx in range(0, num_images):
            # _parallelThreadForGeneratingDensityMap(indices, idx, imagePath, imageList, groundTruthPath, groundTruthHeadPosList,
            #                                num_val, val_path_img, val_path_den, train_path_img, train_path_den,
            #                                densityPath, train_mask_path, val_mask_path, N, num_val)

            threads = threading.Thread(target=_parallelThreadForGeneratingDensityMap,
                                       args=(
                                           indices, idx, imagePath, imageList, groundTruthPath, groundTruthHeadPosList,
                                           num_val, val_path_img, val_path_den, train_path_img, train_path_den,
                                           densityPath, train_mask_path, val_mask_path, N, num_val))
            parallelThreads.append(threads)
            threads.setDaemon(True)
            threads.start()

        for tt in parallelThreads:
            tt.join()


def loadGroundTruth(InFilePath):
    HeadPosXandY = []
    with open(InFilePath) as TxtFile:
        for line in TxtFile:
            line = np.asarray(line.rstrip("\n").split("\t"), dtype='float')
            HeadPosXandY.append(line)

    return np.asarray(HeadPosXandY)


def _parallelThreadForGeneratingDensityMap(indices, idx, imagePath, imageList, groundTruthPath, groundTruthHeadPosList,
                                           num_val, val_path_img, val_path_den, train_path_img, train_path_den,
                                           densityPath, train_mask_path, val_mask_path, InBlockNo=9,
                                           Is_Split_Train_val=True):
    boxNumber = InBlockNo
    i = indices[idx]
    if np.mod(idx, 10) == 0:
        print(f'Processing {idx}/{len(imageList)}\n')

    if groundTruthHeadPosList[i].split('.')[1] == 'txt':
        groundTruthLocation = loadGroundTruth(f'{groundTruthPath}{groundTruthHeadPosList[i]}')

    if groundTruthHeadPosList[i].split('.')[1] == 'mat':
        mat = io.loadmat(f'{groundTruthPath}{groundTruthHeadPosList[i]}')
        try:
            # -- shtech Database -- #
            groundTruthLocation = mat["image_info"][0, 0][0, 0][0]
        except:
            # -- for UFC-50 database -- #
            groundTruthLocation = mat["annPoints"]

    if groundTruthHeadPosList[i].split('.')[1] == 'h5':
        groundTruthLocation = h5py.File(f'{groundTruthPath}{groundTruthHeadPosList[i]}', 'r')
        groundTruthLocation = np.asarray(list(groundTruthLocation['density'])).astype('float32')

    image = UtilityManager.readImage(f'{imagePath}{imageList[i]}')
    h, w, _ = image.shape

    wn2 = w / 8
    hn2 = h / 8
    wn2 = 8 * np.floor(wn2 / 8)
    hn2 = 8 * np.floor(hn2 / 8)

    if w <= 2 * wn2:
        image = cv2.resize(image, (h, 2 * wn2 + 1))
        groundTruthLocation[:, 0] = groundTruthLocation[:, 0] * 2 * wn2 / w

    if h <= 2 * hn2:
        image = cv2.resize(image, (2 * hn2 + 1, w))
        groundTruthLocation[:, 1] = groundTruthLocation[:, 1] * 2 * hn2 / h

    h, w, _ = image.shape

    a_w = wn2 + 1
    b_w = w - wn2
    a_h = hn2 + 1
    b_h = h - hn2

    # Check if we already have density map
    if groundTruthHeadPosList[i].split('.')[1] == 'h5':
        densityMap = groundTruthLocation
        densityMap = cv2.resize(densityMap, (w, h))
    else:
        densityMap = np.zeros((h, w))
        for index in range(0, len(groundTruthLocation)):
            if int(groundTruthLocation[index][1]) < h and int(groundTruthLocation[index][0]) < w:
                densityMap[int(groundTruthLocation[index][1]), int(groundTruthLocation[index][0])] = 1
        # print(f'Create Density Map for {imageList[i]}')
        densityMapWithGaussian = gaussian_filter_density(densityMap, InMethod=1)

    if boxNumber > 1:
        for j in range(boxNumber):
            x = np.floor((b_w - a_w) * np.squeeze(np.random.rand(1)) + a_w)
            y = np.floor((b_h - a_h) * np.squeeze(np.random.rand(1)) + a_h)
            x1 = np.int16(x - wn2)
            y1 = np.int16(y - hn2)
            x2 = np.int16(x + wn2 - 1)
            y2 = np.int16(y + hn2 - 1)
            im_sampled = image[y1:y2, x1:x2]

            if groundTruthHeadPosList[i].split('.')[1] == 'h5':
                im_density_sampled = densityMap[y1:y2, x1:x2]
            else:
                im_density_sampled = densityMapWithGaussian[y1:y2, x1:x2]

            im_mask = densityMap[y1:y2, x1:x2]

            img_idx = f'{imageList[i].split(".")[0]}_{j}'

            # -- Split train val else put everything in train folder -- //
            if num_val:
                if idx < num_val:
                    UtilityManager.saveImageCv(f'{val_path_img}{img_idx}.jpg', im_sampled)
                    UtilityManager.saveToH5File(f'{val_path_den}{img_idx}.h5', im_density_sampled)
                    # UtilityManager.saveToH5File(f'{train_mask_path}{img_idx}.h5', im_mask)
                    # To check density map --\
                    UtilityManager.saveToDensityMapToImage(f'{densityPath}{img_idx}.jpg', im_density_sampled * 255)
                else:
                    UtilityManager.saveImageCv(f'{train_path_img}{img_idx}.jpg', im_sampled)
                    UtilityManager.saveToH5File(f'{train_path_den}{img_idx}.h5', im_density_sampled)
                    # UtilityManager.saveToH5File(f'{val_mask_path}{img_idx}.h5', im_mask)

                    UtilityManager.saveToDensityMapToImage(f'{densityPath}{img_idx}.jpg', im_density_sampled * 255)
            else:
                # Save image
                UtilityManager.saveImageCv(f'{train_path_img}{img_idx}.jpg', im_sampled)
                # Save density map
                UtilityManager.saveToH5File(f'{train_path_den}{img_idx}.h5', im_density_sampled)
                # Save density map as image
                UtilityManager.saveToDensityMapToImage(f'{densityPath}{img_idx}.jpg', im_density_sampled * 255)

                # Save image mask map
                # UtilityManager.saveToH5File(f'{train_mask_path}{img_idx}.h5', im_mask)

    else:
        gtName = groundTruthHeadPosList[i].split('.')[0]
        imName = imageList[i].split('.')[0]
        # Save image
        UtilityManager.saveImageCv(f'{train_path_img}{imName}.jpg', image)
        # Save density map as h5
        if groundTruthHeadPosList[i].split('.')[1] == 'h5':
            UtilityManager.saveToH5File(f'{train_path_den}{gtName}.h5', densityMap)
        else:
            UtilityManager.saveToH5File(f'{train_path_den}{gtName}.h5', densityMapWithGaussian)

        # Save density map as image
        UtilityManager.saveToDensityMapToImage(f'{densityPath}{imName}.jpg', densityMapWithGaussian)
        # Save image mask
        # UtilityManager.saveToH5File(f'{train_mask_path}{imName}.h5', densityMap*255)


def _parallelThreadToSaveDensityMapAsImage(indices, idx, imagePath, imageList, groundTruthPath, groundTruthHeadPosList,
                                           train_path_img):
    i = indices[idx]
    if np.mod(idx, 10) == 0:
        print(f'Processing {idx}/{len(imageList)}\n')

    if groundTruthHeadPosList[i].split('.')[1] == 'txt':
        groundTruthLocation = loadGroundTruth(f'{groundTruthPath}{groundTruthHeadPosList[i]}')

    if groundTruthHeadPosList[i].split('.')[1] == 'mat':
        mat = io.loadmat(f'{groundTruthPath}{groundTruthHeadPosList[i]}')
        try:
            # -- shtech Database -- #
            groundTruthLocation = mat["image_info"][0, 0][0, 0][0]
        except:
            # -- for UFC-50 database -- #
            groundTruthLocation = mat["annPoints"]

    image = UtilityManager.rgb2GrayImage(f'{imagePath}{imageList[i]}')
    h, w = image.shape

    imageDensity = np.zeros((h, w))
    for index in range(0, len(groundTruthLocation)):
        if int(groundTruthLocation[index][1]) < h and int(groundTruthLocation[index][0]) < w:
            imageDensity[int(groundTruthLocation[index][1]), int(groundTruthLocation[index][0])] = 1

    imageDensity = gaussian_filter_density(imageDensity, InMethod=1)
    LogManager.displayLog(f'{train_path_img[:len(train_path_img) - 7]}/densityMap/_{i:04}.png')
    img = UtilityManager.convertImageToRange(imageDensity, 0, 255)

    densityMap = cv2.applyColorMap(img, cv2.COLORMAP_JET)

    cv2.imwrite(f'{train_path_img[:len(train_path_img) - 7]}/densityMap/{i:04}.png', densityMap)
    # UtilityManager.saveImage(imageDensity,f'{train_path_img[:len(train_path_img)-7]}/densityMap/{i:04}.png' )


def calculateMeanStdOfDataset(imagePath, InImageFormat):
    imageList = [image for image in os.listdir(imagePath) if image.endswith(f".{InImageFormat}")]
    imageList.sort()
    if len(imageList) == 0:
        print('No image found!')
        return

    num_images = len(imageList)
    datasetMean = [None] * num_images
    datasetStd = [None] * num_images

    OutResult = {'dataMean': datasetMean,
                 'dataStd': datasetStd}

    parallelLoop = []
    for i in range(num_images):
        imageFullPath = f'{imagePath}{imageList[i]}'

        threads = threading.Thread(target=_parallelThreadForCalculateMeanStdOfDataset,
                                   args=(imageFullPath, OutResult, i))
        parallelLoop.append(threads)
        threads.setDaemon(True)
        threads.start()
        if i % 10 == 0:
            print(f"Loading {i}/{num_images}")

    for tt in parallelLoop:
        tt.join()

    totalMean = ((np.sum(np.asarray(OutResult['dataMean'])[:, 0]) / num_images),
                 (np.sum(np.asarray(OutResult['dataMean'])[:, 1]) / num_images),
                 (np.sum(np.asarray(OutResult['dataMean'])[:, 2]) / num_images))
    totalStd = ((np.sum(np.asarray(OutResult['dataStd'])[:, 0]) / num_images),
                (np.sum(np.asarray(OutResult['dataStd'])[:, 1]) / num_images),
                (np.sum(np.asarray(OutResult['dataStd'])[:, 2]) / num_images))

    LogManager.displayLog(f'TotalNo of image: {num_images}')

    LogManager.displayLog('Mean')
    print(totalMean)
    LogManager.displayLog('Std')
    print(totalStd)

    return np.array([totalMean]), np.array([totalStd])


def _parallelThreadForCalculateMeanStdOfDataset(imageFullPath, InResult, i):
    InResult['dataMean'][i] = (calculateMean(imageFullPath))
    InResult['dataStd'][i] = (calculateStd(imageFullPath))


# -- https://discuss.pytorch.org/t/normalization-in-the-mnist-example/457/11 for more info--#
def calculateMean(InImagePath):
    img = np.array(Image.open(InImagePath).convert('RGBA'))
    mean = np.mean(img / 255, axis=(0, 1))
    # print(mean)
    return mean


def calculateStd(InImagePath):
    img = np.array(Image.open(InImagePath).convert('RGBA'))
    std = np.std(img / 255, axis=(0, 1))
    # print(std)
    return std


def reduceDatasetTo(InImagePath, InImageFormat, InGroundTruthPath, InGroundTruthFormat, InTotalNo, InOutputDir):
    imageList = [f'{InImagePath}/{image}' for image in os.listdir(InImagePath) if image.endswith(f".{InImageFormat}")]
    imageList.sort()
    groundTruthList = [f'{InGroundTruthPath}/{gtFile}' for gtFile in os.listdir(InGroundTruthPath) if
                       gtFile.endswith(f".{InGroundTruthFormat}")]
    groundTruthList.sort()

    trainPath = f'{InOutputDir}/train'
    train_denPath = f'{InOutputDir}/train_den'

    testPath = f'{InOutputDir}/test'
    test_denPath = f'{InOutputDir}/test_den'

    FileManager.createFolder(trainPath)
    FileManager.createFolder(train_denPath)
    FileManager.createFolder(testPath)
    FileManager.createFolder(test_denPath)

    index = UtilityManager.getListOfRandomNo(len(imageList), InTotalNo)
    randIndex = UtilityManager.getListOfRandomNo(len(index), InTotalNo)

    totalTestSet = np.floor(len(index) * 0.2)

    # for i in range(InTotalNo):
    #     imgName, GTName = imageList[index[randIndex[i]]].split("/")[-1], groundTruthList[index[randIndex[i]]].split("/")[-1]
    #
    #     trainName = f'{trainPath}/{imgName}'
    #     groundTruthName = f'{train_denPath}/{GTName}'
    #
    #     LogManager.displayLog(
    #         f'Copying file from {imgName} ===> {trainName}')
    #     shutil.copy(f'{imageList[index[randIndex[i]]]}', trainName)
    #
    #     LogManager.displayLog(
    #          f'Copying file from {GTName} ===> {groundTruthName}')
    #     shutil.copy(f'{groundTruthList[index[randIndex[i]]]}', groundTruthName)

    # -- Train set --#
    for j in range(len(index)):
        imgName, GTName = imageList[index[randIndex[j]]].split("/")[-1], \
                          groundTruthList[index[randIndex[j]]].split("/")[-1]
        if j < totalTestSet:
            imgName, GTName = imageList[index[randIndex[j]]].split("/")[-1], \
                              groundTruthList[index[randIndex[j]]].split("/")[-1]

            trainName = f'{testPath}/{imgName}'
            groundTruthName = f'{test_denPath}/{GTName}'

            LogManager.displayLog(
                f'Copying file from {imgName} ===> {trainName}')
            shutil.copy(f'{imageList[index[randIndex[j]]]}', trainName)

            LogManager.displayLog(
                f'Copying file from {GTName} ===> {groundTruthName}')
            shutil.copy(f'{groundTruthList[index[randIndex[j]]]}', groundTruthName)

        else:
            trainName = f'{trainPath}/{imgName}'
            groundTruthName = f'{train_denPath}/{GTName}'

            LogManager.displayLog(
                f'Copying file from {imgName} ===> {trainName}')
            shutil.copy(f'{imageList[index[randIndex[j]]]}', trainName)

            LogManager.displayLog(
                f'Copying file from {GTName} ===> {groundTruthName}')
            shutil.copy(f'{groundTruthList[index[randIndex[j]]]}', groundTruthName)


# --For CSRNet, it need img and gt filepath list  in json list--#
def createFileListToJson(InDataname, InPath, InImageFormat='Png'):
    imageList = [image for image in os.listdir(InPath) if image.endswith(f".{InImageFormat}")]
    imageList.sort()

    f = open(f'{InDataname}.json', "w+")
    f.write("[")
    for i in range(len(imageList) - 2):
        # "/home/leeyh/Downloads/Shanghai/part_A_final/train_data/images/IMG_73.jpg",
        f.write(f'"{InPath}/{imageList[i]}",\n')
    f.write(f'"{InPath}/{imageList[len(imageList) - 1]}"\n')
    f.write("]")


def loadGroundTruthAndCreateMask(InPath, InOutput, InColor='blue'):
    LogManager.displayLog(f'Loading <{InPath.split("/")[-1]}> data..', InColor)
    filesList = [filename for filename in os.listdir(InPath) if os.path.isfile(os.path.join(InPath, filename))]
    filesList.sort()

    Filetype = filesList[0].split('.')[-1]

    outputPath = InOutput
    FileManager.createFolder(outputPath)

    totalFile = len(filesList)

    for i in range(totalFile):
        if Filetype == 'mat':
            mask = read_matFile(os.path.join(InPath, filesList[i]))
            imagePath = f'{filesList[i].replace("mat", "jpg")}'
            cv2.imwrite(os.path.join(outputPath, imagePath), mask * 255)
        if i % 100 == 0:
            LogManager.displayLog(f'Loading {i}/{totalFile}', 'green')


def read_matFile(InPath):
    mat = io.loadmat(InPath)
    imagePath = InPath.replace('ground_truth', 'images').replace('GT_IMG', 'IMG').replace('mat', 'jpg')
    img = plt.imread(imagePath)
    k = np.zeros((img.shape[0], img.shape[1]))
    try:
        gt = mat["image_info"][0, 0][0, 0][0]
    except:
        # UCF -50
        gt = mat["annPoints"]

    for i in range(0, len(gt)):
        if int(gt[i][1]) < img.shape[0] and int(gt[i][0]) < img.shape[1]:
            k[int(gt[i][1]), int(gt[i][0])] = 1
    return k



def createNonAugDataset(InRootPath, InOutPath, InDatasetName, InTestMode=False, Is_Split_Train_val=0.1):
    if InTestMode:
        train = f'{InRootPath}/test_data/images/'
        train_density = f'{InRootPath}/test_data/ground_truth/'
    else:
        train = f'{InRootPath}/train_data/images/'
        train_density = f'{InRootPath}/train_data/ground_truth/'

    dataPreparation(InDatabaseName=InDatasetName,
                                        InImagePath=train,
                                        InGroundTruthPath=train_density,
                                        InImageFormat='jpg',
                                        InGroundTruthFormat='mat',
                                        InIsBlock=1,
                                        Inoutput=InOutPath,
                                        Is_Split_Train_val=Is_Split_Train_val)

def balanceDataset(root):
    # --Part 1 -Load Daata ---
    import DataManager
    dataManager = DataManager.getDataManager()
    # root = '/media/ramdisk/ShtA_non_aug_patches_1'
    train = f'{root}/train/'
    train_density = f'{root}/train_den/'
    # train_mask = f'{root}/train_mask/'

    # val = f'{root}/val/'
    # val_density = f'{root}/val_den/'
    dataManager.load_train_data(InImagePath=train, InGroundTruth=train_density)
    # dataManager.load_mask_data(InTrainMask=train_mask, InValMask=None)

    X_train, y_train = dataManager.get_train_set(InTrainMode=False, InDataStandarisation=False)
    # train_mask, val_mask = dataManager.get_mask_set(InTrainMode=False)

    # Part 2 -- Balance and split data set --
    # train_dataOut, train_targetOut, val_dataOut, val_targetOut, train_mask, val_mask = \
    return DataManager.train_val_balance_split(X_train, y_train, [], [], InTestSplit=0.1)

def saveBalanceData(final_output, train_dataOut, train_targetOut, val_dataOut, val_targetOut, train_mask, val_mask):
    train_out = f"{final_output}/balance_dataset/NonAug/train/"
    train_den_out = f"{final_output}/balance_dataset/NonAug/train_den/"
    train_mask_out = f"{final_output}/balance_dataset/NonAug/train_mask/"

    val_out = f"{final_output}/balance_dataset/NonAug/val/"
    val_den_out = f"{final_output}/balance_dataset/NonAug/val_den/"
    val_mask_out = f"{final_output}/balance_dataset/NonAug/val_mask/"

    FileManager.createFolder(train_out)
    FileManager.createFolder(train_den_out)
    FileManager.createFolder(train_mask_out)

    FileManager.createFolder(val_out)
    FileManager.createFolder(val_den_out)
    FileManager.createFolder(val_mask_out)

    for i in range(len(train_dataOut)):
        UtilityManager.saveImageCv(f"{train_out}IMG_{i:05}.jpg", train_dataOut[i] * 255)
        # UtilityManager.saveToH5File(f"{train_mask_out}IMG_{i:05}.h5", train_mask[i] * 255)
        UtilityManager.saveToH5File(f"{train_den_out}GT_IMG_{i:05}.h5", train_targetOut[i])

    for i in range(len(val_dataOut)):
        UtilityManager.saveImageCv(f"{val_out}IMG_{i:05}.jpg", val_dataOut[i] * 255)
        # UtilityManager.saveToH5File(f"{val_mask_out}IMG_{i:05}.h5", val_mask[i] * 255)
        UtilityManager.saveToH5File(f"{val_den_out}GT_IMG_{i:05}.h5", val_targetOut[i])

def augmentData(root, outpath, InDatasetName, InTotalSplit=9):
    #  Part 3 -- Save the Balance data to Image --
    # root = '/ocean/anish/Developer/RnD/crowdCounting/_ExternalLib/data/shaghaiTech'
    X_out = f"{root}/balance_dataset/NonAug/train/"
    y_out = f"{root}/balance_dataset/NonAug/train_den/"
    x_mask_out = f"{root}/balance_dataset/NonAug/train_mask/"

    Xv_out = f"{root}/balance_dataset/NonAug/val/"
    yV_out = f"{root}/balance_dataset/NonAug/val_den/"
    xv_mask_out = f"{root}/balance_dataset/NonAug/val_mask/"

    # # # Part 4 -- Aug the data ----
    dataPreparation(InDatabaseName=f'{InDatasetName}_train',
                                        InImagePath=X_out,
                                        InGroundTruthPath=y_out,
                                        InImageFormat='jpg',
                                        InGroundTruthFormat='h5',
                                        InIsBlock=InTotalSplit,
                                        Inoutput=outpath,
                                        Is_Split_Train_val=False)

    dataPreparation(InDatabaseName=f'{InDatasetName}_val',
                                        InImagePath=Xv_out,
                                        InGroundTruthPath=yV_out,
                                        InImageFormat='jpg',
                                        InGroundTruthFormat='h5',
                                        InIsBlock=InTotalSplit,
                                        Inoutput=outpath,
                                        Is_Split_Train_val=False)
    #
    # CrowdCountingHelper.dataPreparation(InDatabaseName=f'{InDatasetName}_train_mask',
    #                                     InImagePath=X_out,
    #                                     InGroundTruthPath=x_mask_out,
    #                                     InImageFormat='jpg',
    #                                     InGroundTruthFormat='h5',
    #                                     InIsBlock=InTotalSplit,
    #                                     Inoutput=outpath,
    #                                     Is_Split_Train_val=False)
    #
    # CrowdCountingHelper.dataPreparation(InDatabaseName=f'{InDatasetName}_val_mask',
    #                                     InImagePath=Xv_out,
    #                                     InGroundTruthPath=xv_mask_out,
    #                                     InImageFormat='jpg',
    #                                     InGroundTruthFormat='h5',
    #                                     InIsBlock=InTotalSplit,
    #                                     Inoutput=outpath,
    #                                     Is_Split_Train_val=False)


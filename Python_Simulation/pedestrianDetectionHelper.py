# read json file
# get  joint min and max
# use cv to create bounding box
# green color box = r=0, g=255, b =0
import os
import Utility
import numpy as np
import cv2
import FileManager
import LogManager

def readCSVFiles(InPath):
    jointCSVFileList = [jointCSV for jointCSV in os.listdir(InPath) if jointCSV.endswith('.csv')]
    jointCSVFileList.sort()

    CSVList=[]
    for i in range(len(jointCSVFileList)):
        path = os.path.join(f'{InPath}/{jointCSVFileList[i]}')
        CSVList.append(Utility.readCSV(path))

    return CSVList
def readImageFiles(InPath, InExt='png'):
    backgroundImageList = [image for image in os.listdir(InPath) if image.endswith(InExt)]
    backgroundImageList.sort()

    imgList = []
    for i in range(len(backgroundImageList)):
        path = os.path.join(f'{InPath}/{backgroundImageList[i]}')
        imgList.append(Utility.readImage(path))

    return imgList
def minMaxPerFrame(InFrame):
    Agents=InFrame
    # find the row with zero joint info
    rowWithZeroValueIndex=[]
    for x in range(Agents.shape[0]):
        # start from index 4 as 0-3 are agentID, and agent color
        if np.sum(Agents[x][4:])<=0:
            rowWithZeroValueIndex.append(x)
    # remove the row with zero joint info
    for i in range(len(rowWithZeroValueIndex)):
        Agents = np.delete(Agents,(rowWithZeroValueIndex[i]-i), axis=0)

    totalAgent = Agents.shape[0]
    MinMaxPerAgent=[]
    for k in range(totalAgent):
        jointXList = []
        jointYList = []
        index = 0
        # extendBBox=2
        jointsInfoPerAgent=Agents[k][4:]
        # Loop through the col and extract joint x and joint y
        while index < len(jointsInfoPerAgent-2):
            jointXList.append(jointsInfoPerAgent[index])
            jointYList.append(jointsInfoPerAgent[index + 1])
            index += 2
        x = np.array(jointXList)
        y = np.array(jointYList)
        minX = np.min(x)
        maxX = np.max(x)
        minY = np.min(y)
        maxY = np.max(y)
        MinMaxPerAgent.append([minX, maxX, minY, maxY])

    return MinMaxPerAgent
def getMinMaxFromCSV(JointInfoList):
    LogManager.displayLog(f'Calculating bbox min and max .. ', InColor='blue')
    MinMax=[]
    for i in range(len(JointInfoList)):
        if i % 20==0:
            LogManager.displayLog(f'Loading Frame {i}', InColor='green')
        MinMax.append(minMaxPerFrame(JointInfoList[i]))
    return MinMax
def generate_data(BackgroundImageList, JointInfoList, minmax, Outpath='test/Pedestrian_DB/'):
    FileManager.createFolder(f'{Outpath}/images')
    FileManager.createFolder(f'{Outpath}/images_with_box')
    FileManager.createFolder(f'{Outpath}/annotation_bbox_minmax')
    FileManager.createFolder(f'{Outpath}/annotation_bbox_hw')
    for i in range(len(BackgroundImageList)):
        # Save the ground truth image
        Utility.saveImageCv(f'{Outpath}/images/{i:05}.png', BackgroundImageList[i])
        # make sure min and max are within the image
        bbox_minmax=""
        bbox_hw = ""
        for j in range(len(minmax[i])):
            agentMinMax = minmax[i][j]
            xmin, ymin = agentMinMax[0], agentMinMax[2]
            xmax, ymax = agentMinMax[1], agentMinMax[3]
            color = JointInfoList[i][j][1:4]
            # color = [0,255,0]
            h,w = BackgroundImageList[0].shape[:2]
            # check if avatar is outside the image, if true continue next for loop
            if (xmin <=0 or xmin >=w) and (xmax<=0 or xmax>=w) \
                    or (ymin<=0 or ymin>=h) and (ymax<=0 or ymax>=h):
                continue
            # draw rectangle around the agent
            cv2.rectangle(BackgroundImageList[i],
                          (xmin, ymin),(xmax, ymax),
                          (int(color[0]),int(color[1]),int(color[2])),2)
            # format string to be save as csv
            bbox_minmax+=f'person,{xmin},{ymin},{xmax},{ymax}\n'
            bbox_hw+=f'person,{xmin},{ymin},{abs(xmax-xmin)},{abs(ymax-ymin)}\n'
        # save string as csv .ie annotation of bbox of agent --
        with open(f"{Outpath}/annotation_bbox_minmax/{i:05}.csv", "w") as text_file:
            print(bbox_minmax, file=text_file)
        with open(f"{Outpath}/annotation_bbox_hw/{i:05}.csv", "w") as text_file:
            print(bbox_hw, file=text_file)
        # save image with box for preview purpose
        Utility.saveImageCv(f'{Outpath}/images_with_box/{i:05}.png', BackgroundImageList[i])

root='/home/anish/Developer/RnD/crowdSimulation/Unity_Visual/Compositing/Result/KU_SEC_Back_1_15_40_5'
JointInfoList = readCSVFiles(f'{root}/joint')
minmaxList = getMinMaxFromCSV(JointInfoList)
BackgroundImageList = readImageFiles(f'{root}/Ori', InExt='png')
generate_data(BackgroundImageList, JointInfoList, minmaxList)

import FileManager
import Utility
import os
from PIL import Image
import LogManager
import cv2
from scipy.misc import imread, imsave, imresize
import numpy as np
import Utility

def resizeImageTo(InImagePath, InImageExt, InResizeTo):
    folderPath= f'{InImagePath[:len(InImagePath)-7]}/_resizeVersion/'
    FileManager.createFolder(folderPath)
    # size = InResizeTo,InResizeTo

    max_height = InResizeTo
    max_width = InResizeTo

    imageList = [image for image in os.listdir(InImagePath) if image.endswith(f".{InImageExt}")]
    imageList.sort()

    for i in range(len(imageList)):
        # im = Image.open(f'{InImagePath}/{imageList[i]}',1)

        img = imread(f'{InImagePath}/{imageList[i]}')
        # --remove gray image --#
        if len(img.shape)<3:
            continue
        # height, width = img.shape[:2]
        #
        # # only shrink if img is bigger than required
        # if max_height < height or max_width < width:
        #     # get scaling factor
        #     scaling_factor = max_height / float(height)
        #     if max_width / float(width) < scaling_factor:
        #         scaling_factor = max_width / float(width)
            # resize image
            # img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        img = cv2.resize(img,(max_height, max_width),interpolation=cv2.INTER_AREA)
        LogManager.displayLog(f"Saving in {folderPath}{i:05}.jpg")
        imsave(f'{folderPath}{i:05}.jpg', img)
            # Utility.saveImageCv(f'{folderPath}{i:05}.jpg', img)
        #
        # if im.layers == 3:
        #     im.thumbnail(size, Image.ANTIALIAS)
        #     # im.save(f'{InImagePath}/_resizeVersion/', "JPEG")
        #     LogManageimg.shaper.displayLog(f'Saving {folderPath}{i:05}.jpg')
        #     im.save(f'{folderPath}{i:05}.jpg',"JPEG" )

def convertColorToFitGAN(InPathToSegmentedImage, InOutput):
    folderPath = os.path.join(InOutput)
    FileManager.createFolder(folderPath)

    filesList = [filename for filename in os.listdir(InPathToSegmentedImage) if
                 os.path.isfile(os.path.join(InPathToSegmentedImage, filename))]
    filesList.sort()

    for i in range(len(filesList)):

        img = cv2.imread(os.path.join(InPathToSegmentedImage, filesList[i]))
        img = img.astype(np.float32, copy=False)

        # Conver to RGB
        image =img[...,::-1]
        #
        # find black and convert it into pink -- walk way path color
        R = image[:,:,0]
        G = image[:,:,1]
        B= image[:,:,2]

        # Convert Black to pink - ie walk way
        a=128,
        b=64
        c =128
        R[R[:]==0] = a
        G[G[:]==0] = b
        B[B[:]==0] =c

        # # covert bg to green  i.e grass
        # R[R[:] == 0] = 154
        # G[G[:] == 0] = 250
        # B[B[:] == 0] = 152

        # if not pink convert to red - ie crowd
        R[R[:]!=a] = 220
        G[G[:]!=b] = 20
        B[B[:]!=c] = 60

        newImage = img
        newImage[:, :, 0] = B
        newImage[:, :, 1] = G
        newImage[:, :, 2] = R



        Utility.saveImageCv(os.path.join(InOutput,f'{i:04}.png'),newImage)





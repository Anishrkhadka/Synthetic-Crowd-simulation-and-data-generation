# -- Need to load any image and convert it to png format also extract background --#
import os

import cv2


class getBackground:
    def __init__(self):
        self.imageHeight = None
        self.imageWidth = None
        self.imageType = None
        self.imageList = None

    def loadBackground(self, InImagePathFolder, InImageExtension):
        # -- Get the image in InImagePathFolder with InImageExtension and sort it -- #
        self.imageList = [imageFile for imageFile in os.listdir(InImagePathFolder) if
                          imageFile.endswith(f".{InImageExtension}")]
        self.imageList.sort()
        # - removes alpha channel --#
        singleImage = cv2.imread(filename=f'{InImagePathFolder}/{self.imageList[0]}', flags=cv2.IMREAD_COLOR)

        # import matplotlib.pyplot as plt
        # singleImage = plt.imread(f'{InImagePathFolder}/{self.imageList[0]}')
        # a = Utility.getCameraFocalLengthEstimation(InImageWidth=singleImage.shape[1], InFOV=50)
        imageHeight, imageWidth, channel = singleImage.shape
        # image = np.zeros([singleImage.shape], dtype='int')

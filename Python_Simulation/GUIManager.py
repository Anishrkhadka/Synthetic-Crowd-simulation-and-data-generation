import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button



class getWindow:
    def __init__(self):
        self.background =None
        self.waitForKeyBoard = True
        self.gridMap = None
        self.imageSize = None
        self.fig, self.ax = plt.subplots()
        # self.fig = plt.figure()
        # self.ax = self.fig.add_subplot(111)
        # -- Get the X key from keyboard to quit the matplot -- #
        self.fig.canvas.mpl_connect('key_press_event', self.keyEvent)
        self.IsGridMapPositionSet = False

    def setBackground(self, InBackground):
        self.background = InBackground

    def show(self):
        self.ax.imshow(self.background)

        # self.ax.imshow(self.background)
    def pltShow(self):
        plt.show()

    def setTitle(self, InTitle):
        self.ax.set_xlabel(InTitle)

    def showWidget(self):
        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, 'Left')
        bnext.on_clicked(self.moveGridToLeft())
        bprev = Button(axprev, 'Right')
        bprev.on_clicked(self.moveGridToRight())

    @staticmethod
    def getPointFromUser(InIndex=None):
        return np.asarray(plt.ginput(1, timeout=-1))


    def plotPoint(self, InX, InY, Informat='o', InMarkerSize=1):
        self.ax.plot(InX, InY, Informat, markersize=InMarkerSize)

    def plotBox(self, InX, InY, Informat='r'):
        self.ax.plot(InX, InY, Informat, markersize=1)


    def plotLine(self, InX, InY, InLinewidth=2, Informat='ro'):
        self.ax.plot(InX, InY)

    def plotImage(self, InImageArray, InFileName=None, InIsFlip=False):
        # self.ax.imshow(InImageArray, interpolation='nearest')
        #
        # if InIsFlip:
        #     self.ax.gca().invert_yself.axis()
        #
        # if InFileName:
        #     self.ax.imsave(InFileName, InImageArray)
        #     self.ax.close()

        self.ax.imshow(InImageArray, interpolation='nearest')
        if InIsFlip:
            plt.gca().invert_yaxis()
        # self.ax.show()

        if InFileName:
            plt.savefig(InFileName, bbox_inches='tight')
            # self.ax.close()


    def plotPointOnImage(self, InX, InY, InIsFlip=False, InSymbol='o', InMarkerSize=1):
        im = self.ax.imshow(self.background)
        if InIsFlip:
            plt.ylim(plt.ylim()[::-1])
        self.plotPoint(InX, InY, InSymbol, InMarkerSize)


    def plotPointOnImageAndSave(self, InX, InY, InIsFlip, InFileName=None):
        self.full_frame()

        self.plotPointOnImage(InX, InY, InIsFlip, "yv", InMarkerSize=2)

        if InFileName:
            plt.savefig(InFileName, bbox_inches='tight')


    def full_frame(self, width=None, height=None):
        import matplotlib as mpl
        mpl.rcParams['savefig.pad_inches'] = 0
        figsize = None if width is None else (width, height)
        self.fig = plt.figure(figsize=figsize)
        self.ax = plt.axes([0, 0, 1, 1], frameon=False)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        plt.autoscale(tight=True)

    def plotGridMap(self, InGridMap, InImageHeight):
        self.gridMap = InGridMap
        self.imageSize = InImageHeight

        self.plotPoint(self.gridMap[:, :, 0],
                       self.imageSize - self.gridMap[:, :, 1])


    def moveGridToLeft(self, InMoveBy =20):
        del self.ax.lines[0:]
        self.gridMap[:, :, 0] -= InMoveBy
        self.plotPoint(self.gridMap[:, :, 0],
                       self.imageSize - self.gridMap[:, :, 1])
        self.show()
        return self.gridMap

    def moveGridToRight(self,InMoveBy = 20):
        del self.ax.lines[10:]
        self.gridMap[:, :, 0] += InMoveBy
        self.plotPoint(self.gridMap[:, :, 0],
                       self.imageSize - self.gridMap[:, :, 1])
        self.show()
        return self.gridMap

    def moveGridToUp(self, InMoveBy = 20):
        del self.ax.lines[10:]
        self.gridMap[:, :, 1] += InMoveBy
        self.plotPoint(self.gridMap[:, :, 0],
                       self.imageSize - self.gridMap[:, :, 1])
        self.show()
        return self.gridMap

    def moveGridToDown(self,InMoveBy=20):
        del self.ax.lines[10:]
        self.gridMap[:, :, 1] -= InMoveBy
        self.plotPoint(self.gridMap[:, :, 0],
                       self.imageSize - self.gridMap[:, :, 1])
        self.show()
        return self.gridMap

    def getWaitForKeyBoard(self):
        return self.waitForKeyBoard

    def keyEvent(self, event):
        print(event.key)
        if event.key == 'q':
            self.waitForKeyBoard = False
        if event.key == 'left':
            self.moveGridToLeft()
        if event.key == 'right':
            self.moveGridToRight()
        if event.key == 'up':
            self.moveGridToUp()
        if event.key == 'down':
            self.moveGridToDown()

        if event.key == 'enter':
            self.IsGridMapPositionSet = True

    def getIsGridMapPositionSet(self):
        return self.IsGridMapPositionSet

    def getGridMap(self):
        return self.gridMap

    def saveImage(self, InFilePath):
        self.full_frame()
        im = self.ax.imshow(self.background, cmap=plt.get_cmap('jet'))
        plt.savefig(InFilePath, bbox_inches='tight' )
        plt.close('all')

    def closeFigure(self):
        plt.close('all')

# fig.canvas.mpl_connect('button_press_event', on_press)
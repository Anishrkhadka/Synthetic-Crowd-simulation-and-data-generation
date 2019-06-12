import threading

import numpy as np

import AgentsProcessManager
import LogManager
import MapManager
import PathManager
import Utility


# import  cython
class getAgents:

    def __init__(self, InSettings):
        self.simulationSettings = InSettings
        self.totalNumberOfAgents = InSettings.getTotalNumberOfAgentsForSimulation()
        self.sampleAgentProperties = {'ID': 0,
                                      'FOV': 5,
                                      'MaxSpeed': 0.7,
                                      'MaxRotation': 6,
                                      'MaxAcceleration': 90,
                                      'MaxAngularAcceleration': 90,
                                      'Position': np.array([-1000, -1000], dtype='float'),
                                      'Velocity': np.array([0, 0], dtype='float'),
                                      'SegmentNumber': 0,
                                      'Orientation': 0,
                                      'Rotation': 0,
                                      'StartLocation': None,
                                      'EndLocation': None,  # Destination
                                      'Radius': None,
                                      'FrameNumber': None,
                                      'State': None,
                                      'ProxyAgents': None,
                                      'ProxyObject': None,
                                      'Path': None,
                                      'Path2': None,
                                      'Map': None,
                                      'MapProperties': None,
                                      }
        self.pathFinder = PathManager.PathFinder()
        self.gridMap = None
        self.gridMapProperties = None
        self.gridMapForPathFinder = None
        rand_seed = 64678
        np.random.seed(rand_seed)

    def getGripMapAndItsProperties(self):
        # -- Load the gridMap from file for Path Finder algorithm -- #
        # -- orientation of grid need to fix for agent to appear in right position --  #
        MapManager.setTheGripMapToRightOrientation(self.simulationSettings.getGridMapFilePath())
        # -- From here on it will use this modified map -- #
        self.gridMap = MapManager.getGridMapFromFile(self.simulationSettings.getGridMapFilePath())
        self.gridMapProperties = MapManager.getGripMapProperties(InGridMap=self.gridMap, InMapUnitSize=1)

        self.gridMapForPathFinder = MapManager.convertGripMapToPathFinderFormat(self.gridMap)

    def createAgentDetail(self):

        # -- create list of agents with sample Agent Properties -- #
        LogManager.displayLog(self.totalNumberOfAgents, InName="Total Number of Agents")

        OutAgentsList = []
        xNoOfMoreValue = 100

        # -- Run the path finder-- #
        self.pathFinder.setGripMap(self.gridMapForPathFinder)

        # -- Generate random distance to be used for generation of path -- #
        setOfRandomDistanceForInAndOut = Utility.getListOfRandomNo(
            InRange=self.simulationSettings.getMaxDistanceForInAndOutForAgent(),
            InNumberOfValue=self.totalNumberOfAgents + xNoOfMoreValue, InIsRepeatNo=True)


        # -- Make sure all the path distance are more 4 -- #
        setOfRandomDistanceForInAndOut[setOfRandomDistanceForInAndOut < self.simulationSettings.getMaxDistanceForInAndOutForAgent()] = self.simulationSettings.getMaxDistanceForInAndOutForAgent()
        # setOfRandomDistanceForInAndOut[setOfRandomDistanceForInAndOut < 15] = 15
        # -- Get the list of path --#
        pathList = self.pathFinder.getListOfPathForAgents(InTotalNoOfPath=self.totalNumberOfAgents + xNoOfMoreValue,
                                                          InLengthOfPath=setOfRandomDistanceForInAndOut)

        setOfRandomIndexForPath = Utility.getListOfRandomNo(
            InRange=self.totalNumberOfAgents + xNoOfMoreValue,
            InNumberOfValue=self.totalNumberOfAgents)

        # setOFRandomRadius = np.array([0,-0.1, 0.1, -0.05, -0.15, 0.05])
        setOFRandomRadius = np.array([-0.1, 0.1, -0.05, -0.15, 0.05])
        setOfRandomIndexForRadius = Utility.getListOfRandomNo(InRange=setOFRandomRadius.shape[0],
                                                              InNumberOfValue=self.totalNumberOfAgents,
                                                              InIsRepeatNo=True)

        setOFIncreasingValueForFrame = Utility.getListOfRandomNo(
            InRange=self.simulationSettings.getTotalNumberOfSimulatedFrame(),
            InNumberOfValue=self.totalNumberOfAgents, InIsRepeatNo=True)

        setOfRandomIndexForFrame = Utility.getListOfRandomNo(InRange=self.totalNumberOfAgents,
                                                             InNumberOfValue=self.totalNumberOfAgents,
                                                             InIsRepeatNo=False)

        # setOfDistinationNo = np.arange(start=1, stop=self.pathFinder.getTotalNumberOfStartEndPointInGrid(), step=1)

        # -- Create the total Number of Agents -- #
        for i in range(0, self.totalNumberOfAgents):
            # -- added to the list -- #
            OutAgentsList.append(self.sampleAgentProperties.copy())
            # -- create a unique i -- #
            OutAgentsList[i]['ID'] = i
            # -- get a list of path with random start, end path -- #
            OutAgentsList[i]['Path'] = pathList[setOfRandomIndexForPath[i]]
            if self.totalNumberOfAgents <= 15:
                # print(f"Id= {i}")
                Utility.displayPath(pathList[setOfRandomIndexForPath[i]], self.gridMapForPathFinder, i,
                                    self.simulationSettings)

            OutAgentsList[i]['StartLocation'] = np.asarray(pathList[setOfRandomIndexForPath[i]][0][:], dtype='float')
            OutAgentsList[i]['CurrentEndLocation'] = np.asarray(pathList[setOfRandomIndexForPath[i]][-1][:],
                                                                dtype='float')

            # agentList[i]['EndLocation'] = setOfDistinationNo[Utility.getListOfNonRepeatingRandomNo(InRange=setOfDistinationNo.shape[0], InNumberOfValue=1)]
            OutAgentsList[i]['EndLocation'] = i
            OutAgentsList[i]['Radius'] = np.around(0.45 + setOFRandomRadius[setOfRandomIndexForRadius[i]], decimals=5)
            OutAgentsList[i]['State'] = 'PathFollow'
            OutAgentsList[i]['FrameNumber'] = setOFIncreasingValueForFrame[setOfRandomIndexForFrame[i]]



        return OutAgentsList

    # -- step 1 -- #
    def updateAgents(self, InAgentList):

        LogManager.displayLog('Simulation Started')

        frameNumber = self.simulationSettings.getInitialFrameNumber()
        startFrame = 0
        totalFrameForSimulation = self.simulationSettings.getTotalNumberOfFrameForSimulation()
        IsFinishedAgentLoop = False
        simulationFrameRate = self.simulationSettings.getSimulationFrameRate()

        # -- Placeholder for final Position and Rotation of Agents  -- #
        finalAgentPositionMatrix = np.zeros([totalFrameForSimulation, self.totalNumberOfAgents * 2], dtype='float')
        finalAgentPositionMatrix[finalAgentPositionMatrix == 0] = -1000
        finalAgentsRotationMatrix = np.zeros([totalFrameForSimulation, self.totalNumberOfAgents], dtype='float')
        frameCounterForFinalDetails = 0

        # -- Main Loop --#
        while frameNumber < totalFrameForSimulation - 1 and IsFinishedAgentLoop == False:
            frameNumber += 1

            # -- Create a single thread for each agent -- #
            resultsFromParallelThreads = self.runParallelProcess(InAgentList, frameNumber)

            # -- Non parallel version -- #
            # resultsFromParallelThreads = self.runNonParallelProcess(InAgentList, frameNumber)

            InAgentList = resultsFromParallelThreads['getAgentList']

            totalNoOfAgentWhoFinishedPath = np.sum(
                np.asarray(resultsFromParallelThreads['totalNoOfAgentsWhoFinishedPath']))

            if totalNoOfAgentWhoFinishedPath == self.totalNumberOfAgents:
                IsFinishedAgentLoop = True

            frameCounterForFinalDetails = self.getFrame(InAgentList,
                                                        frameNumber,
                                                        simulationFrameRate,
                                                        startFrame,
                                                        finalAgentPositionMatrix,
                                                        finalAgentsRotationMatrix,
                                                        frameCounterForFinalDetails)

        return InAgentList, finalAgentPositionMatrix, finalAgentsRotationMatrix

    def runParallelProcess(self, InAgentList, InFrameNumber):
        OutResultsFromParallelThreads = {'getAgentList': InAgentList,
                                         'totalNoOfAgentsWhoFinishedPath': np.zeros([self.totalNumberOfAgents, 1])}

        parallelThreads = []
        for agentIndex in range(0, self.totalNumberOfAgents):
            threads = threading.Thread(target=self.parallelSimulationForNoOFAgents,
                                       args=(OutResultsFromParallelThreads, InFrameNumber, agentIndex))
            threads.setDaemon(True)
            parallelThreads.append(threads)
            # print(f'Thread {agentIndex} started')
            threads.start()

        for tt in parallelThreads:
            tt.join()


        return OutResultsFromParallelThreads

    def runNonParallelProcess(self, InAgentList, InFrameNumber):
        OutResultsFromParallelThreads = {'getAgentList': InAgentList,
                                         'totalNoOfAgentsWhoFinishedPath': np.zeros([self.totalNumberOfAgents, 1])}

        for agentIndex in range(0, self.totalNumberOfAgents):
            self.parallelSimulationForNoOFAgents(OutResultsFromParallelThreads, InFrameNumber, agentIndex)

        return OutResultsFromParallelThreads

    def getFrame(self, InAgentList, frameNumber, simulationFrameRate, startFrame, finalAgentPositionMatrix,
                 finalAgentsRotationMatrix, frameCounterForFinalDetails):
        # -- Store Agent Position and Rotation best on Frame Rate i.e 1 pos,1 rot for 12fps
        if np.mod(frameNumber, simulationFrameRate) == 0 and frameNumber > startFrame:
            pos, rot = self.reshapeAgentPositionAndRotationToOneLine(InAgentList)

            finalAgentPositionMatrix[frameCounterForFinalDetails, :] = pos
            finalAgentsRotationMatrix[frameCounterForFinalDetails, :] = rot

            frameCounterForFinalDetails += 1
            if frameCounterForFinalDetails % 20==0:
                LogManager.displayLog(f'frame number = {frameCounterForFinalDetails}', InColor='yellow')
        return frameCounterForFinalDetails

    def parallelSimulationForNoOFAgents(self, Out, InFrameNumber, index):
        # print(f'current thread={threading.current_thread()}')
        InAgentList = Out['getAgentList']
        totalNoOfAgentsWhoFinishedPath = Out['totalNoOfAgentsWhoFinishedPath']

        # -- first check the agents -- #
        if InFrameNumber >= InAgentList[index]['FrameNumber'] and \
                InAgentList[index]['SegmentNumber'] >= 0:

            # -- if agent is ready to enter the scene then change the position to startLocation --- #
            if AgentsProcessManager.IsAgentReadyToEnterTheScene(InAgentList[index], InFrameNumber):
                InAgentList[index]['Position'] = InAgentList[index]['StartLocation']
                InAgentList[index]['SegmentNumber'] = 1

                # InAgentList[index]['ProxyObject'], visionList, riskList = \
                #     AgentsProcessManager.getVisibleObjectInScene(InAgentList[index], self.gridMapProperties)

                # -- check if we have risk --#
                #     if riskList:
                #         print('RiskList is true!!')
                #         gridMap = self.gridMap.copy()
                #         for i in range(len(riskList)):
                #             gridMap = MapManager.updateGridMapWithRiskInfo(gridMap, riskList[i])
                #         # -- Update grid map properties after updating risk -- #
                #         self.gridMapProperties = MapManager.getGripMapProperties(gridMap)
                #         # -- Cover this new grid map to PathFinder Formation -- #
                #         gridMapForPathFinder = MapManager.convertGripMapToPathFinderFormat(gridMap)
                #         # -- Set the new Grip Map in pathFinder-- #
                #         self.pathFinder.setGripMap(gridMapForPathFinder)
                #         # -- Update the path -- #
                #         path =  np.squeeze(self.pathFinder.getListOfPathForAgents(InTotalNoOfPath=1, InLengthOfPath=8,InStartPosition= InAgentList[index]['StartLocation']))
                #         InAgentList[index]['Path'] = np.asarray(path, dtype='float')
                #         InAgentList[index]['Path2'] = None
                #         InAgentList[index]['SegmentNumber'] = 0
                #         InAgentList[index]['StartLocation'] = InAgentList[index]['Path'][0]
                #         InAgentList[index]['CurrentEndLocation'] = InAgentList[index]['Path'][-1]
                #         InAgentList[index]['Position'] = InAgentList[index]['StartLocation']
                #         InAgentList[index]['Velocity'] = np.array([0, 0], dtype='float')
                #         InAgentList[index]['Orientation'] = 0
                #         InAgentList[index]['Rotation'] = 0

                InAgentList[index]['ProxyAgents'] = AgentsProcessManager.getProximityAgents(InAgentList,
                                                                                            InAgentID=index)

            agentSteeringInfo = {'Velocity': np.array([0, 0], dtype='float'), 'Rotation': np.array([0], dtype='float')}

            # InAgentList[index], agentSteeringInfo = AgentsProcessManager.updateAgentsGroupVelocity(
            #     InAgentList[index])
            InAgentList[index], agentSteeringInfo = AgentsProcessManager.updateAgentVelocity(agentSteeringInfo,
                                                                                             InAgentList[index])

            InAgentList[index] = AgentsProcessManager.updateKinematicsOfAgentWithSteeringInfo(InAgentList[index],
                                                                                              agentSteeringInfo,
                                                                                              self.simulationSettings)

        elif InAgentList[index]['SegmentNumber'] < 0:
            # as Path2 is never set -- #
            # if InAgentList[index]['Path2'] is not None:
            #     InAgentList[index]['Path'] = InAgentList[index]['Path2']
            #     InAgentList[index]['Path2'] = None
            #     InAgentList[index]['StartLocation'] = np.asarray(InAgentList[index]['Path'][0])
            #     InAgentList[index]['CurrentEndLocation'] = np.asarray(InAgentList[index]['Path'][-1])
            #     InAgentList[index]['EndLocation'] = InAgentList[index]['Destination2']
            #     InAgentList[index]['Position'] = np.array([-1000, -1000])
            #     InAgentList[index]['Velocity'] = np.array([0, 0], dtype='float')
            #     InAgentList[index]['Orientation'] = np.array([0, 0], dtype='float')
            #     InAgentList[index]['Rotation'] = 0
            # else:
            totalNoOfAgentsWhoFinishedPath[index] = 1
            InAgentList[index]['Position'] = np.array([-1000, -1000], dtype='float')
        else:
            # -- if the agent is not in the scene yet move the agent out of the scene -- #
            InAgentList[index]['Position'] = np.array([-1000, -1000], dtype='float')

        Out['getAgentList'] = InAgentList
        Out['totalNoOfAgentsWhoFinishedPath'] = totalNoOfAgentsWhoFinishedPath


    def reshapeAgentPositionAndRotationToOneLine(self, InAgentList):
        agentPositionList = []
        agentRotationList = []

        for x in range(len(InAgentList)):
            agentPositionList.append(InAgentList[:][x]['Position'])
            agentRotationList.append(InAgentList[:][x]['Orientation'])

        agentPosition = np.asarray(agentPositionList)
        agentRotation = np.asarray(agentRotationList)

        return agentPosition.reshape(1, self.totalNumberOfAgents * 2).copy(), \
               agentRotation.reshape(1, self.totalNumberOfAgents).copy()

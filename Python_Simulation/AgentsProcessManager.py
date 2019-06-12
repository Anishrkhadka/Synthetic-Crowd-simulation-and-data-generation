import Utility
import numpy as np
import LogManager

def IsAgentReadyToEnterTheScene(InSingleAgent, InFrameNumber):
    if InFrameNumber >= InSingleAgent['FrameNumber'] and \
            InSingleAgent['SegmentNumber'] == 0:
        return True
    else:
        return False


def getVisibleObjectInScene(InSingleAgent, InGridMapProperties, InTotalNoOfRay=7, InMapUnitSize=1):
    # newMapProperties = InGridMapProperties.copy()
    rotationAngles = np.array([0, -15, 15, 30, -30, -45, 45, 60, -60, -75, 75, 90, -90, -100, 100])

    OutVisionList = []
    OutProxyObjectList = []
    positionRisksList = []
    OutRiskList = []

    for i in range(InTotalNoOfRay):
        rayEndPointVector = Utility.getRotateVector(Utility.getNormalisedVector(InSingleAgent['Velocity']),
                                                    rotationAngles[i])
        rayEndPoint = InSingleAgent['Position'] + (rayEndPointVector * (InSingleAgent['FOV'] * (1 / InMapUnitSize)))

        seenList, InGridMapProperties = getRayIntersect(InRayOriginPoint=InSingleAgent['Position'],
                                                        InRayEndPoint=rayEndPoint,
                                                        InGridMapProperties=InGridMapProperties,
                                                        InRayID=i)
        if seenList:
            OutVisionList.append(seenList[0])

    if len(OutVisionList) > 0:
        # -- get obstacles only --#
        OutProxyObjectList = [item for item in OutVisionList if item['Height'] > 0]
        # -- get Risk obstacles -- #
        # positionRisksList = [item for item in OutVisionList if item['Risk'] > 0]

        # -- if there are any risk -- #
        # if len(positionRisksList) > 0:
        #     for i in range(0,len(positionRisksList)):
        #         if positionRisksList[i]['Seen'] < 7:
        #             OutRiskList.append(positionRisksList[i])

    return OutProxyObjectList, OutVisionList, OutRiskList


def getRayIntersect(InRayOriginPoint, InRayEndPoint, InGridMapProperties, InRayID):
    # OutGridMapProperties = OutGridMapProperties.copy()
    OutSeenList = []

    # -- if InRayOriginPoint and InRayEndPoint is not same  i.e if they are same there will be no euclideanDistance --#
    # - as a results LAB will be Zero and it will lead to NaN value for others --
    if (InRayOriginPoint != InRayEndPoint).all():

        hitsList = []
        ts = np.array([0])

        LAB = Utility.getEuclideanDistance(InRayOriginPoint, InRayEndPoint)

        # -- Direction from Vector InRayOriginPoint to InRayEndPoint -- #
        Dx, Dy = (InRayEndPoint - InRayOriginPoint) / LAB

        for i in range(0, len(InGridMapProperties)):
            # t = (Dx * (InGridMapProperties[i]['Position'][0] - InRayOriginPoint[0])) + \
            #     (Dy * (InGridMapProperties[i]['Position'][1] - InRayOriginPoint[1]))

            x, y = InGridMapProperties[i]['Position'] - InRayOriginPoint
            t = Dx * x + Dy * y

            Exy = [t * Dx + InRayOriginPoint[0], t * Dy + InRayOriginPoint[1]]
            # Ey = t * Dy + InRayOriginPoint[1]

            LEC = Utility.getEuclideanDistance(Exy, InGridMapProperties[i]['Position'])

            if LEC < InGridMapProperties[i]['Radius'] * 1:
                if 0 <= t <= LAB:
                    if InGridMapProperties[i]['Seen'] == 0:
                        InGridMapProperties[i]['Seen'] = InRayID

                    hitsList.append(InGridMapProperties[i])
                    ts = np.vstack([ts, t])

        # - Remove the zero -- #
        ts = ts[1:]

        if ts.shape[0] > 0:
            # -- Sort row --#
            ts = ts[ts[:, 0].argsort(),]
            inds = ts[:, 0].argsort()

            visibleHeight = 0

            for i in range(0, inds.shape[0] - 1):

                if hitsList[inds[i]]['Height'] >= visibleHeight:
                    if hitsList[inds[i]]['Seen'] == InRayID:
                        hitsList[inds[i]]['Visibility'] = getVisibility(InRayID)
                        OutSeenList.append(hitsList[inds[i]])

                if hitsList[inds[i]]['Height'] > visibleHeight:
                    visibleHeight = hitsList[inds[i]]['Height']

                if visibleHeight >= 1:
                    break

    return OutSeenList, InGridMapProperties


# - Simple switch case -- #
def getVisibility(InRayID):
    switch = {
        1: 1,
        2: 0.6,
        3: 0.6,
        4: 0.6,
        5: 0.6,
        6: 0.4,
        7: 0.4,
        8: 0.4,
        9: 0.3,
        10: 0.3,
        11: 0.3,
        12: 0.2,
        13: 0.2,
        14: 0.2,
        15: 0.2
    }
    return switch.get(InRayID)


# -- Not necessary for now --#
def getVisibilityState(InVisionList, InCurrentSceneVision):
    OutCurrentSceneVision = InCurrentSceneVision.copy()

    for i in range(0, len(InVisionList)):
        OutCurrentSceneVision[InVisionList[i]['Position'][0],
                              InVisionList[i]['Position'][1]] += InVisionList[i]['Visibility']

    return OutCurrentSceneVision


def getProximityAgents(InAgentList, InAgentID):
    proxyAgentsList = []
    aperture = np.pi

    # -- Loop through the agent list to find if other agents are in InAgentID the corn vision -- #
    for i in range(0, len(InAgentList)):

        if i != InAgentID:
            radius = InAgentList[InAgentID]['Radius'] + InAgentList[i]['Radius']
            # -- Check if agents are on top of another -- #
            if Utility.getVectorMagnitude(InAgentList[InAgentID]['Position'] - InAgentList[i]['Position']) < radius:
                proxyAgentsList.append(InAgentList[i])

            coneBase = InAgentList[InAgentID]['Position'] + \
                       Utility.getNormalisedVector(InAgentList[InAgentID]['Velocity']) * \
                       InAgentList[InAgentID]['FOV']

            # -- Is the position of the Agent inside a cone and not on top of the source -- #
            if Utility.getIsPointInsideFOVCorn(InAgentList[i]['Position'],
                                               InAgentList[InAgentID]['Position'],
                                               coneBase,
                                               aperture):
                proxyAgentsList.append(InAgentList[i])


    return proxyAgentsList


def updateAgentsGroupVelocity(InSingleAgent):
    OutSingleAgent = InSingleAgent.copy()

    OutSteering = {'Velocity': np.array([0, 0], dtype='float'), 'Rotation': np.array([0], dtype='float')}

    # -- threshold is eps ie. np.power(2.0, -52) -- #
    threshold = np.finfo(float).eps
    # threshold = np.power(2.0, -52)
    # --Group 1 -- #
    groupVelocity1 = np.array([0, 0], dtype='float')
    tempVelocity = agentAvoidance(OutSingleAgent)
    groupVelocity1 += tempVelocity
    tempVelocity = objectAvoidance(OutSingleAgent)
    groupVelocity1 += tempVelocity

    # - Group 2 - #
    groupVelocity2 = np.array([0, 0], dtype='float')
    tempVelocity = agentSeparation(OutSingleAgent)
    groupVelocity2 += tempVelocity

    groupVelocity3 = np.array([0, 0], dtype='float')
    tempVelocity, OutSingleAgent = pathFollow(OutSingleAgent)
    groupVelocity3 += tempVelocity

    if Utility.getVectorMagnitude(groupVelocity1) > threshold:
        OutSteering['Velocity'] = groupVelocity1
    elif Utility.getVectorMagnitude(groupVelocity2) > threshold:
        OutSteering['Velocity'] = groupVelocity2
    else:
        OutSteering['Velocity'] = groupVelocity3

    OutSingleAgent, OutSteering['Rotation'] = lookWhereYourGoing(OutSingleAgent)

    return OutSingleAgent, OutSteering


def updateAgentVelocity(InSteering, InSingleAgent):
    OutSteering = InSteering.copy()
    OutSingleAgent = InSingleAgent.copy()

    # -- list of implemented algorithms [Zheng, PathFollow, Boids]-- #
    # crowdSimulationAlgorithmName = 'Zheng'
    # LogManager.displayLog(f'Using [ {crowdSimulationAlgorithmName} ] for crowd Simulation')
    OutSingleAgent, OutSteering = getCrowdSimulationAlgorithm('Zheng', OutSingleAgent, OutSteering)

    return OutSingleAgent, OutSteering


def getCrowdSimulationAlgorithm(InNameOfAlgorithm, InSingleAgent, InSteering):
    if InNameOfAlgorithm == 'Zheng':
        return Zheng(InSingleAgent, InSteering)
    if InNameOfAlgorithm == 'PathFollow':
        return PathFollow(InSingleAgent, InSteering)
    if InNameOfAlgorithm == 'Boids':
        return Boids(InSingleAgent, InSteering)


def Zheng(InSingleAgent, InSteering):

    tempVelocity = agentSeparation(InSingleAgent)
    InSteering['Velocity'] += (tempVelocity * 1)
    tempVelocity = agentAvoidance(InSingleAgent)
    InSteering['Velocity'] += (tempVelocity * 2)
    # tempVelocity = objectAvoidance(InSingleAgent)
    # InSteering['Velocity'] += (tempVelocity * 5)

    velocity, OutSingleAgent = pathFollow(InSingleAgent)
    InSteering['Velocity'] += (velocity * 1)


    return OutSingleAgent, InSteering

def PathFollow(InSingleAgent, InSteering):
    InSingleAgent['State'] = 'PathFollow'
    tempVelocity = agentSeparation(InSingleAgent)
    InSteering['Velocity'] += (tempVelocity * 1)
    tempVelocity = agentAvoidance(InSingleAgent)
    InSteering['Velocity'] += (tempVelocity * 3)
    tempVelocity = objectAvoidance(InSingleAgent)
    InSteering['Velocity'] += (tempVelocity * 5)
    tempVelocity, InSingleAgent = pathFollow(InSingleAgent)
    InSteering['Velocity'] += (tempVelocity * 1)

    InSingleAgent, OutRotation = lookWhereYourGoing(InSingleAgent)
    InSteering['Rotation'] += OutRotation

    return  InSingleAgent, InSteering

def Boids(InSingleAgent, InSteering):
    tempVelocity = objectAvoidance(InSingleAgent)
    InSteering['Velocity'] += (tempVelocity * 3)
    tempVelocity, InSingleAgent = pathFollow(InSingleAgent)
    InSteering['Velocity'] += (tempVelocity * 5)
    InSingleAgent['Orientation'] = np.rad2deg(Utility.getAtan2(InSingleAgent['Velocity'][0], InSingleAgent['Velocity'][1]))

    return InSingleAgent, InSteering

def agentSeparation(InSingleAgent):
    OutVelocity = np.array([0, 0], dtype='float')

    # -- if there are any agent around the current agent --#
    if InSingleAgent['ProxyAgents']:
        personalSpace = (InSingleAgent['Radius'] + 0.45) * 1
        # personalSpace = (InSingleAgent['Radius'] + 0.45)

        for i in range(0, len(InSingleAgent['ProxyAgents'])):

            direction = InSingleAgent['Position'] - InSingleAgent['ProxyAgents'][i]['Position']
            distance = Utility.getVectorMagnitude(direction)
            radius = (InSingleAgent['Radius'] + (0.45 + InSingleAgent['ProxyAgents'][i]['Radius'])) + personalSpace
            # radius = (0.45 + InSingleAgent['Radius']) + InSingleAgent['ProxyAgents'][i]['Radius']

            if distance < radius:
                strength = InSingleAgent['MaxAcceleration'] * (radius - distance) / radius
                direction = Utility.getNormalisedVector(direction)

                OutVelocity += (direction * strength)

    return OutVelocity


def agentAvoidance(InSingleAgent):
    OutVelocity = np.array([0, 0], dtype='float')

    for i in range(0, len(InSingleAgent['ProxyAgents'])):

        tempProxyAgent = InSingleAgent['ProxyAgents'][i]
        timeToCollision = Utility.getCollisionTimeOfTwoObject(InSingleAgent['Position'],
                                                              InSingleAgent['Velocity'],
                                                              tempProxyAgent['Position'],
                                                              tempProxyAgent['Velocity'])

        distanceWithTime = Utility.getDistanceBetweenTwoObjectWithTime(InSingleAgent['Position'],
                                                                       InSingleAgent['Velocity'],
                                                                       tempProxyAgent['Position'],
                                                                       tempProxyAgent['Velocity'],
                                                                       timeToCollision)

        # if (distance < (agent.Radius + temp.Radius) & & time_to_collision > 0)
        if distanceWithTime < InSingleAgent['Radius'] + tempProxyAgent['Radius'] and timeToCollision > 0:
            directionWithTime = Utility.getDirectionBetweenTwoObjectWithTime(InSingleAgent['Position'],
                                                                             InSingleAgent['Velocity'],
                                                                             tempProxyAgent['Position'],
                                                                             tempProxyAgent['Velocity'],
                                                                             timeToCollision)
            distanceToCollision = Utility.getVectorMagnitude(InSingleAgent['Velocity'] * timeToCollision)
            # force = distanceToCollision + (distanceWithTime - InSingleAgent['Velocity'] * timeToCollision)
            force = InSingleAgent['MaxAcceleration'] / (distanceToCollision +
                                                        (distanceWithTime -
                                                         InSingleAgent['Velocity'] *
                                                         timeToCollision))

            OutVelocity += (directionWithTime * force)

    return OutVelocity


def pathFollow(InSingleAgent):
    totalNoOfSegment = InSingleAgent['Path'].shape[0] - 1

    # -- return 0 Velocity and OutSingleAgent if Segment is below 0 i.e agent finished the path -- #
    if InSingleAgent['SegmentNumber'] < 0 or InSingleAgent['SegmentNumber'] > totalNoOfSegment:
        return 0, InSingleAgent

    OutSingleAgent = InSingleAgent.copy()
    pathRadius = 1.5

    direction = OutSingleAgent['Path'][OutSingleAgent['SegmentNumber']] - OutSingleAgent['Position']
    distance = Utility.getVectorMagnitude(direction)

    if distance < pathRadius:
        OutSingleAgent['SegmentNumber'] += 1

        if OutSingleAgent['SegmentNumber'] > totalNoOfSegment:
            OutSingleAgent['SegmentNumber'] = -10
            return 0, OutSingleAgent
        else:
            OutSingleAgent['CurrentEndLocation'] = OutSingleAgent['Path'][OutSingleAgent['SegmentNumber']]

    OutVelocity = seekORFlee(OutSingleAgent)

    return OutVelocity, OutSingleAgent


def objectAvoidance(InSingleAgent):
    OutVelocity = np.array([0, 0], dtype='float')

    for i in range(0, len(InSingleAgent['ProxyObject'])):
        direction = InSingleAgent['Position'] - InSingleAgent['ProxyObject'][i]['Position']
        distance = Utility.getVectorMagnitude(direction)
        radius = (0.45 + InSingleAgent['Radius']) + InSingleAgent['ProxyObject'][i]['Radius']

        if distance < radius:
            strength = InSingleAgent['MaxAcceleration'] * (radius - distance) / radius
            direction = Utility.getNormalisedVector(direction)
            OutVelocity += (direction * strength)

    return OutVelocity


def lookWhereYourGoing(InSingleAgent):
    OutSingleAgent = InSingleAgent.copy()
    OutRotation = np.array([0], dtype='float')

    distance = Utility.getVectorMagnitude(OutSingleAgent['Velocity'])
    if distance > 4:
        targetOrientation = np.rad2deg(
            Utility.getAtan2(InX=OutSingleAgent['Velocity'][0], InY=OutSingleAgent['Velocity'][1]))

        OutSingleAgent, OutRotation = alignToTargetOrientation(OutSingleAgent, targetOrientation)

    return OutSingleAgent, OutRotation


def seekORFlee(InSingleAgent):
    OutVelocity = InSingleAgent['CurrentEndLocation'] - InSingleAgent['Position']
    OutVelocity = Utility.getNormalisedVector(OutVelocity) * InSingleAgent['MaxAcceleration']

    return OutVelocity


def alignToTargetOrientation(InSingleAgent, InTargetOrientation):
    OutSingleAgent = InSingleAgent.copy()
    targetRadius = 1.0
    slowRadius = 5.0
    timeToTarget = 2.0
    targetRotation = 0.0

    OutSingleAgent['Rotation'] = InTargetOrientation - OutSingleAgent['Orientation']
    OutSingleAgent['Rotation'] = Utility.getWrapTo360(OutSingleAgent['Rotation'])
    rotSize = np.abs(OutSingleAgent['Rotation'])

    if rotSize > targetRadius:
        targetRotation = OutSingleAgent['MaxRotation'] * rotSize / slowRadius

    targetRotation = targetRotation * OutSingleAgent['Rotation'] / rotSize
    OutRotation = targetRotation - OutSingleAgent['Rotation']
    OutRotation = OutRotation / timeToTarget

    if np.abs(OutRotation) > OutSingleAgent['MaxAngularAcceleration']:
        OutRotation = OutRotation / np.abs(OutRotation)
        OutRotation = OutRotation * OutSingleAgent['MaxAngularAcceleration']

    return OutSingleAgent, OutRotation



def updateKinematicsOfAgentWithSteeringInfo(InSingleAgent, InSteering, InSimulationSettings):
    OutSingleAgent = InSingleAgent.copy()
    timeRate = InSimulationSettings.getTimeRate()
    mapUnitSize = InSimulationSettings.getMapUnitSize()

    # -- Update Position and Orientation --#
    OutSingleAgent['Position'] += OutSingleAgent['Velocity'] * timeRate

    OutSingleAgent['Orientation'] += OutSingleAgent['Rotation'] * timeRate
    OutSingleAgent['Orientation'] = Utility.getWrapTo360(OutSingleAgent['Orientation'])

    # -- Update Velocity and Rotation -- #
    OutSingleAgent['Velocity'] += InSteering['Velocity'] * timeRate
    OutSingleAgent['Orientation'] += InSteering['Rotation'] * timeRate
    OutSingleAgent['Orientation'] = Utility.getWrapTo360(OutSingleAgent['Orientation'])

    # -- make sure agent does not accelerate over the max speed limit --#
    if Utility.getVectorMagnitude(OutSingleAgent['Velocity']) > OutSingleAgent['MaxSpeed']:
        OutSingleAgent['Velocity'] = Utility.getNormalisedVector(OutSingleAgent['Velocity'])
        OutSingleAgent['Velocity'] *= OutSingleAgent['MaxSpeed']


    # -- Scale the velocity relative to the unit length of each map segment -- #
    OutSingleAgent['Velocity'] *= (1 / mapUnitSize)

    return OutSingleAgent



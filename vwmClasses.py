# Classes used by stimulusSetup to build a collection of trials with
# counterbalanced attributes. Includes structure for each rectangle (VWMObj),
# structure for each trial (VWMTrial) and member functions. 

import numpy as np

# Targets and distractors sets
TargetSets      = np.array([2,4])
DistractorSets  = np.array([0,2,4])

# number of conditions dependent on # of targets and distractors
nConds = TargetSets.size*DistractorSets.size

######### Assign Condition Names ###############
conds               = {}
nTotalObjsPerCond   = {}
nTargetsInCond      = {}
nDistractorsInCond  = {}
cnt = 0;
for ts in range(TargetSets.size):
    for ds in range(DistractorSets.size):
        conds[cnt]              = 'T' + str(TargetSets[ts]) + 'D' + str(DistractorSets[ds])
        nTargetsInCond[cnt]     = TargetSets[ts]
        nDistractorsInCond[cnt] = DistractorSets[ds]
        nTotalObjsPerCond[cnt]  = int(nTargetsInCond[cnt]+nDistractorsInCond[cnt])
        cnt += 1

###  Visual Working Memory Object Class
class VWMObj():
    """ Trial objects. """
    size = (.5, 1.5)
    def __init__(self, objType, objID , centerLoc = (0,0), orientation = 0):
    # center location tuple: (radii in deg from center of screen, theta from median)
        if objType=="target":
            self.color      = 'firebrick'
        elif objType=="distractor":
            self.color      = 'mediumblue'
        else:
            self.color      = 'black'
        # pixel location of the object's center
        self.centerLoc      = centerLoc
        self.orientation    = orientation
        # the object's number relative to the # of objects per trial
        self.objID          = objID
        # types: target or distrator
        self.objType        = objType
        # hemifield: left or right
        self.hemifield      = 'none'

    def getLoc(self):
        return self.centerLoc

    def getOrientation(self):
        return self.orientation

    def getObjID(self):
        return self.objID

    def getColor(self):
        return self.color

    def objType(self):
        return self.objType

    def getHemifield(self):
        return self.hemifield

    def setOrientation(self, o):
        self.orientation = o

    def setLoc(self, p):
        self.centerLoc = p
        if self.centerLoc[0] < 0:
            self.hemifield = 'left'
        else:
            self.hemifield = 'right'

###  Visual Working Memory Trial Class
class VWMTrial():
    """trial properties for VWM alpha tACS """
    def __init__(self, trialID, condNum, ChangeCond, ChangeTargID):
        # trial ID number relative to the total number of trials
        self.trialID        = trialID
        # condition number, 1 thru 6 inclusive
        self.condNum        = condNum
        # whole field condition is identical to the hemifield-specific condition
        self.HFCond         = condNum
        # total number of targets
        self.nTargets       = nTargetsInCond[condNum-1]
        self.nDistractors   = nDistractorsInCond[condNum-1]
        # total number of distractors
        self.nTotalItems    = self.nDistractors + self.nTargets
        # Change Conditions: 0 = Left Change, 1 = Right Change, 3 = No Change
        self.ChangeCond     = ChangeCond
        if ChangeCond==3: # no change
            self.ChangeTrial = 0
            self.TargetChangeID = -1
        else:
            self.ChangeTrial = 1
            self.TargetChangeID = ChangeTargID
        # Array of trial objects (VWMObj class)
        self.Objects        = []
        # Array with targets marked with a 1 and distractors marked with a 0
        self.ObjTarg        = np.zeros(self.nTotalItems,np.int)
        # rotation used to mark change trials in stimulusSetup
        self.rotation       = 0
        cnt = 0
        # assign targets and distractors to the Objects array
        for obj in range(self.nTargets):
            self.Objects.append(VWMObj('target',cnt))
            self.ObjTarg[cnt]=1
            cnt+=1
        for obj in range(self.nDistractors):
            self.Objects.append(VWMObj('distractor',cnt))
            self.ObjTarg[cnt]=0
            cnt+=1

    # returns the number of objects (can define the type) on the left hemifield
    def leftObjectCount(self, objType='all'):
        leftCount = 0
        for obj in self.Objects:
            if objType == 'all' and obj.getHemifield() == 'left':
                leftCount += 1
            elif obj.objType == objType and obj.getHemifield() == 'left':
                leftCount += 1
        return leftCount

    # returns the number of objects (can define the type) on the right hemifield.
    def rightObjectCount(self, objType='all'):
        rightCount = 0
        for obj in self.Objects:
            if objType == 'all' and obj.getHemifield() == 'right':
                rightCount += 1
            elif obj.objType == objType and obj.getHemifield() == 'right':
                rightCount += 1
        return rightCount

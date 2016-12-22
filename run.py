# Running this file runs the whole behavioral task. The pickle file required to
# present the task is loaded by entering the subj and run numbers in terminal.
# Running this task in terminal is done as follows:
# python ./run.py %subj %run
# where run and subj are the actual subject and run numbers.
#
# stimulusSetup must be run in advance with the same subj and run numbers to
# create the pickle file.

# imports for run
import sys
# prevents bytecode file clutter in the source folder
sys.dont_write_bytecode = True
from presentationSetup import oneTrial, VWMTrials, win
from psychopy import core

# initialize nTrials constant based on VWMTrials data structure
nTrials = len(VWMTrials)

# Runs all nTrials
for i in range(nTrials):
    oneTrial(i)

# close window and quit psychopy
win.close()
core.quit()

# This file performs the first step of data analysis, performing calculations
# on a .csv data file output by the psychopy package. Pashler's K, d prime,
# hit rates, RTs and more are returned in a dictionary by extractPerformance to
# be utilized by pandas or another python data analysis library.

# imports
from __future__ import division
import pandas as pd
from collections import OrderedDict
from scipy.stats import norm
Z = norm.ppf
import os
from os.path import expanduser
import re

# constant number of trials per change cond
nTrialsPerChangeCond = 16

# counts number of trials in each run matching the inputted conditions
def condCounter(df, response, changeType, cond):
    count = float(len(df[response & changeType & cond]))
    return count

# calculates K pased on Pashler equation: K = S * ((H - F) / (1 - F))
def pashlerK(hits, misses, falarms, crejects, cond):
    S = cond[1]
    hitRate = hits/(hits+misses)
    faRate = falarms/(falarms+crejects)
    K = int(S) * ((hitRate - faRate) / (1 - faRate))
    return {'K': K, 'hitRate': hitRate, 'faRate': faRate}

# calculates d's using Z from scipy.stats.norm.ppf()
def dprime(hits, misses, falarms, crejects):
    faRate = 0
    hitRate = 0
    #correct for FA values of 0
    if falarms == 0:
        faRate = 1 / (2 * crejects)
    elif crejects ==0:
        faRate = 1 - (1 / (2*falarms))
    else:
        faRate = falarms / (falarms + crejects)
    if misses == 0:
        hitRate = 1 - (1 / (2 * hits))
    elif hits ==0:
        hitRate = 1 / (2 * misses)
    else:
        hitRate = hits/(hits+misses);

    # calculate dprime using Z (ppf function in scipy.norm)
    dprime = Z(hitRate) - Z(faRate)

    # calculate critereon using Z
    critereon = -.5 * (Z(hitRate) + Z(faRate))
    return {'dprime': dprime, 'critereon': critereon}

# calculates RTs for each condition by finding median response time
def rt(df, resps, change, cond):
    row = df[resps & change & cond]
    rt = row['RT'].median()
    return rt

# generates a dictionary containing all relevant data from a test run .csv file
# uses regex to find the data filename given subj, run and testRound numbers.
def extractPerformance(subj, run, testRound):
    ### read in csv file ###
    # establish file data directory
    homeDirectory = expanduser("~")
    dataDirectory = homeDirectory + os.sep + 'Google Drive/tACS_VWM_ALPHA/data/' + testRound + '/'

    # find file in directory with regex
    saveDirectory = dataDirectory + 's' + str(subj) + os.sep + 'runData/'
    directoryFiles = os.listdir(saveDirectory)
    csv = ''
    for file in directoryFiles:
        match = re.match('run' + str(run) + '.*', file, re.M|re.I)
        if match != None:
            csv = saveDirectory + match.group()
    df = pd.read_csv(csv)

    # only conduct assertions if 384 trials
    assertionsPossible = len(df.index) == 384

    # initialize conditions
    resps = df['Response'] == 1
    rejects = df['Response'] == 2
    changes = df['ChangeTrial'] == 1
    noChanges = df['ChangeTrial'] == 0
    lChanges = df['ChangeCond'] == 1
    lNoChanges = df['ChangeCond'] != 1
    rChanges = df['ChangeCond'] == 2
    rNoChanges = df['ChangeCond'] != 2
    t1d0 = df['Cond'] == 1
    t1d1 = df['Cond'] == 2
    t1d2 = df['Cond'] == 3
    t2d0 = df['Cond'] == 4
    t2d1 = df['Cond'] == 5
    t2d2 = df['Cond'] == 6

    # initialize dictionaries
    lHits = OrderedDict()
    lMisses = OrderedDict()
    lFAs = OrderedDict()
    lCRs = OrderedDict()
    rHits = OrderedDict()
    rMisses = OrderedDict()
    rFAs = OrderedDict()
    rCRs = OrderedDict()
    wHits = OrderedDict()
    wMisses = OrderedDict()
    wFAs = OrderedDict()
    wCRs = OrderedDict()
    lHitRTs = OrderedDict()
    rHitRTs = OrderedDict()
    wHitRTs = OrderedDict()
    lFaRTs = OrderedDict()
    rFaRTs = OrderedDict()
    wFaRTs = OrderedDict()
    lKs = OrderedDict()
    rKs = OrderedDict()
    wKs = OrderedDict()
    lHRs = OrderedDict()
    rHRs = OrderedDict()
    wHRs = OrderedDict()
    lfaRates = OrderedDict()
    rfaRates = OrderedDict()
    wfaRates = OrderedDict()
    ldPs = OrderedDict()
    rdPs = OrderedDict()
    wdPs = OrderedDict()
    lCrits = OrderedDict()
    rCrits = OrderedDict()
    wCrits = OrderedDict()
    HFconds = OrderedDict([('t1d0', t1d0), ('t1d1', t1d1), ('t1d2', t1d2),
    ('t2d0', t2d0), ('t2d1', t2d1), ('t2d2', t2d2)])

    # store rate values
    # CR/crit = Correct Rejection, FA/fa = False Alarm, dP = d', HR = Hit Rate
    # K = Memory capacity (calculated for each condition using Pashler equation)
    # hitRT = Response time for trials where the subj responded correctly
    # faRT = Response time for trials where the subj false alarmed
    for key in HFconds:
        lHits[key] = condCounter(df, resps, lChanges, HFconds[key])
        lMisses[key] = condCounter(df, rejects, lChanges, HFconds[key])
        lFAs[key] = condCounter(df, resps, noChanges, HFconds[key])
        lCRs[key] = condCounter(df, rejects, noChanges, HFconds[key])

        rHits[key] = condCounter(df, resps, rChanges, HFconds[key])
        rMisses[key] = condCounter(df, rejects, rChanges, HFconds[key])
        rFAs[key] = condCounter(df, resps, noChanges, HFconds[key])
        rCRs[key] = condCounter(df, rejects, noChanges, HFconds[key])

        # HFconds used b/c ChangeCond #s are equivalent to WFconds
        wHits[key] = condCounter(df, resps, changes, HFconds[key])
        wMisses[key] = condCounter(df, rejects, changes, HFconds[key])
        wFAs[key] = condCounter(df, resps, noChanges, HFconds[key])
        wCRs[key] = condCounter(df, rejects, noChanges, HFconds[key])

        if (assertionsPossible):
            assert (lHits[key] + lMisses[key] == nTrialsPerChangeCond), 'lChange counterbalancing failed: ' + str(lHits[key] + lMisses[key]) + ': ' + str(subj) + ',' + str(run) + 'Cond: ' + key
            assert (lFAs[key] + lCRs[key] == nTrialsPerChangeCond * 3), 'lNoChange counterbalancing failed: ' + str(lFAs[key] + lCRs[key])
            assert (rHits[key] + rMisses[key] == nTrialsPerChangeCond), 'rChange counterbalancing failed: ' + str(rHits[key] + rMisses[key])
            assert (rFAs[key] + rCRs[key] == nTrialsPerChangeCond * 3), 'rNoChange counterbalancing failed: ' + str(rFAs[key] + rCRs[key])
            assert (wHits[key] + wMisses[key] == nTrialsPerChangeCond * 2), 'wChange counterbalancing failed: ' + str(wHits[key] + wMisses[key])
            assert (wFAs[key] + wCRs[key] == nTrialsPerChangeCond * 2), 'wNoChange counterbalancing failed: ' + str(wFAs[key] + wCRs[key])

        lHitRTs[key] = rt(df, resps, lChanges, HFconds[key])
        rHitRTs[key] = rt(df, resps, rChanges, HFconds[key])
        wHitRTs[key] = rt(df, resps, changes, HFconds[key])
        lFaRTs[key] = rt(df, resps, lNoChanges, HFconds[key])
        rFaRTs[key] = rt(df, resps, rNoChanges, HFconds[key])
        wFaRTs[key] = rt(df, resps, noChanges, HFconds[key])

        lPashler = pashlerK(lHits[key],lMisses[key],lFAs[key], lCRs[key], key)
        rPashler = pashlerK(rHits[key],rMisses[key],rFAs[key], rCRs[key], key)
        wPashler = pashlerK(wHits[key],wMisses[key],wFAs[key], wCRs[key], key)
        lHRs[key] = lPashler['hitRate']
        rHRs[key] = rPashler['hitRate']
        wHRs[key] = wPashler['hitRate']
        lKs[key] = lPashler['K']
        rKs[key] = rPashler['K']
        wKs[key] = wPashler['K']
        lfaRates[key] = lPashler['faRate']
        rfaRates[key] = rPashler['faRate']
        wfaRates[key] = wPashler['faRate']
        ldPrime = dprime(lHits[key],lMisses[key],lFAs[key], lCRs[key])
        rdPrime = dprime(rHits[key],rMisses[key],rFAs[key], rCRs[key])
        wdPrime = dprime(wHits[key],wMisses[key],wFAs[key], wCRs[key])
        ldPs[key] = ldPrime['dprime']
        rdPs[key] = rdPrime['dprime']
        wdPs[key] = wdPrime['dprime']
        lCrits[key] = ldPrime['critereon']
        rCrits[key] = rdPrime['critereon']
        wCrits[key] = wdPrime['critereon']

    return {'lHits': lHits, 'rHits': rHits, 'lMisses': lMisses, 'rMisses': rMisses,
            'lFAs': lFAs, 'rFAs': rFAs, 'lCRs': lCRs, 'rCRs': rCRs, 'lHitRTs': lHitRTs,
            'rHitRTs': rHitRTs, 'lFaRTs': lFaRTs, 'rFaRTs': rFaRTs, 'lHRs': lHRs,
            'rHRs': rHRs, 'lKs': lKs, 'rKs': rKs, 'ldPs': ldPs, 'rdPs': rdPs,
            'wHRs': wHRs, 'wKs': wKs, 'wHitRTs': wHitRTs, 'wFaRTs': wFaRTs, 'wdPs': wdPs,
            'lfaRates': lfaRates, 'rfaRates': rfaRates, 'wfaRates': wfaRates,
            'lCrits': lCrits, 'rCrits': rCrits, 'wCrits': wCrits}

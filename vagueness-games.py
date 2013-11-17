import sys
import copy
import csv

import numpy as np
from numpy import random as random

from scipy import stats as stats

import matplotlib.pyplot as plt
import itertools

def plotStrategies(block=False):
    plt.clf()

    plt.subplot(4,2,1)
    plt.plot(PerceptualSpace, Priors)
    plt.ylim(ymin=0)
    plt.title('Priors')

    plt.subplot(4,4,3)
    plt.imshow(Utility, origin='lower', interpolation='none')
    plt.title('Utility')
    plt.subplot(4,4,4)
    plt.imshow(Confusion, origin='lower', interpolation='none')
    plt.title('Confusion')

    plt.subplot(4,2,3)
    for m in xrange(NMessages):
        plt.plot(PerceptualSpace, Speaker[:,m], label='$m_'+str(m)+'$')
    plt.ylim(-0.1,1.1)
    plt.legend(loc='lower left')
    plt.title('Speaker strategy')

    plt.subplot(4,2,4)
    for m in xrange(NMessages):
        plt.plot(PerceptualSpace, Hearer[m,:], label='$m_'+str(m)+'$')
    plt.ylim(ymin=0)
    plt.legend(loc='lower left')
    plt.title('Hearer strategy')

    plt.subplot(4,1,3)
    plt.plot(ExpectedUtilityHistory)
    plt.ylim(ymin=0)
    plt.title('Expected utility')

    plt.subplot(4,2,7)
    plt.plot(BasicUncertaintySpeakerHistory, label='basic')
    plt.plot(LucaTerminiUncertaintySpeakerHistory, label='LT')
    plt.plot(FrankeUncertaintySpeakerHistory, label='MF-2')
    plt.plot(CorreiaUncertaintySpeakerHistory, label='JPC')
    plt.plot(EntropyMixedSpeakerHistory, label='E')
    plt.ylim(ymin=-0.1, ymax=1.1)
    plt.legend(loc='upper right')
    plt.title('Uncertainty metrics speaker')

    plt.subplot(4,2,8)
    plt.plot(BasicUncertaintyHearerHistory, label='basic')
    plt.plot(LucaTerminiUncertaintyHearerHistory, label='LT')
    plt.plot(FrankeUncertaintyHearerHistory, label='MF-2')
    plt.plot(CorreiaUncertaintyHearerHistory, label='JPC')
    plt.plot(EntropyMixedHearerHistory, label='E')
    plt.ylim(ymin=-0.1)#, ymax=1.1)
    plt.legend(loc='upper right')
    plt.title('Uncertainty metrics hearer')

    plt.show(block=block)
    plt.pause(0.01)

def normalize(Vector):
    return Vector / np.max(Vector)

def makePDF(Vector):
    if np.sum(Vector) == 0:
        Vector = np.ones(np.shape(Vector))
    return Vector / np.sum(Vector)

def makePDFPerRow(Matrix):
    return np.array([ makePDF(Row) for Row in Matrix ])
    
def ShannonEntropy(x):
    if x == 0 or x == 1:
        return 0
    else:
        return -x * np.log10(x) - (1 - x) * np.log10(1 - x)

def BasicUncertainty(Strategy):
    return np.mean([1 - abs(Strategy[c,a] - 0.5) / 0.5
                    for c in xrange(Strategy.shape[0])
                    for a in xrange(Strategy.shape[1])])

def LucaTerminiUncertainty(Strategy):
    return np.mean([(1.0/Strategy.shape[1]) * np.sum(ShannonEntropy(Strategy[c,a])
                           for a in xrange(Strategy.shape[1]))
                    for c in xrange(Strategy.shape[0])])
    
def FrankeUncertainty(Strategy):
    return np.mean([np.min([-np.log10(Strategy[c,a]) if Strategy[c,a] != 0 else 0
                            for a in xrange(Strategy.shape[1])])
                    for c in xrange(Strategy.shape[0])])

def CorreiaUncertainty(Strategy):
    return np.mean([1 - (1.0/np.log(Strategy.shape[1])) * np.sum(np.log(Strategy.shape[1] * Strategy[c,a]) * Strategy[c,a] if Strategy[c,a] != 0 else 0
                             for a in xrange(Strategy.shape[1]))
                    for c in xrange(Strategy.shape[0])])

def ExpectedUtility(Speaker, Hearer, Utility):
    return np.sum(Speaker[t1,m] * Hearer[m,t2] * Utility[t1,t2]
                  for t1 in xrange(Speaker.shape[0])
                  for m in xrange(Speaker.shape[1])
                  for t2 in xrange(Hearer.shape[1]))

def ToMixedStrategy(Strategy):
    return [ np.prod([Strategy[c, s[c]] for c in xrange(Strategy.shape[0])])
            for s in itertools.product(xrange(Strategy.shape[1]), repeat=Strategy.shape[0]) ]

def NormalizedEntropy(MixedStrategy):
    return - sum(x * np.log2(x) if x != 0 else 0 for x in MixedStrategy) / np.log2(len(MixedStrategy))

## Settings

NStates = 10
PriorDistributionType = 'uniform'

NMessages = 2

Dynamics = 'replicator dynamics'
Impairment = 0.1

Tolerance = 0.2

## Batch mode

BatchMode = False

if BatchMode:
    if len(sys.argv) < 3:
        print "Usage: python", sys.argv[0], "<number of states> <acuity>"
        sys.exit(1)
    else:
        NStates = int(sys.argv[1])
        Impairment = float(sys.argv[2])

## Initialization

PerceptualSpace = np.linspace(0, 1, NStates, endpoint=False)

if PriorDistributionType == 'uniform':
    Priors = stats.uniform.pdf(PerceptualSpace, loc=0, scale=NStates)
elif PriorDistributionType == 'normal':
    Priors = stats.norm.pdf(PerceptualSpace, loc=0.5, scale=0.1)

Distance = np.array([ [ abs(x - y) for y in PerceptualSpace ] for x in PerceptualSpace ])

Utility = np.exp( - (Distance ** 2 / Tolerance ** 2))

Confusion = np.exp( - (Distance ** 2 / Impairment ** 2)) if Impairment != 0 else np.identity(NStates)

Speaker = random.dirichlet([1]*NMessages,NStates)
Hearer = random.dirichlet([1]*NStates,NMessages)

ExpectedUtilityHistory = []

# Uncertainty metrics
BasicUncertaintySpeakerHistory = []
LucaTerminiUncertaintySpeakerHistory = []
FrankeUncertaintySpeakerHistory = []
CorreiaUncertaintySpeakerHistory = []
EntropyMixedSpeakerHistory = []

BasicUncertaintyHearerHistory = []
LucaTerminiUncertaintyHearerHistory = []
FrankeUncertaintyHearerHistory = []
CorreiaUncertaintyHearerHistory = []
EntropyMixedHearerHistory = []

i=0
converged = False
while not converged:
    i+=1
    
    if not BatchMode: plotStrategies()

    SpeakerBefore, HearerBefore = copy.deepcopy(Speaker), copy.deepcopy(Hearer)

    ExpectedUtilityHistory.append(ExpectedUtility(Speaker, Hearer, Utility))

    # Uncertainty metrics
    
    BasicUncertaintySpeakerHistory.append(BasicUncertainty(Speaker))
    LucaTerminiUncertaintySpeakerHistory.append(LucaTerminiUncertainty(Speaker))
    FrankeUncertaintySpeakerHistory.append(FrankeUncertainty(Speaker))
    CorreiaUncertaintySpeakerHistory.append(CorreiaUncertainty(Speaker))

    BasicUncertaintyHearerHistory.append(BasicUncertainty(Hearer))
    LucaTerminiUncertaintyHearerHistory.append(LucaTerminiUncertainty(Hearer))
    FrankeUncertaintyHearerHistory.append(FrankeUncertainty(Hearer))
    CorreiaUncertaintyHearerHistory.append(CorreiaUncertainty(Hearer))

    MixedSpeaker = ToMixedStrategy(Speaker)
    EntropyMixedSpeakerHistory.append(NormalizedEntropy(MixedSpeaker))

    MixedHearer = ToMixedStrategy(Hearer)
    EntropyMixedHearerHistory.append(NormalizedEntropy(MixedHearer))

    ## Dynamics
    
    ## Speaker strategy
    
    UtilitySpeaker = np.array([ [ np.dot(Hearer[m], Utility[t]) for m in xrange(NMessages) ] for t in xrange(NStates) ])

    for t in xrange(NStates):
        for m in xrange(NMessages):
            if Dynamics == 'replicator dynamics':
                Speaker[t,m] = Speaker[t,m] * UtilitySpeaker[t,m] * NMessages / sum(UtilitySpeaker[t])
            elif Dynamics == 'best response':
                Speaker[t,m] = 1 if UtilitySpeaker[t,m] == max(UtilitySpeaker[t]) else 0

    Speaker = np.dot(Confusion, Speaker)

    Speaker = makePDFPerRow(Speaker)
    
    ## Hearer strategy
    
    UtilityHearer = np.array([ [ np.dot(Priors * Speaker[:,m], Utility[t]) for t in xrange(NStates) ] for m in xrange(NMessages) ])

    for m in xrange(NMessages):
        for t in xrange(NStates):
            if Dynamics == 'replicator dynamics':
                Hearer[m,t] = Hearer[m,t] * UtilityHearer[m,t] * NStates / sum(UtilityHearer[m])
            elif Dynamics == 'best response':
                Hearer[m,t] = 1 if UtilityHearer[m,t] == max(UtilityHearer[m]) else 0

    Hearer = np.dot(Hearer, np.transpose(Confusion))

    Hearer = makePDFPerRow(Hearer)

    if np.sum(abs(Speaker - SpeakerBefore)) < 0.01 and np.sum(abs(Hearer - HearerBefore)) < 0.01:
        converged = True
        if not BatchMode: print 'Language converged!'

if not BatchMode: plotStrategies(block=True)

csv.writer(sys.stdout).writerow([NStates, PriorDistributionType, NMessages, Impairment, Tolerance, Dynamics, \
    BasicUncertainty(Speaker), LucaTerminiUncertainty(Speaker), FrankeUncertainty(Speaker), CorreiaUncertainty(Speaker), NormalizedEntropy(ToMixedStrategy(Speaker)), \
    BasicUncertainty(Hearer), LucaTerminiUncertainty(Hearer), FrankeUncertainty(Hearer), CorreiaUncertainty(Hearer), NormalizedEntropy(ToMixedStrategy(Hearer)), \
    ExpectedUtility(Speaker, Hearer, Utility), i])

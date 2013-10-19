import sys
import copy

import numpy as np
from numpy import random as random

from scipy import stats as stats

import matplotlib.pyplot as plt

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
    plt.ylim(ymin=-0.1, ymax=1.1)
    plt.legend(loc='upper right')
    plt.title('Uncertainty metrics speaker')

    plt.subplot(4,2,8)
    plt.plot(BasicUncertaintyHearerHistory, label='basic')
    plt.plot(LucaTerminiUncertaintyHearerHistory, label='LT')
    plt.plot(FrankeUncertaintyHearerHistory, label='MF-2')
    plt.plot(CorreiaUncertaintyHearerHistory, label='JPC')
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
    
## Settings

NStates = 50
PriorDistributionType = 'uniform'

NMessages = 2

Dynamics = 'replicator dynamics'
LimitedPerception = True
Acuity = 10

## Batch mode

BatchMode = False

if BatchMode:
    if len(sys.argv) < 3:
        print "Usage: python", sys.argv[0], "<number of states> <acuity>"
        sys.exit(1)
    else:
        NStates = int(sys.argv[1])
        Acuity = float(sys.argv[2])

## Initialization

PerceptualSpace = np.linspace(0, 1, NStates, endpoint=False)

if PriorDistributionType == 'uniform':
    Priors = stats.uniform.pdf(PerceptualSpace, loc=0, scale=NStates)
elif PriorDistributionType == 'normal':
    Priors = stats.norm.pdf(PerceptualSpace, loc=0.5, scale=0.1)

Distance = np.array([ [ abs(x - y) for y in PerceptualSpace ] for x in PerceptualSpace ])
Similarity = np.exp( - (Distance ** 2 / (1.0/Acuity) ** 2))

Utility = Similarity

Confusion = Similarity

Speaker = makePDFPerRow(random.random((NStates,NMessages)))
Hearer = makePDFPerRow(random.random((NMessages,NStates)))

ExpectedUtilityHistory = []

# Uncertainty metrics
BasicUncertaintySpeakerHistory = []
LucaTerminiUncertaintySpeakerHistory = []
FrankeUncertaintySpeakerHistory = []
CorreiaUncertaintySpeakerHistory = []

BasicUncertaintyHearerHistory = []
LucaTerminiUncertaintyHearerHistory = []
FrankeUncertaintyHearerHistory = []
CorreiaUncertaintyHearerHistory = []

converged = False
while not converged:
    
    if not BatchMode: plotStrategies()

    SpeakerBefore, HearerBefore = copy.deepcopy(Speaker), copy.deepcopy(Hearer)

    ExpectedUtility = np.sum(Speaker[t1,m]*Hearer[m,t2]*Utility[t1,t2]
                             for t1 in xrange(NStates)
                             for m in xrange(NMessages)
                             for t2 in xrange(NStates))
    ExpectedUtilityHistory.append(np.sum(ExpectedUtility))

    # Uncertainty metrics
    
    BasicUncertaintySpeakerHistory.append(BasicUncertainty(Speaker))
    LucaTerminiUncertaintySpeakerHistory.append(LucaTerminiUncertainty(Speaker))
    FrankeUncertaintySpeakerHistory.append(FrankeUncertainty(Speaker))
    CorreiaUncertaintySpeakerHistory.append(CorreiaUncertainty(Speaker))

    print "Speaker:", BasicUncertainty(Speaker), LucaTerminiUncertainty(Speaker), FrankeUncertainty(Speaker), CorreiaUncertainty(Speaker)
    
    BasicUncertaintyHearerHistory.append(BasicUncertainty(Hearer))
    LucaTerminiUncertaintyHearerHistory.append(LucaTerminiUncertainty(Hearer))
    FrankeUncertaintyHearerHistory.append(FrankeUncertainty(Hearer))
    CorreiaUncertaintyHearerHistory.append(CorreiaUncertainty(Hearer))

    print "Hearer:", BasicUncertainty(Hearer), LucaTerminiUncertainty(Hearer), FrankeUncertainty(Hearer), CorreiaUncertainty(Hearer)
    
    ## Dynamics
    
    ## Speaker strategy
    
    UtilitySpeaker = np.array([ [ np.dot(Hearer[m], Utility[t]) for m in xrange(NMessages) ] for t in xrange(NStates) ])

    for t in xrange(NStates):
        for m in xrange(NMessages):
            if Dynamics == 'replicator dynamics':
                Speaker[t,m] = Speaker[t,m] * UtilitySpeaker[t,m] * NMessages / sum(UtilitySpeaker[t])
            elif Dynamics == 'best response':
                Speaker[t,m] = 1 if UtilitySpeaker[t,m] == max(UtilitySpeaker[t]) else 0

    if LimitedPerception:
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

    if LimitedPerception:
        Hearer = np.dot(Hearer, np.transpose(Confusion))

    Hearer = makePDFPerRow(Hearer)

    if np.sum(abs(Speaker - SpeakerBefore)) < 0.01 and np.sum(abs(Hearer - HearerBefore)) < 0.01:
        converged = True
        if not BatchMode: print 'Language converged!'

if not BatchMode: plotStrategies(block=True)
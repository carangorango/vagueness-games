import sys
import copy

import numpy as np
from numpy import random as random

from scipy import stats as stats

import matplotlib.pyplot as plt

def plotStrategies(NStates, NMessages, PerceptualSpace, Priors, Utility, Confusion, Speaker, Hearer, block=False, vline=None):
    plt.clf()

    plt.subplot(2,2,1)
    plt.plot(PerceptualSpace, Priors)
    plt.ylim(ymin=0)
    plt.title('Priors')

    plt.subplot(2,4,3)
    plt.imshow(Utility, origin='lower', interpolation='none')
    plt.title('Utility')
    plt.subplot(2,4,4)
    plt.imshow(Confusion, origin='lower', interpolation='none')
    plt.title('Confusion')

    plt.subplot(2,2,3)
    for m in xrange(NMessages):
        plt.plot(PerceptualSpace, Speaker[:,m], label='$m_'+str(m)+'$')
    if vline:
        plt.axvline(vline, linestyle='--', color='red')
    plt.ylim(-0.1,1.1)
    plt.legend(loc='lower left')
    plt.title('Speaker strategy')

    plt.subplot(2,2,4)
    for m in xrange(NMessages):
        plt.plot(PerceptualSpace, Hearer[m,:], label='$m_'+str(m)+'$')
    if vline:
        plt.axvline(vline, linestyle='--', color='red')
    plt.ylim(ymin=0)
    plt.legend(loc='lower left')
    plt.title('Hearer strategy')

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
    
## Settings

NStates = 50
PriorDistributionType = 'uniform'

NMessages = 2

Dynamics = 'replicator dynamics'
SoritesProgression = 'sequential'

LimitedPerception = True
Acuity = 10

Rationality = 20

Susceptibility = 0.5

## Batch mode

BatchMode = False

if BatchMode:
    if len(sys.argv) < 4:
        print "Usage: python", sys.argv[0], "<number of states> <acuity> <susceptibility>"
        sys.exit(1)
    else:
        NStates = int(sys.argv[1])
        Acuity = float(sys.argv[2])
        Susceptibility = float(sys.argv[3])

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

converged = False
while not converged:
    
    if not BatchMode: plotStrategies(NStates, NMessages, PerceptualSpace, Priors, Utility, Confusion, Speaker, Hearer)

    SpeakerBefore, HearerBefore = copy.deepcopy(Speaker), copy.deepcopy(Hearer)

    ## Speaker strategy
    
    UtilitySpeaker = np.array([ [ np.dot(Hearer[m], Utility[t]) for m in xrange(NMessages) ] for t in xrange(NStates) ])

    for t in xrange(NStates):
        for m in xrange(NMessages):
            if Dynamics == 'replicator dynamics':
                Speaker[t,m] = Speaker[t,m] * UtilitySpeaker[t,m] * NMessages / sum(UtilitySpeaker[t])
            elif Dynamics == 'best response':
                Speaker[t,m] = 1 if UtilitySpeaker[t,m] == max(UtilitySpeaker[t]) else 0
            elif Dynamics == 'quantal best response':
                Speaker[t,m] = np.exp(Rationality * UtilitySpeaker[t,m]) / sum(np.exp(Rationality * UtilitySpeaker[t]))

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
            elif Dynamics == 'quantal best response':
                Hearer[m,t] = np.exp(Rationality * UtilityHearer[m,t]) / sum(np.exp(Rationality * UtilityHearer[m]))

    if LimitedPerception:
        Hearer = np.dot(Hearer, np.transpose(Confusion))

    Hearer = makePDFPerRow(Hearer)

    if np.sum(abs(Speaker - SpeakerBefore)) < 0.01 and np.sum(abs(Hearer - HearerBefore)) < 0.01:
        converged = True
        if not BatchMode: print 'Language converged!'

MaximalElements = [ np.where(Hearer[m] == Hearer[m].max())[0] for m in xrange(NMessages) ]
Criterion1 = all(len(MaximalElements[m]) == 1 for m in xrange(NMessages))

Prototype = [ np.argmax(Hearer[m]) for m in xrange(NMessages) ]
CriterionX = all(Prototype[m1] != Prototype[m2] if m1 != m2 else True for m1 in xrange(NMessages) for m2 in xrange(NMessages))

# precision issues, otherwise Hearer[m,t1] > Hearer[m,t2]
Criterion2 = all(all(Hearer[m,t1] > Hearer[m,t2] or Hearer[m,t2] - Hearer[m,t1] < 0.01 for t1 in xrange(NStates) for t2 in xrange(NStates) if Similarity[t1,Prototype[m]] > Similarity[t2,Prototype[m]]) for m in xrange(NMessages)) 

Criterion3 = all(all(Speaker[t,m1] > Speaker[t,m2] or Speaker[t,m2] - Speaker[t,m1] < 0.01 for m1 in xrange(NMessages) for m2 in xrange(NMessages) if Similarity[t,Prototype[m1]] > Similarity[t,Prototype[m2]]) for t in xrange(NStates))

if Criterion1 and CriterionX and Criterion2 and Criterion3 and not BatchMode:
    print 'Language is proper vague language'
elif not BatchMode:
    print 'Language is NOT properly vague'

if not BatchMode: plotStrategies(NStates, NMessages, PerceptualSpace, Priors, Utility, Confusion, Speaker, Hearer, block=True)

for n in xrange(0, NStates):
    if SoritesProgression == 'sequential':
        i = n
    elif SoritesProgression == 'random':
        i = random.randint(0, NStates)

    if not BatchMode: print 'State', n, ':', PerceptualSpace[i]

    if not BatchMode: plotStrategies(NStates, NMessages, PerceptualSpace, Priors, Utility, Confusion, Speaker, Hearer, vline=PerceptualSpace[i])

    UtilitySpeaker = np.array([ [ np.dot(Hearer[m], Utility[t]) for m in xrange(NMessages) ] for t in xrange(NStates) ])

    Response = np.zeros((NStates,NMessages))
    for m in xrange(NMessages):
        Response[i,m] = 1 if Speaker[i,m] == max(Speaker[i]) else 0

    if LimitedPerception:
        Response = np.dot(Confusion, Response)

    Speaker = (1 - Susceptibility) * Speaker + Susceptibility * Response
    
    Speaker = makePDFPerRow(Speaker)

    UtilityHearer = np.array([ [ np.dot(Priors * Speaker[:,m], Utility[t]) for t in xrange(NStates) ] for m in xrange(NMessages) ])

    for m in xrange(NMessages):
        for t in xrange(NStates):
            if Dynamics == 'replicator dynamics':
                Hearer[m,t] = Hearer[m,t] * UtilityHearer[m,t] * NStates / sum(UtilityHearer[m])
            elif Dynamics == 'best response':
                Hearer[m,t] = 1 if UtilityHearer[m,t] == max(UtilityHearer[m]) else 0
            elif Dynamics == 'quantal best response':
                Hearer[m,t] = np.exp(Rationality * UtilityHearer[m,t]) / sum(np.exp(Rationality * UtilityHearer[m]))

    if LimitedPerception:
        Hearer = np.dot(Hearer, np.transpose(Confusion))

    Hearer = makePDFPerRow(Hearer)
    
ParadoxReached = any([ all([ Speaker[t,m] == max(Speaker[t]) for t in xrange(NStates) ]) for m in xrange(NMessages) ])

print str(NStates) + ',' + str(Acuity) + ',' + str(Susceptibility) + ',' + str(ParadoxReached)

if not BatchMode: plotStrategies(NStates, NMessages, PerceptualSpace, Priors, Utility, Confusion, Speaker, Hearer, block=True)

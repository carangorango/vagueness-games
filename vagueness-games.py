import sys
import copy
import csv
import math

import numpy as np
from numpy import random as random

from scipy import stats as stats

import matplotlib.pyplot as plt
import itertools

def plotStrategies(block=False):
    plt.clf()

    plt.subplot(3, 2, 1)
    plt.plot(PerceptualSpace, Priors)
    plt.ylim(ymin=0)
    plt.title('Priors')

    plt.subplot(3, 4, 3)
    plt.imshow(Utility, origin='lower', interpolation='none')
    plt.title('Utility')
    plt.subplot(3, 4, 4)
    plt.imshow(Confusion, origin='lower', interpolation='none')
    plt.title('Confusion')

    plt.subplot(3, 2, 3)
    for m in xrange(NMessages):
        plt.plot(PerceptualSpace, Speaker[:, m], label='$m_{' + str(m) + '}$')
    for m in xrange(NMessages):
        plt.plot(PerceptualSpace, SpeakerOptimal[:, m], linestyle='--', color='0.5')
    plt.ylim(-0.1, 1.1)
    plt.legend(loc='lower left')
    plt.title('Speaker strategy')

    plt.subplot(3, 2, 4)
    for m in xrange(NMessages):
        plt.plot(PerceptualSpace, Hearer[m, :], label='$m_{' + str(m) + '}$')
    for m in xrange(NMessages):
        plt.plot(PerceptualSpace, HearerOptimal[m, :], linestyle='--', color='0.5')
    plt.ylim(ymin=0)
    plt.legend(loc='lower left')
    plt.title('Hearer strategy')

    plt.subplot(3, 1, 3)
    plt.plot(ExpectedUtilityHistory, label='$U(\\sigma,\\rho)$')
    plt.plot(EntropySpeakerHistory, label='$E(\\sigma)$', linestyle='--', color='green')
    plt.plot(ConvexitySpeakerHistory, label='$C(\\sigma)$', linestyle='-.', color='green')
    plt.plot(EntropyHearerHistory, label='$E(\\rho)$', linestyle='--', color='red')
    plt.plot(ConvexityHearerHistory, label='$C(\\rho)$', linestyle='-.', color='red')
    plt.ylim(ymin= -0.1, ymax=1.1)
    plt.legend(loc='upper right')
    plt.title('Measures')

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
    
def ExpectedUtility(Speaker, Hearer, Utility):
    return np.sum(Speaker[t1, m] * Hearer[m, t2] * Utility[t1, t2]
                  for t1 in xrange(Speaker.shape[0])
                  for m in xrange(Speaker.shape[1])
                  for t2 in xrange(Hearer.shape[1]))

def NormalizedEntropy(Strategy):
    return -sum(np.log(Strategy[c, a]) * Strategy[c, a] if Strategy[c, a] != 0 else 0
                 for c in xrange(Strategy.shape[0]) for a in xrange(Strategy.shape[1])) / (Strategy.shape[0] * np.log(Strategy.shape[1]))

def convex_sequences(options, length, current=None, acc=[]):
    if length == 0:
        return [acc]
    else:
        result = []
        for x in options:
            new_acc = list(acc)
            new_acc.append(x)
            new_options = list(options)
            if x != current and current in new_options:
                new_options.remove(current)
            for seq in convex_sequences(new_options, length - 1, x, new_acc):
                result.append(seq)
        return result

def Convexity(Strategy):
    ConvexPureStrategies = convex_sequences(range(Strategy.shape[1]), Strategy.shape[0])
    return sum(np.prod([ Strategy[c, s[c]] for c in xrange(Strategy.shape[0])])
               for s in ConvexPureStrategies)

# # Settings

NStates = 6
PriorDistributionType = 'uniform'

NMessages = 2

Dynamics = 'replicator dynamics'
Impairment = 0.1

Tolerance = 0.2

# # Batch mode

BatchMode = False

if BatchMode:
    if len(sys.argv) < 3:
        print "Usage: python", sys.argv[0], "<number of states> <acuity>"
        sys.exit(1)
    else:
        NStates = int(sys.argv[1])
        Impairment = float(sys.argv[2])

# # Initialization

PerceptualSpace = np.linspace(0, 1, NStates, endpoint=False)

if PriorDistributionType == 'uniform':
    Priors = stats.uniform.pdf(PerceptualSpace, loc=0, scale=NStates)
elif PriorDistributionType == 'normal':
    Priors = stats.norm.pdf(PerceptualSpace, loc=0.5, scale=0.1)

Distance = np.array([ [ abs(x - y) for y in PerceptualSpace ] for x in PerceptualSpace ])

Utility = np.exp(-(Distance ** 2 / Tolerance ** 2))

Confusion = np.exp(-(Distance ** 2 / Impairment ** 2)) if Impairment != 0 else np.identity(NStates)

Speaker = random.dirichlet([1] * NMessages, NStates)
Hearer = random.dirichlet([1] * NStates, NMessages)

ExpectedUtilityHistory = []

EntropySpeakerHistory = []
EntropyHearerHistory = []

ConvexitySpeakerHistory = []
ConvexityHearerHistory = []

if NMessages == 2:
    SpeakerOptimal = np.array([[1, 0]] * (NStates / 2) + [[0, 1]] * (NStates / 2))
    HearerOptimal = np.zeros((NMessages, NStates))
    HearerOptimal[0, (NStates / 2 - 1) / 2] = 1
    HearerOptimal[1, NStates - 1 - (NStates / 2 - 1) / 2] = 1
else:
    SpeakerOptimal, HearerOptimal = copy.deepcopy(Speaker), copy.deepcopy(Hearer)
    converged = False
    while not converged:
    
        SpeakerOptimalBefore, HearerOptimalBefore = copy.deepcopy(SpeakerOptimal), copy.deepcopy(HearerOptimal)
    
        UtilitySpeakerOptimal = np.array([ [ np.dot(HearerOptimal[m], Utility[t]) for m in xrange(NMessages) ] for t in xrange(NStates) ])
    
        for t in xrange(NStates):
            for m in xrange(NMessages):
                    SpeakerOptimal[t, m] = 1 if UtilitySpeakerOptimal[t, m] == max(UtilitySpeakerOptimal[t]) else 0
    
        SpeakerOptimal = makePDFPerRow(SpeakerOptimal)
    
        UtilityHearerOptimal = np.array([ [ np.dot(Priors * SpeakerOptimal[:, m], Utility[t]) for t in xrange(NStates) ] for m in xrange(NMessages) ])
    
        for m in xrange(NMessages):
            for t in xrange(NStates):
                    HearerOptimal[m, t] = 1 if UtilityHearerOptimal[m, t] == max(UtilityHearerOptimal[m]) else 0
    
        HearerOptimal = makePDFPerRow(HearerOptimal)
    
        if np.sum(abs(SpeakerOptimal - SpeakerOptimalBefore)) == 0 and np.sum(abs(HearerOptimal - HearerOptimalBefore)) == 0:
            converged = True

OptimalExpectedUtility = ExpectedUtility(SpeakerOptimal, HearerOptimal, Utility)

i = 0
converged = False
while not converged:
    i += 1
    
    if not BatchMode: plotStrategies()

    SpeakerBefore, HearerBefore = copy.deepcopy(Speaker), copy.deepcopy(Hearer)

    ExpectedUtilityHistory.append(ExpectedUtility(Speaker, Hearer, Utility) / OptimalExpectedUtility)

    EntropySpeakerHistory.append(NormalizedEntropy(Speaker))
    EntropyHearerHistory.append(NormalizedEntropy(Hearer))

    ConvexitySpeakerHistory.append(Convexity(Speaker))
    ConvexityHearerHistory.append(Convexity(Hearer))

    # # Dynamics
    
    # # Speaker strategy
    
    UtilitySpeaker = np.array([ [ np.dot(Hearer[m], Utility[t]) for m in xrange(NMessages) ] for t in xrange(NStates) ])

    for t in xrange(NStates):
        for m in xrange(NMessages):
            if Dynamics == 'replicator dynamics':
                Speaker[t, m] = Speaker[t, m] * UtilitySpeaker[t, m] * NMessages / sum(UtilitySpeaker[t])
            elif Dynamics == 'best response':
                Speaker[t, m] = 1 if UtilitySpeaker[t, m] == max(UtilitySpeaker[t]) else 0

    Speaker = np.dot(Confusion, Speaker)

    Speaker = makePDFPerRow(Speaker)
    
    # # Hearer strategy
    
    UtilityHearer = np.array([ [ np.dot(Priors * Speaker[:, m], Utility[t]) for t in xrange(NStates) ] for m in xrange(NMessages) ])

    for m in xrange(NMessages):
        for t in xrange(NStates):
            if Dynamics == 'replicator dynamics':
                Hearer[m, t] = Hearer[m, t] * UtilityHearer[m, t] * NStates / sum(UtilityHearer[m])
            elif Dynamics == 'best response':
                Hearer[m, t] = 1 if UtilityHearer[m, t] == max(UtilityHearer[m]) else 0

    Hearer = np.dot(Hearer, np.transpose(Confusion))

    Hearer = makePDFPerRow(Hearer)

    if np.sum(abs(Speaker - SpeakerBefore)) < 0.01 and np.sum(abs(Hearer - HearerBefore)) < 0.01:
        converged = True
        if not BatchMode: print 'Language converged!'

if not BatchMode: plotStrategies(block=True)

csv.writer(sys.stdout).writerow([NStates, PriorDistributionType, NMessages, Impairment, Tolerance, Dynamics, \
    NormalizedEntropy(Speaker), NormalizedEntropy(Hearer), \
    Convexity(Speaker), Convexity(Hearer), \
    ExpectedUtility(Speaker, Hearer, Utility) / OptimalExpectedUtility, i, \
    Speaker.tolist(), Hearer.tolist()])

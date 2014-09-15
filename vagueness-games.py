import sys
import copy
import csv
import math

import numpy as np
from numpy import random as random

from scipy import stats as stats

import matplotlib.pyplot as plt
import itertools

from datetime import datetime

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
    plt.legend(loc='best')
    plt.title('Speaker strategy')

    plt.subplot(3, 2, 4)
    for m in xrange(NMessages):
        plt.plot(PerceptualSpace, Hearer[m, :], label='$m_{' + str(m) + '}$')
    for m in xrange(NMessages):
        plt.plot(PerceptualSpace, HearerOptimal[m, :], linestyle='--', color='0.5')
    plt.ylim(ymin=0)
    plt.legend(loc='best')
    plt.title('Hearer strategy')

    plt.subplot(3, 1, 3)
    plt.plot(ExpectedUtilityHistory, label='$U(\\sigma,\\rho)$')
    plt.plot(EntropySpeakerHistory, label='$E(\\sigma)$', linestyle='--', color='green')
    plt.plot(ConvexitySpeakerHistory, label='$C(\\sigma)$', linestyle='--', color='red')
    plt.plot(VoronoinessSpeakerHistory, label='$V(\\sigma)$', linestyle='--', color='brown')
    plt.plot(InformativitySpeakerHistory, label='$I(\\sigma)$', linestyle='--', color='purple')
    plt.plot(EntropyHearerHistory, label='$E(\\rho)$', linestyle='-.', color='green')
#    plt.plot(ConvexityHearerHistory, label='$C(\\rho)$', linestyle='-.', color='red')
    plt.plot(VoronoinessHearerHistory, label='$V(\\rho)$', linestyle='-.', color='brown')
    plt.plot(InformativityHearerHistory, label='$I(\\rho)$', linestyle='-.', color='purple')
    plt.ylim(ymin= -0.1, ymax=1.1)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=8)
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

def Voronoiness(HearerStrategy, SpeakerStrategy, StateSimilarity):
    Prototypes = [ np.argmax(HearerStrategy[m]) for m in xrange(HearerStrategy.shape[0]) ]

    acc = 0.0
    for m in xrange(HearerStrategy.shape[0]):
        p = Prototypes[m]
        for t1 in xrange(HearerStrategy.shape[1]):
            for t2 in xrange(HearerStrategy.shape[1]):
                if (StateSimilarity[t1, p] > StateSimilarity[t2, p] and HearerStrategy[m, t1] > HearerStrategy[m, t2]) \
                   or (StateSimilarity[t1, p] <= StateSimilarity[t2, p] and HearerStrategy[m, t1] <= HearerStrategy[m, t2]):
                    acc += 1
    HearerVoronoiness = acc / (HearerStrategy.shape[0] * HearerStrategy.shape[1] * HearerStrategy.shape[1])

    acc = 0.0
    for t in xrange(SpeakerStrategy.shape[0]):
        for m1 in xrange(SpeakerStrategy.shape[1]):
            p1 = Prototypes[m1]
            for m2 in xrange(SpeakerStrategy.shape[1]):
                p2 = Prototypes[m2]
                if (StateSimilarity[t, p1] > StateSimilarity[t, p2] and SpeakerStrategy[t, m1] > SpeakerStrategy[t, m2]) \
                   or (StateSimilarity[t, p1] <= StateSimilarity[t, p2] and SpeakerStrategy[t, m1] <= SpeakerStrategy[t, m2]):
                    acc += 1
    SpeakerVoronoiness = acc / (SpeakerStrategy.shape[0] * SpeakerStrategy.shape[1] * SpeakerStrategy.shape[1])

    return (SpeakerVoronoiness, HearerVoronoiness)

def InformationQuantity(SpeakerStrategy, HearerStrategy, Priors):
    NStates = SpeakerStrategy.shape[0]
    NMessages = SpeakerStrategy.shape[1]
    NActs = HearerStrategy.shape[1]

    InformationOnStatesPerMessage = np.zeros(NMessages)
    for m in xrange(NMessages):
        MessageProbability = sum(Priors[t] * SpeakerStrategy[t, m] for t in xrange(NStates))
        for t in xrange(NStates):
            ConditionalProbability = (SpeakerStrategy[t, m] * Priors[t]) / MessageProbability
            InformationOnStatesPerMessage[m] += ConditionalProbability * np.log(ConditionalProbability / Priors[t]) if ConditionalProbability != 0 else 0
    InformationOnStates = sum(InformationOnStatesPerMessage[m] for m in xrange(NMessages)) / NMessages

    InformationOnActsPerMessage = np.zeros(NMessages)
    for m in xrange(NMessages):
        for a in xrange(NActs):
            ActProbability = sum(Priors[t] * SpeakerStrategy[t, m2] * HearerStrategy[m2, a] for t in xrange(NStates) for m2 in xrange(NMessages))
            InformationOnActsPerMessage[m] += HearerStrategy[m, a] * np.log(HearerStrategy[m, a] / ActProbability) if HearerStrategy[m, a] != 0 else 0
    InformationOnActs = sum(InformationOnActsPerMessage[m] for m in xrange(NMessages)) / NMessages

    return (InformationOnStates, InformationOnActs)

# # Settings

NStates = 6
PriorDistributionType = 'uniform'

NMessages = 2

Dynamics = 'replicator dynamics'

Impairment = 0.2
Tolerance = 0.025

convThreshold = 0.001
rounds = 200

OutputFile = sys.stdout

# # Batch mode

BatchMode = len(sys.argv) > 1

if BatchMode:
    if len(sys.argv) < 5:
        print "Usage: python", sys.argv[0], "<number of states> <number of messages> <impairment> <output file>"
        sys.exit(1)
    else:
        NStates = int(sys.argv[1])
        NMessages = int(sys.argv[2])
        Impairment = float(sys.argv[3])
        OutputFile = open(sys.argv[4], 'ab')

# # Initialization

PerceptualSpace = np.linspace(0, 1, NStates, endpoint=True)

if PriorDistributionType == 'uniform':
    Priors = stats.uniform.pdf(PerceptualSpace, loc=0, scale=NStates)
elif PriorDistributionType == 'normal':
    Priors = stats.norm.pdf(PerceptualSpace, loc=0.5, scale=0.1)

Distance = np.array([ [ abs(x - y) for y in PerceptualSpace ] for x in PerceptualSpace ])

Similarity = np.exp(-(Distance ** 2 / Tolerance ** 2))

Utility = Similarity

Confusion = np.exp(-(Distance ** 2 / Impairment ** 2)) if Impairment != 0 else np.identity(NStates)
Confusion = makePDFPerRow(Confusion)

Speaker = random.dirichlet([1] * NMessages, NStates)
Hearer = random.dirichlet([1] * NStates, NMessages)

ExpectedUtilityHistory = []

EntropySpeakerHistory = []
EntropyHearerHistory = []

ConvexitySpeakerHistory = []
ConvexityHearerHistory = []

VoronoinessSpeakerHistory = []
VoronoinessHearerHistory = []

InformativitySpeakerHistory = []
InformativityHearerHistory = []

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

    (SpeakerVoronoiness, HearerVoronoiness) = Voronoiness(Hearer, Speaker, Similarity)
    VoronoinessSpeakerHistory.append(SpeakerVoronoiness)
    VoronoinessHearerHistory.append(HearerVoronoiness)

    (InformativitySpeaker, InformativityHearer) = InformationQuantity(Speaker, Hearer, Priors)
    InformativitySpeakerHistory.append(InformativitySpeaker)
    InformativityHearerHistory.append(InformativityHearer)

    # # Dynamics

    # # Speaker strategy

    UtilitySpeaker = np.array([ [ np.dot(Hearer[m], Utility[t]) for m in xrange(NMessages) ] for t in xrange(NStates) ])

    for t in xrange(NStates):
        for m in xrange(NMessages):
            if Dynamics == 'replicator dynamics':
                Speaker[t, m] = Speaker[t, m] * UtilitySpeaker[t, m]
            elif Dynamics == 'best response':
                Speaker[t, m] = 1 if UtilitySpeaker[t, m] == max(UtilitySpeaker[t]) else 0

    if Dynamics == 'replicator dynamics': Speaker = makePDFPerRow(Speaker)

    Speaker = np.dot(Confusion, Speaker)

    # # Hearer strategy

    UtilityHearer = np.array([ [ np.dot(Priors * Speaker[:, m], Utility[t]) for t in xrange(NStates) ] for m in xrange(NMessages) ])

    for m in xrange(NMessages):
        for t in xrange(NStates):
            if Dynamics == 'replicator dynamics':
                Hearer[m, t] = Hearer[m, t] * UtilityHearer[m, t] * NStates / sum(UtilityHearer[m])
            elif Dynamics == 'best response':
                Hearer[m, t] = 1 if UtilityHearer[m, t] == max(UtilityHearer[m]) else 0

    if Dynamics == 'replicator dynamics': Hearer = makePDFPerRow(Hearer)

    Hearer = np.dot(Hearer, Confusion)

    if (np.sum(abs(Speaker - SpeakerBefore)) < convThreshold and np.sum(abs(Hearer - HearerBefore)) < convThreshold) or i > rounds:
        converged = True
        if not BatchMode: print 'Language converged!'

if not BatchMode: plotStrategies(block=True)

ResultsDirectory = 'results/strategies'
SimulationID = datetime.today().strftime('%Y%m%d-%H%M%S-%f')
SpeakerOutputFilename = ResultsDirectory + '/' + SimulationID + '-speaker.csv'
HearerOutputFilename = ResultsDirectory + '/' + SimulationID + '-hearer.csv'
np.savetxt(SpeakerOutputFilename, Speaker, delimiter=',')
np.savetxt(HearerOutputFilename, Hearer, delimiter=',')

(SpeakerVoronoiness, HearerVoronoiness) = Voronoiness(Hearer, Speaker, Similarity)
(InformativitySpeaker, InformativityHearer) = InformationQuantity(Speaker, Hearer, Priors)
csv.writer(OutputFile).writerow([NStates, PriorDistributionType, NMessages, Impairment, Tolerance, Dynamics, \
    NormalizedEntropy(Speaker), NormalizedEntropy(Hearer), \
    Convexity(Speaker), Convexity(Hearer), \
    SpeakerVoronoiness, HearerVoronoiness, \
    InformativitySpeaker, InformativityHearer, \
    ExpectedUtility(Speaker, Hearer, Utility) / OptimalExpectedUtility, i, \
    SpeakerOutputFilename, HearerOutputFilename])

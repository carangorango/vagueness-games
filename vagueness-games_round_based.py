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

PriorDistributionType = 'uniform'
Dynamics = 'replicator dynamics'
Tolerance = 0.1

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

Speaker = random.dirichlet([1] * NMessages, NStates)
Hearer = random.dirichlet([1] * NStates, NMessages)

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


for i in xrange(101):

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

    if i % 5 == 0:

        csv.writer(OutputFile).writerow([NStates, PriorDistributionType, NMessages, Impairment, Tolerance, Dynamics, \
            ExpectedUtility(Speaker, Hearer, Utility) / OptimalExpectedUtility, i])

import copy
import csv
import matplotlib.pyplot as plt
import numpy as np
import sys
from datetime import datetime
from numpy import random as random
from scipy import stats as stats


def plotStrategies(block=False):
    plt.clf()

    # plt.subplot(4, 2, 1)
    # plt.plot(PerceptualSpace, Priors)
    # plt.ylim(ymin=0)
    # plt.title('Priors')

    for i in xrange(NPopulations):
        plt.subplot(4, NPopulations, 1 + i)
        plt.imshow(SenderConfusions[i], origin='lower', interpolation='none')
        # plt.title('Confusion')

    for i in xrange(NPopulations):
        plt.subplot(4, NPopulations, NPopulations + 1 + i)
        for m in xrange(NMessages):
            plt.plot(PerceptualSpace, Speakers[i][:, m], label='$m_{' + str(m) + '}$')
        plt.ylim(-0.1, 1.1)
        plt.legend(loc='best')
        # plt.title('Speaker strategy')
        plt.subplot(4, NPopulations, 2 * NPopulations + 1 + i)
        for m in xrange(NMessages):
            plt.plot(PerceptualSpace, Hearers[i][m, :], label='$m_{' + str(m) + '}$')
        plt.ylim(ymin=0)
        plt.legend(loc='best')
        # plt.title('Hearer strategy')

    plt.subplot(4, 3, 10)
    for i in xrange(NPopulations):
        plt.plot(ExpectedUtilityHistorySenders[:, i], label=Impairments[i])
    plt.legend(loc='upper left', prop={'size': 8})
    plt.subplot(4, 3, 11)
    for i in xrange(NPopulations):
        plt.plot(ExpectedUtilityHistoryReceivers[:, i], label=Impairments[i])
    plt.legend(loc='upper left', prop={'size': 8})
    plt.subplot(4, 3, 12)
    for i in xrange(NPopulations):
        plt.plot(PopulationProportionsHistory[:, i], label=Impairments[i])
    plt.legend(loc='upper left', prop={'size': 8})

    #     plt.subplot(3, 1, 3)
    #     plt.plot(ExpectedUtilityHistory, label='$U(\\sigma,\\rho)$')
    #     plt.plot(EntropySpeakerHistory, label='$E(\\sigma)$', linestyle='--', color='green')
    #     plt.plot(ConvexitySpeakerHistory, label='$C(\\sigma)$', linestyle='--', color='red')
    #     plt.plot(VoronoinessSpeakerHistory, label='$V(\\sigma)$', linestyle='--', color='brown')
    #     plt.plot(InformativitySpeakerHistory, label='$I(\\sigma)$', linestyle='--', color='purple')
    #     plt.plot(EntropyHearerHistory, label='$E(\\rho)$', linestyle='-.', color='green')
    # #    plt.plot(ConvexityHearerHistory, label='$C(\\rho)$', linestyle='-.', color='red')
    #     plt.plot(VoronoinessHearerHistory, label='$V(\\rho)$', linestyle='-.', color='brown')
    #     plt.plot(InformativityHearerHistory, label='$I(\\rho)$', linestyle='-.', color='purple')
    #     plt.ylim(ymin= -0.1, ymax=1.1)
    #     plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=8)
    #     plt.title('Measures')

    plt.show(block=block)
    plt.pause(0.01)


def normalize(Vector):
    return Vector / np.max(Vector)


def makePDF(Vector):
    if np.sum(Vector) == 0:
        Vector = np.ones(np.shape(Vector))
    return Vector / np.sum(Vector)


def makePDFPerRow(Matrix):
    return np.array([makePDF(Row) for Row in Matrix])


def ExpectedUtility(Speaker, Hearer, Utility):
    return np.sum(Speaker[t1, m] * Hearer[m, t2] * Utility[t1, t2]
                  for t1 in xrange(Speaker.shape[0])
                  for m in xrange(Speaker.shape[1])
                  for t2 in xrange(Hearer.shape[1]))


def ExpectedUtilitySpeaker(Speaker, Hearers, HearersProbabilities, Utility):
    return np.sum(HearersProbabilities[k] * ExpectedUtility(Speaker, Hearers[k], Utility)
                  for k in xrange(len(Hearers)))


def ExpectedUtilityHearer(Speakers, SpeakersProbabilities, Hearer, Utility):
    return np.sum(SpeakersProbabilities[k] * ExpectedUtility(Speakers[k], Hearer, Utility)
                  for k in xrange(len(Speakers)))


def NormalizedEntropy(Strategy):
    return -sum(np.log(Strategy[c, a]) * Strategy[c, a] if Strategy[c, a] != 0 else 0
                for c in xrange(Strategy.shape[0]) for a in xrange(Strategy.shape[1])) / (
               Strategy.shape[0] * np.log(Strategy.shape[1]))


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
    return sum(np.prod([Strategy[c, s[c]] for c in xrange(Strategy.shape[0])])
               for s in ConvexPureStrategies)


def ConvexityCat(Strategy):
    ConvexPureStrategies = convex_sequences(range(Strategy.shape[1]), Strategy.shape[0])
    return sum(np.prod([Strategy[c, s[c]] == max(Strategy[c]) for c in xrange(Strategy.shape[0])])
               for s in ConvexPureStrategies)


def Voronoiness(HearerStrategy, SpeakerStrategy, StateSimilarity):
    Prototypes = [np.argmax(HearerStrategy[m]) for m in xrange(HearerStrategy.shape[0])]

    acc = 0.0
    for m in xrange(HearerStrategy.shape[0]):
        p = Prototypes[m]
        for t1 in xrange(HearerStrategy.shape[1]):
            for t2 in xrange(HearerStrategy.shape[1]):
                if (StateSimilarity[t1, p] > StateSimilarity[t2, p] and HearerStrategy[m, t1] > HearerStrategy[m, t2]) \
                        or (StateSimilarity[t1, p] <= StateSimilarity[t2, p] and HearerStrategy[m, t1] <=
                            HearerStrategy[m, t2]):
                    acc += 1
    HearerVoronoiness = acc / (HearerStrategy.shape[0] * HearerStrategy.shape[1] * HearerStrategy.shape[1])

    acc = 0.0
    for t in xrange(SpeakerStrategy.shape[0]):
        for m1 in xrange(SpeakerStrategy.shape[1]):
            p1 = Prototypes[m1]
            for m2 in xrange(SpeakerStrategy.shape[1]):
                p2 = Prototypes[m2]
                if (StateSimilarity[t, p1] > StateSimilarity[t, p2] and SpeakerStrategy[t, m1] > SpeakerStrategy[t, m2]) \
                        or (StateSimilarity[t, p1] <= StateSimilarity[t, p2] and SpeakerStrategy[t, m1] <=
                            SpeakerStrategy[t, m2]):
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
            InformationOnStatesPerMessage[m] += ConditionalProbability * np.log(
                ConditionalProbability / Priors[t]) if ConditionalProbability != 0 else 0
    InformationOnStates = sum(InformationOnStatesPerMessage[m] for m in xrange(NMessages)) / NMessages

    InformationOnActsPerMessage = np.zeros(NMessages)
    for m in xrange(NMessages):
        for a in xrange(NActs):
            ActProbability = sum(
                Priors[t] * SpeakerStrategy[t, m2] * HearerStrategy[m2, a] for t in xrange(NStates) for m2 in
                xrange(NMessages))
            InformationOnActsPerMessage[m] += HearerStrategy[m, a] * np.log(HearerStrategy[m, a] / ActProbability) if \
                HearerStrategy[m, a] != 0 else 0
    InformationOnActs = sum(InformationOnActsPerMessage[m] for m in xrange(NMessages)) / NMessages

    return (InformationOnStates, InformationOnActs)


# # Settings

NStates = 30
PriorDistributionType = 'uniform'
NMessages = 2
Dynamics = 'replicator dynamics'
Impairments = [0.0, 0.05]
PopulationProportions = makePDF(np.ones(len(Impairments)))
NewPopulationRate = 0.05
Tolerance = 0.1
convThreshold = 0.001
rounds = 200
MetaDynamicsStep = 1
SubPopulationInteraction = 'weakest'

# # Batch mode

BatchMode = len(sys.argv) > 1

if BatchMode:
    if len(sys.argv) < 5:
        print "Usage: python", sys.argv[
            0], "--batch <number of states> <meta dynamics step> <birth rate> <sub-population interaction type> <<impairment proportion>...>"
        sys.exit(1)
    else:
        NStates = int(sys.argv[2])
        MetaDynamicsStep = int(sys.argv[3])
        NewPopulationRate = float(sys.argv[4])
        SubPopulationInteraction = sys.argv[5]
        Impairments = []
        PopulationProportions = []
        for i in xrange(6, len(sys.argv), 2):
            Impairments.append(float(sys.argv[i]))
            PopulationProportions.append(float(sys.argv[i+1]))

# # Initialization
NPopulations = len(Impairments)

PopulationProportions = makePDF(PopulationProportions)

PerceptualSpace = np.linspace(0, 1, NStates, endpoint=True)
if PriorDistributionType == 'uniform':
    Priors = stats.uniform.pdf(PerceptualSpace, loc=0, scale=NStates)
elif PriorDistributionType == 'normal':
    Priors = stats.norm.pdf(PerceptualSpace, loc=0.5, scale=0.1)

Distance = np.array([[abs(x - y) for y in PerceptualSpace] for x in PerceptualSpace])
Similarity = np.exp(-(Distance ** 2 / Tolerance ** 2))
Utility = Similarity

SenderConfusions = [
    makePDFPerRow(np.exp(-(Distance ** 2 / x ** 2)) if x != 0 else np.identity(NStates))
    for x in Impairments
]
ReceiverConfusions = [
    makePDFPerRow(np.exp(-(Distance ** 2 / x ** 2)) if x != 0 else np.identity(NStates))
    for x in Impairments
]

Speakers = [random.dirichlet([1] * NMessages, NStates)] * NPopulations
Hearers = [random.dirichlet([1] * NStates, NMessages)] * NPopulations

ExpectedUtilitiesSenders = [ExpectedUtilitySpeaker(Speakers[j], Hearers, PopulationProportions, Utility)
                            for j in xrange(NPopulations)]
ExpectedUtilitiesHearers = [ExpectedUtilityHearer(Speakers, PopulationProportions, Hearers[j], Utility)
                            for j in xrange(NPopulations)]

SubPopulationMeasurements = []
for j in xrange(NPopulations):
    SubPopulationMeasurements.append({
        'number.of.states': NStates,
        'birth.rate': NewPopulationRate,
        'meta.step': MetaDynamicsStep,
        'interaction': SubPopulationInteraction,
        'iteration': 0,
        'impairment': Impairments[j],
        'sender.converged': False,
        'receiver.converged': False,
        'proportion': PopulationProportions[j],
        'sender.eu': ExpectedUtilitySpeaker(Speakers[j], Hearers, PopulationProportions, Utility),
        'receiver.eu': ExpectedUtilityHearer(Speakers, PopulationProportions, Hearers[j], Utility),
        'sender.entropy': NormalizedEntropy(Speakers[j]),
        'receiver.entropy': NormalizedEntropy(Hearers[j]),
        'sender.convexity': Convexity(Speakers[j]),
        'sender.convex': ConvexityCat(Speakers[j]),
    })

PopulationProportionsHistory = np.array([PopulationProportions])
ExpectedUtilityHistorySenders = np.array([ExpectedUtilitiesSenders])
ExpectedUtilityHistoryReceivers = np.array([ExpectedUtilitiesHearers])

if not BatchMode:
    plotStrategies(block=False)

converged = False
for i in xrange(1, rounds):
    # print i

    SpeakersBefore, HearersBefore = copy.deepcopy(Speakers), copy.deepcopy(Hearers)

    PoT = [makePDFPerRow(Priors * np.transpose(SenderConfusions[k]))
           for k in xrange(NPopulations)]  # prob actual state (col) given observed state (row)
    PSigma = [np.dot(SenderConfusions[k], SpeakersBefore[k])
              for k in xrange(NPopulations)]  # prob mess (col) given actual state (row)
    PSigmaInverse = [makePDFPerRow(Priors * np.transpose(PSigma[k]))
                     for k in xrange(NPopulations)]
    PRho = [np.dot(HearersBefore[k], ReceiverConfusions[k])
            for k in xrange(NPopulations)]  # prob receiver plays act (row) given message (column)
    for j in xrange(NPopulations):
        if SubPopulationInteraction == 'strong':
            PoSender = np.dot(PoT[j], np.sum(PopulationProportions[k] * PSigma[k]
                                             for k in xrange(NPopulations)))  # P_o(m|t_o)
            ExpUS = np.array([
                [np.sum([PoT[j][to, ta] * np.sum(PopulationProportions[k] * PRho[k][m, tr] * Utility[ta, tr]
                                                 for k in xrange(NPopulations)
                                                 for tr in xrange(NStates))
                         for ta in xrange(NStates)])
                 for m in xrange(NMessages)]
                for to in xrange(NStates)])
            Speakers[j] = makePDFPerRow(PoSender * ExpUS)

            PoReceiver = np.dot(np.sum(PopulationProportions[k] * PRho[k]
                                       for k in xrange(NPopulations)), SenderConfusions[j])  # P_o(t_o|m)
            ExpUR = np.array([
                [np.sum(
                    [PopulationProportions[k] * PSigmaInverse[k][m, ta] * ReceiverConfusions[j][ti, tr] * Utility[ta, tr]
                     for ta in xrange(NStates)
                     for tr in xrange(NStates)
                     for k in xrange(NPopulations)])
                    for ti in xrange(NStates)]
                for m in xrange(NMessages)])
            Hearers[j] = makePDFPerRow(PoReceiver * ExpUR)
        elif SubPopulationInteraction == 'weak':
            PoSender = np.dot(PoT[j], PSigma[j])  # P_o(m|t_o)
            ExpUS = np.array([
                [np.sum([PoT[j][to, ta] * np.sum(PopulationProportions[k] * PRho[k][m, tr] * Utility[ta, tr]
                                                 for k in xrange(NPopulations)
                                                 for tr in xrange(NStates))
                         for ta in xrange(NStates)])
                 for m in xrange(NMessages)]
                for to in xrange(NStates)])
            Speakers[j] = makePDFPerRow(PoSender * ExpUS)

            PoReceiver = np.dot(PRho[j], SenderConfusions[j])  # P_o(t_o|m)
            ExpUR = np.array([
                [np.sum(
                    [PopulationProportions[k] * PSigmaInverse[k][m, ta] * ReceiverConfusions[j][ti, tr] * Utility[ta, tr]
                     for ta in xrange(NStates)
                     for tr in xrange(NStates)
                     for k in xrange(NPopulations)])
                    for ti in xrange(NStates)]
                for m in xrange(NMessages)])
            Hearers[j] = makePDFPerRow(PoReceiver * ExpUR)
        elif SubPopulationInteraction == 'weakest':
            PoSender = np.dot(PoT[j], PSigma[j])  # P_o(m|t_o)
            ExpUS = np.array([
                [np.sum([PoT[j][to, ta] * np.sum(PRho[j][m, tr] * Utility[ta, tr]
                                                 for tr in xrange(NStates))
                         for ta in xrange(NStates)])
                 for m in xrange(NMessages)]
                for to in xrange(NStates)])
            Speakers[j] = makePDFPerRow(PoSender * ExpUS)

            PoReceiver = np.dot(PRho[j], SenderConfusions[j])  # P_o(t_o|m)
            ExpUR = np.array([
                [np.sum(
                    [PSigmaInverse[j][m, ta] * ReceiverConfusions[j][ti, tr] * Utility[ta, tr]
                     for ta in xrange(NStates)
                     for tr in xrange(NStates)])
                    for ti in xrange(NStates)]
                for m in xrange(NMessages)])
            Hearers[j] = makePDFPerRow(PoReceiver * ExpUR)
        else:
            raise ValueError(
                'Valid sub-population interaction types are \'strong\', \'weak\', and \'weakest\'. Unknown value \'%s\''
                % SubPopulationInteraction)

    for j in xrange(NPopulations):
        ExpectedUtilitiesSenders[j] = ExpectedUtilitySpeaker(Speakers[j], Hearers, PopulationProportions, Utility)
        ExpectedUtilitiesHearers[j] = ExpectedUtilityHearer(Speakers, PopulationProportions, Hearers[j], Utility)

    ExpectedUtilityHistorySenders = np.append(ExpectedUtilityHistorySenders,
                                              [copy.deepcopy(ExpectedUtilitiesSenders)], axis=0)
    ExpectedUtilityHistoryReceivers = np.append(ExpectedUtilityHistoryReceivers,
                                                [copy.deepcopy(ExpectedUtilitiesHearers)], axis=0)

    if i % MetaDynamicsStep == 0:
        for j in xrange(NPopulations):
            PopulationProportions[j] = PopulationProportions[j] \
                                       *(ExpectedUtilitiesSenders[j] + ExpectedUtilitiesHearers[j]) \
                                       / (sum(ExpectedUtilitiesSenders) + sum(ExpectedUtilitiesHearers))
        PopulationProportions = makePDF(PopulationProportions)
        NewSpeakers = [random.dirichlet([1] * NMessages, NStates)] * NPopulations
        NewHearers = [random.dirichlet([1] * NStates, NMessages)] * NPopulations
        for j in xrange(NPopulations):
            Speakers[j] = makePDFPerRow((1 - NewPopulationRate) * Speakers[j] +
                                        NewPopulationRate * NewSpeakers[j])
            Hearers[j] = makePDFPerRow((1 - NewPopulationRate) * Hearers[j] +
                                       NewPopulationRate * NewHearers[j])

    PopulationProportionsHistory = np.append(PopulationProportionsHistory, [copy.deepcopy(PopulationProportions)], axis=0)

    SpeakersConverged = [np.sum(abs(Speakers[j] - SpeakersBefore[j])) < convThreshold for j in xrange(NPopulations)]
    HearersConverged = [np.sum(abs(Hearers[j] - HearersBefore[j])) < convThreshold for j in xrange(NPopulations)]

    for j in xrange(NPopulations):
        SubPopulationMeasurements.append({
            'number.of.states': NStates,
            'birth.rate': NewPopulationRate,
            'meta.step': MetaDynamicsStep,
            'interaction': SubPopulationInteraction,
            'iteration': i,
            'impairment': Impairments[j],
            'sender.converged': SpeakersConverged[j],
            'receiver.converged': HearersConverged[j],
            'proportion': PopulationProportions[j],
            'sender.eu': ExpectedUtilitiesSenders[j],
            'receiver.eu': ExpectedUtilitiesHearers[j],
            'sender.entropy': NormalizedEntropy(Speakers[j]),
            'receiver.entropy': NormalizedEntropy(Hearers[j]),
            'sender.convexity': Convexity(Speakers[j]),
            'sender.convex': ConvexityCat(Speakers[j]),
        })

    if not BatchMode:
        plotStrategies()

    # if all(SpeakersConverged) and all(HearersConverged):
    #     converged = True
    #     print 'Languages converged!'
    #     break

# if not BatchMode: plotStrategies(block=True)

ResultsDirectory = 'results'
SimulationID = datetime.today().strftime('%Y%m%d-%H%M%S-%f')

MeasurementsOutputFilename = ResultsDirectory + '/' + SimulationID + '-measurements.csv'
with open(MeasurementsOutputFilename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=SubPopulationMeasurements[0].keys())
    writer.writeheader()
    writer.writerows(SubPopulationMeasurements)

for i in xrange(NPopulations):
    SpeakerOutputFilename = ResultsDirectory + '/strategies/' + \
                            SimulationID + '-speaker-' + str(Impairments[i]) + '.csv'
    np.savetxt(SpeakerOutputFilename, Speakers[i], delimiter=',')
    HearerOutputFilename = ResultsDirectory + '/strategies/' + \
                           SimulationID + '-hearer-' + str(Impairments[i]) + '.csv'
    np.savetxt(HearerOutputFilename, Hearers[i], delimiter=',')

# (SpeakerVoronoiness, HearerVoronoiness) = Voronoiness(Hearer, Speaker, Similarity)
# (InformativitySpeaker, InformativityHearer) = InformationQuantity(Speaker, Hearer, Priors)
# csv.writer(OutputFile).writerow([NStates, PriorDistributionType, NMessages, Impairment, Tolerance, Dynamics, \
#     NormalizedEntropy(Speaker), NormalizedEntropy(Hearer), \
#     Convexity(Speaker), Convexity(Hearer), \
#     SpeakerVoronoiness, HearerVoronoiness, \
#     InformativitySpeaker, InformativityHearer, \
#     ExpectedUtility(Speaker, Hearer, Utility) / OptimalExpectedUtility, i, \
#     ConvexityCat(Speaker), ConvexityCat(Hearer), \
#     SpeakerOutputFilename, HearerOutputFilename])

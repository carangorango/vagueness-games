## Main changes 

We have tried to address all of the reviewers comments as well as we could, while keeping an eye on the length of the paper.

The most important changes are that, as reviewer 1 suggested, we moved the comparison between the RDD and the RMD into the appendix and we shortened the comparison to alternative approaches (saving ca. 1.5 pages).

In response to reviewer 2's comments we have also included another technical appendix section that sketches a derivation of our RDD from an agent-based update protocol. (More on this below.) This added ca. 3 pages of text. Despite adding to the length of the paper, we believe that inclusion of this nicely rounds of the picture and makes much clearer what our dynamic is or could be and what alternatives would suggest themselves.  


We also added a Figure (an example of a Voronoi language, as suggested by reviewer 1) and added explanation of the formulas and concepts in the main text (we kept the appendices fairly technical for reasons of space). To compensate for the additions, we also removed some lines and paragraphs that were more peripheral to our main concerns.

In total, the new version has ca. 200 words of main text more than the previous. 

## Reaction to reviewers

### Reviewer 1

> This paper has improved a great deal since the last version I saw.  It is now a very nice contribution.  The changes make the philosophical content of the paper much clearer and the entire thing easier to follow.  The technical level is still (probably) too high for the vast majority of the audience of PHOS and for this reason I recommend conditional acceptance.  I've included a few suggestions for how to make the paper a bit more readable.  These don't alter the main points or results (which I think are well structured at this point), just the presentation of technical details.
>
> 1) **The authors might consider moving section 4 to the appendix.**  While this work is quite interesting on its own and should be published, it is peripheral to the central arguments of the paper.  For this reason the appendix is a nice way to include it without drawing attention away from the focus on vagueness.  This also helps with the 'too technical' issue.

This section has been moved to an appendix and the main text adapted accordingly.

> 2) **Pictures could simplify explanation in a few places.**  First, when the authors describe Voronoi languages a picture of one could be very helpful.  When the authors describe sim-max games a picture of the state space would likewise be helpful.  The picture of Nosofsky-similarity functions is good.

A picture was added to illustrate the first example of a Voronoi language for the unit interval. We did not add a picture of a state-space, because of space reasons.

> 3) **Where equations are presented, describe them in words.**  It shouldn't be too hard to use everyday language to make a few of your equations easier to follow.  (The introduction to expected utility in 3.1, for example, 'The first equation shows the sender's expected utility given a particular message, state, and receiver strategy…)

We added verbal descriptions for the most important things: sender/receiver strategies, expected utility functions and definitions of diffusion. We did not do that for the metrics we used to evaluate our simulation results or for material in the appendix. This is simply because of space reasons. Still, we believe that the most important notions should now be clear even to a less technically-minded readership.

> 4)** Be sure when you introduce new terms to think about what the audience will know. ** To give examples, consider the bottom of pg 3 where you introduce the sim-max game.  It takes one line to say what a similarity metric is, and one like to say what a probability distribution is in this instance.

We added more explanation for state probabilities, similarity metric and utilities. We did not give definitions for any of these and the paper is technical enough as it is. Again, we sought a tradeoff with length, focusing on elaborating on the concepts that are most important to follow the main argument, without going into irrelevant technical detail either.


> A few little things:
>
> i) What is 'impairment' as compared to 'imprecision'?  Are they both \alpha?  Is there some reason one term shows up in fig 5 and the other in fig 7?

Thanks for spotting this. We now use uniform terminology (imprecision) throughout the paper, including labels in figures.

> ii) Section 6.2 could still be a bit shorter, though it's fine as is.

We shortened this section by ca. 1.5 pages, mainly by not explaining the details of the alternative accounts, but only sketching the main idea in so far as it is necessary to see the difference to our approach.

> iii) In fig 4, why is one of the categories 0-~.2 and then .6-1?  Does the similarity metric go around in a circle?  If not, it seems weird that 0-.2 evolved to be the first message rather than the second (which has a response closer to it).

The similarity metric does not go around in a circle. In the unit interval, distance is maximal between 0 and 1, and minimal between every point and itself, and so is perceptual similarity which is proportional to distance (see Figure 3).

Yes, it is 'weird' that this shows up under the replicator dynamics, and that is precisely our point. This configuration is presumably not dynamically stable, but it would take a very, very long time to get away from it. It is "almost stable" in this sense (an evolutionary bottleneck).

We don't have the space to elaborate on this in the paper and we also don't have a rigorous analysis of the behavior of the replicator dynamic in sim-max games at hand. But to understand how it is possible to come to such a state, notice that we could start the evolutionary run (by pure chance) with a receiver interpretation for one message that has two prototypes or peaks, so to speak, flanking the prototype of the other message. Sender strategies adapt much faster in sim-max games than receiver strategies. This is because the sender has much fewer options (two messages as opposed to 90 receiver acts/states), so that, intuitively speaking, there is much more competition among choice options on the receiver side than on the sender side (notice how ragged the receiver strategy looks in Figure 4a, while the sender part is not). As a result, with a two-prototype receiver strategy that adapts much slower, the sender strategy would be driven towards a non-convex state (as shown in Figure 4a). This need not be dynamically stable, but the payoff differences may become very low even for the sender (in the left-hand part of the interval in Figure 4a, we are relatively far away from both prototypes, so to speak), so that evolutionary adaptation slows down dramatically. Adding vagueness/noise helps avoid this problem.

> iv) On a related note, given the similarities between generalized reinforcement learning and RDD, have you thought at all about whether there is a mathematical connection?  (Mean field dynamics??)

Although it would be interesting to pursue such a connection, doing so is certainly a non-trivial task and would probably be enough work to stand and be presented on its own. We thus consider it out of scope, but we added a sentence in the paper pointing to it as possible future work. We do provide a motivation of our RDD as the mean field behavior of another agent-level adaptation process, though.

> v) Given your discussion on the top of pg 5, you might be interested in O'Connor's 2014 'Evolving Perceptual Categories', which has a discussion of how 'conceptual spaces' might arise in the first place that employs sim-max games.

This is definitely related and worth referring to. Furthermore, we realized that the reference to Jäger's related work would fit better at the end of said discussion. We thus moved those references and added O'Connor (2014) to the list.

### Reviewer 2

Before saying anything else, we would like to thank the reviewer for making us think much more deeply about how our abstract evolutionary dynamic could possibly be motivated. We apologize for not having properly understood what the reviewer had in mind the first time around. The second review was eye-opening and pushed us to dig much deeper into this issue. We are very grateful for what we learned from that!

> This is an interesting paper. It makes some clear contributions to our growing understanding of how vagueness can emerge and be sustained in signaling games. Unfortunately, **I am still not convinced that the authors’ equations for the replicator diffusion dynamic correctly reflect their written description of the process and the visualization provided in Figure 1 [now Figure 2]**. Below I have attempted to thoroughly explain some reasons for my skepticism. From my point of view, I think **the authors have two options**. **If I’m wrong about the mismatch, then they should include a correct derivation of their dynamic from “first principles,” so to speak.** This is what I’ve begun below. Start with payoffs in the game with confused states, and work from the bottom-up to derive the dynamic. **If I’m correct about the mismatch, then they should rewrite a few paragraphs early in the paper so that their description of the process matches the mathematics.** Even if I’m correct about the mismatch, the authors have still made a solid contribution to the literature and with a non-misleading write-up the results should be published.

Being presented with two options, we chose a third and did both. Most importantly, we have added an appendix section that gives a derivation of the RDD in terms of an imitation-based update protocol. But we have also amended the text to do justice to this new material and to try to avoid further misunderstanding. The most important change is the last paragraph of Section 3.2, which explains what we think the RDD could reflect.

This paragraph also stresses that there are other options for "merging" perceptual noise with the replicator dynamic. So, in direct response to the reviewer's comments and sketched formalization, our view of the RDD is that fitness-based selection (including calculation of expected utilities) is not influenced by perceptual noise. This is a simplifying, perhaps simplistic assumption that can definitely be debated (and maybe should be at some point). Our appendix section tries to justify this assumption by showing that the RDD could be considered the outcome of an imitation-based update protocol in which the agents themselves are not aware of the noise. When deriving our dynamic from imitation-based updates, this seems like a reasonable assumption, because the opposite, the assumption that agents can calculate expected utilities in such a way as to factor in perceptual noise, seems much less plausible and less in line with the idea of evolutionary game theory as modeling rather unsophisticated agents. (Yes, we admit that our derivation makes some strong assumptions about how noise is weeded out in the imitation-process, but these are not much more implausible than the usual assumptions for imitation-based update protocols which also assume that the updating agent faithfully perceives or knows the expected utility of the act (or even full strategy) of some other agent.)

This is then the main difference between ours and the approach that the reviewer seems to suggest: the issue is whether noise should be factored into the calculation of expected utilities and thereby to affect fitness-based selection. It seems to us that saying 'yes' (the reviewer's approach in as far as we understand it), 'no' (our present approach) and  also 'yes and no' can be plausible depending on what we think of the agent-level process that motivates the population-level dynamic. It would be an interesting enterprise to sort out the consequences of these alternatives. But, surely, this is not something we can do in this paper.
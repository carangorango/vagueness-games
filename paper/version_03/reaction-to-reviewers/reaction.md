# Reaction to reviewers

## Reviewer 1

> This paper has improved a great deal since the last version I saw.  It is now a very nice contribution.  The changes make the philosophical content of the paper much clearer and the entire thing easier to follow.  The technical level is still (probably) too high for the vast majority of the audience of PHOS and for this reason I recommend conditional acceptance.  I've included a few suggestions for how to make the paper a bit more readable.  These don't alter the main points or results (which I think are well structured at this point), just the presentation of technical details.
>
> 1) The authors might consider moving section 4 to the appendix.  While this work is quite interesting on its own and should be published, it is peripheral to the central arguments of the paper.  For this reason the appendix is a nice way to include it without drawing attention away from the focus on vagueness.  This also helps with the 'too technical' issue.

This section has been moved to an appendix and the main text adapted accordingly.

> 2) Pictures could simplify explanation in a few places.  First, when the authors describe Voronoi languages a picture of one could be very helpful.  When the authors describe sim-max games a picture of the state space would likewise be helpful.  The picture of Nosofsky-similarity functions is good.

A picture was added to illustrate the first example of a Voronoi language for the unit interval.

> 3) Where equations are presented, describe them in words.  It shouldn't be too hard to use everyday language to make a few of your equations easier to follow.  (The introduction to expected utility in 3.1, for example, 'The first equation shows the sender's expected utility given a particular message, state, and receiver strategy…)



> 4) Be sure when you introduce new terms to think about what the audience will know.  To give examples, consider the bottom of pg 3 where you introduce the sim-max game.  It takes one line to say what a similarity metric is, and one like to say what a probability distribution is in this instance.



> A few little things:
>
> i) What is 'impairment' as compared to 'imprecision'?  Are they both \alpha?  Is there some reason one term shows up in fig 5 and the other in fig 7?

"Impairment" and "imprecision" are indeed the same thing: \alpha. We added a footnote alerting the reader for the fact that the terms are used interchangeably.

**Is this enough or should we redo the plots?**

> ii) Section 6.2 could still be a bit shorter, though it's fine as is.

Given this is not a strict requirement, we chose to leave the section as it is given that we find the content important to situate our contribution in the context of similar work.

> iii) In fig 4, why is one of the categories 0-~.2 and then .6-1?  Does the similarity metric go around in a circle?  If not, it seems weird that 0-.2 evolved to be the first message rather than the second (which has a response closer to it).

The similarity metric does not go around in a circle. In the unit interval, distance is maximal between 0 and 1, and minimal between every point and itself, and so is perceptual similarity which is proportional to distance (see Figure 3).

**I don't see the problem...**

> iv) On a related note, given the similarities between generalized reinforcement learning and RDD, have you thought at all about whether there is a mathematical connection?  (Mean field dynamics??)

Although it would be interesting to pursue such a connection, doing so is certainly a non-trivial task and would probably be enough work to stand and be presented on its own. We thus consider it out of scope, but we added a sentence in the paper pointing to it as possible future work.

> v) Given your discussion on the top of pg 5, you might be interested in O'Connor's 2014 'Evolving Perceptual Categories', which has a discussion of how 'conceptual spaces' might arise in the first place that employs sim-max games.

This is definitely related and worth referring to. Furthermore, we realized that the reference to Jäger's related work would fit better at the end of said discussion. We thus moved those references and added O'Connor (2014) to the list.
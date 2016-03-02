---
title: "Comments to reviewers"

output:
  html_document:
    theme: cosmo
---

## Referee: 1


This paper is very nicely written and the technical results are 1) novel, 2) interesting and 3) of the right level for a publication in philosophy.

1) The author(s) should motivate the assumption of confusability of stimuli a bit more.  One or two sentences and a citation about related empirical work should do it.

> Thank you for the suggestion. We have added, on top of Section 3.2, mention to empirical results in experimental psychology that motivates for the need to consider confusability of states and for its assumed relation with similarity. We hope it is now much more clear. 

2) Section 4.2 is labeled 'Experimental set-up' and then describes simulation results.  Since there is an active debate in the philosophy of modeling about whether computer simulations should be thought of as experiments or not (with probably more philosophers leaning towards not), I would recommend relabeling this as 'Simulation set-up' or some such.

> We agree with the recommendation and have relabelled Section 4.2 as suggested.


## Referee: 2

This paper presents and analyzes an interesting variation on the traditional Lewis-style sender receiver games which is meant to model the formation of vague linguistic categories that range over a (relatively) large state space.  I believe that the model presented is interesting and the analysis is conceptually sound.  I am, however, somewhat concerned about the clarity of the arguments surrounding the application of the model to linguistic phenomena.  As a result, I recommend that the authors revise the paper to make it more clear what the model is, in fact, explaining.

> We have added some material to the introduction, the motivating section 2 (especially at the end) and a few words to the conclusion, to clarify what the explanatory goals of this paper are and what we believe its main relevant achievements are. More detail about this is given below.

There are essentially two motivations that I see in the paper.

Motivation One: Lipman's problem – it seems intuitive that evolution would reward precision, but vagueness is ubiquitous.  What gives?

Here I'm not really sure that the model provides an answer to this problem. The agents in the model are getting very close to being as precise as they can be given the constraints imposed by the modeler. So, all the explanatory work is being done by the modeler's choices. And, I think the authors would agree their choices are sufficiently arbitrary as to not provide clear explanations. (I don't mean this is a criticism of the model, just a point about what parts can be used to explain.)

To put this a slightly different way, what exactly is the answer that the model is providing to Lipman's problem?  It strikes me that the answer is “evolution can't make them any more precise.”  But this answer was an obvious answer to Lipman's problem without the authors' model, and I don't know what the model adds.

> Since this is a very natural and fair concern, the revised version of this paper addresses this issue explicitly already in the introduction. We believe that even if it is intuitively obvious that something like confusability of similar stimuli could lead to vagueness, there is still value in a rigorous formalization. A formal model would show how exactly confusability interacts with other forces in meaning evolution and whether there might be any unforeseen inconsistencies or unexpected side-effects. And indeed our formalization shows that one intuitive partial cause of vagueness has a prima facie unexpected side-effect, namely implicit regularization of evolving meanings. This is particularly noteworthy because it nicely complements results from prominent work in language evolution where regularization effects stem from inductive biases, not "mere" biases of perception.

One final thought on Lipman's problem, I find it strange that the authors don't discuss partial pooling equilibria as a potential answer to this question.  These actually do provide – at least some – explanation for why evolution might not lead to more precision even when more precision is possible.

> Indeed, the paper should mention partial pooling equilibria! Section 2.2 now includes a very brief discussion of these (with references to more in-depth discussion elsewhere). The main point is this: lack of precision due to partial pooling traps does not capture what we would like to think of as vagueness in signaling. This is what Section 2.2 tries to show with a few illustrative examples. We deliberately kept this discussion short and, unfortunately, somewhat untechnical and superficial, because the topic has been discussed elsewhere and we wanted to keep the paper concise and focused.

Motivation Two: The behavior of linguistic categories

I think the argument on the top of page 3 needs to be spelled out a little bit.  First and foremost, what does it mean to say that linguistic categories are “well-behaved and orderly”?   I see two possibilities of what the author might mean here.

1. That we group together similar things in our linguistic concepts.  That is we don't have “similarity-gaps” in our linguistic concepts where x and y are in the same category but z is not – where S(x,z) > S(x, y).  But are our categories convex in that sense?   And what exactly does that mean to say they are convex, since we are the people who impose the metric on the space in first place?  I'm a little worried that the explanandum here is a tautology – we see similar things as similar.  Furthermore, because of the relatively strong assumptions about how the similarity and utility functions are related, it's not really clear to me that this model provides much of an explanation.

> We agree that the argument needed more clarification and have thus adapted the last two paragraphs of Section 2.1. For that reason we added some additional motivation for considering convex categories and some references to relevant publications from comparative linguistics. We would still maintain that the idea of convexity of natural concepts is intuitive for words that typically relate to one-dimensional scales, like 'tall' and 'short' for height. Furthermore, we added reference to work that shows that convexity is also observable in color categorization in a large number of languages (namely the World Color Survey data). Although this is a matter of debate, we here assume that there is a clear-enough distinction between perceptual similarity and linguistic categorization (e.g., three persons of different height can be reasonably judged as more or less similar in height to each other, rather independently of whether we could call them "tall" or "short"). And even if similarity judgements were strongly affected by (linguistic) conceptualization, convexity of the latter in a space defined by the former would still not be implied. Also, we do not claim that convexity necessarily applies to all vocabulary that relates to perceptually continuous stimuli, but that it is a reasonable assumption for a number of cases and that for these cases signaling games can provide an interesting explanation for the phenomenon.
> 
> Additionally, the relation between physical objective similarity and subjective psychological similarity is supported by work in experimental psychology that studies human performance in stimulus identification tasks. We added references to this on top of Section 3.2 to further motivate our assumptions. Regarding the relation between this and utility, our main motivation is communicative success: the higher the similarity between the state picked out by the receiver based on the message selected by the sender and the state that triggered the sender to select that message, the more successful their interaction will be. Although this assumption might not apply to all possible sorts of linguistically mediated interactions, we believe it to be very reasonable for a large number of those.
> 
>  We would like to mention here as well that we see the main contribution of the paper, a novel evolutionary dynamic that integrates perceptual biases, as valuable even if the motivation for sim-max games as a possible explanation of convexity of natural categories is cast into doubt.

2. That our linguistic conceptual space is a metric space.  This is not tautologous, although I don't have the expertise to evaluate whether or not it's true.  But, here I'm not sure that a sim-max game can explain this, since the metric space is imposed by the modeler.

> A fair point that we try to address in footnote 1. For clarity, we take over the idea that similarity is a metric as a convenience assumption from the previous relevant literature. The metric and the assumptions about how similarity relates to payoffs are basic assumptions that are fed into the model and that are used to explain other phenomena of interest. 


Small comments:

I don't follow the sentence on page 1, “Since the the existence...”  Why do unclear borderline cases entail inefficiency?

> This argument is put forward by Lipman (2009). Since it would be distracting to accurately reproduce the precise formal result in the introduction, and because we believe that doing so later would bring us too much away from our positive contribution, we rephrased the statement to make the intuition behind the results clearer and to direct the reader more clearly to the appropriate reference. As the revised version of the paper hopefully makes clear, our contribution can be appreciated independently of Lipman's result: we give a formal model that integrates natural assumptions of perceptual confusion and shows that it has some intuitive and some quite unexpected but nice properties. In the interest of space and conciseness, we would therefore prefer not to reproduce the result in too much detail.

I think footnote 2 should be moved into the main text.  I'm skeptical if JMR's results would hold for any monotonic utility function on any metric space.  I think it might be better to start with euclidean space and utility function in the text (or an informal gloss).  Drop the generality that is implied by describing the game as taking place in any-old metric space and having any-old utility function that monotonically decreasing in distance, since this generality is never used in the paper.

> We have tried to follow this suggestion, but eventually decided against it. The reasoning behind this choice is given in footnote 2.

Section 3.2, I would say this is a noisy game, not noisy replicator dynamics, since the dynamics remains deterministic.  I'm worried that “noisy … dynamics” suggests a stochastic dynamics.

> Agreed. We now speak of "imprecise imitation dynamic" throughout. 

Page 7, the number of states on the previous page was $n$, now it's $n_s$.

> Thank you for catching this. We corrected $n$ on top of Section 4.1 to $n_s$.

Page 8, I take it from the figures that there are only two messages.  I don't recall being told that, although it's entirely possible I missed it.

> This is correct, a statement regarding the number of messages considered in the simulations was missing. We added a note on this at end of Section 4.1.
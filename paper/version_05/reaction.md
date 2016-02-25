# Comments

## Referee: 1

> This paper is very nicely written and the technical results are 1) novel, 2) interesting and 3) of the right level for a publication in philosophy.
>
> 1) The author(s) should motivate the assumption of confusability of stimuli a bit more.  One or two sentences and a citation about related empirical work should do it.

Thank you for the suggestion. We have added, on top of Section 3.2, mention to empirical results in experimental psychology that motivates for the need to consider confusability of states and for its assumed relation with similarity. We hope it is now much more clear. 

> 2) Section 4.2 is labeled 'Experimental set-up' and then describes simulation results.  Since there is an active debate in the philosophy of modeling about whether computer simulations should be thought of as experiments or not (with probably more philosophers leaning towards not), I would recommend relabeling this as 'Simulation set-up' or some such.

We agree with the recommendation and have relabelled Section 4.2 as suggested.


## Referee: 2

> This paper presents and analyzes an interesting variation on the traditional Lewis-style sender receiver games which is meant to model the formation of vague lingusitic categories that range over a (relatively) large state space.  I believe that the model presented is interesting and the analysis is conceptually sound.  I am, however, somewhat concerned about the clarity of the arguments surrounding the application of the model to linguistic phenomena.  As a result, I recommend that the authors revise the paper to make it more clear what the model is, in fact, explaining.
>
> There are essentially two motivations that I see in the paper.
>
> Motivation One: Lipman's problem – it seems intuitive that evolution would reward precision, but vagueness is ubiquitous.  What gives?
>
> Here I'm not really sure that the model provides an answer to this problem.  The agents in the model are getting very close to being as precise as they can be given the constraints imposed by the modeler.  So, all the explanatory work is being done by the modeler's choices.  And, I think the authors would agree their choices are sufficiently arbitrary as to not provide clear explanations.  (I don't mean this is a criticism of the model, just a point about what parts can be used to explain.)
>
> To put this a slightly different way, what exactly is the answer that the model is providing to Lipman's problem?  It strikes me that the answer is “evolution can't make them any more precise.”  But this answer was an obvious answer to Lipman's problem without the authors' model, and I don't know what the model adds.
>
> One final thought on Lipman's problem, I find it strange that the authors don't discuss partial pooling equilibria as a potential answer to this question.  These actually do provide – at least some – explanation for why evolution might not lead to more precision even when more precision is possible.

**Michael, I'll leave it to you to answer this point**

> Motivation Two: The behavior of linguistic categories
>
> I think the argument on the top of page 3 needs to be spelled out a little bit.  First and foremost, what does it mean to say that linguistic categories are “well-behaved and orderly”?   I see two possibilities of what the author might mean here.
>
> 1. That we group together similar things in our linguistic concepts.  That is we don't have “similarity-gaps” in our linguistic concepts where x and y are in the same category but z is not – where S(x,z) > S(x, y).  But are our categories convex in that sense?   And what exactly does that mean to say they are convex, since we are the people who impose the metric on the space in first place?  I'm a little worried that the explanandum here is a tautology – we see similar things as similar.  Furthermore, because of the relatively strong assumptions about how the similarity and utility functions are related, it's not really clear to me that this model provides much of an explanation.
>
> 2. That our linguistic conceptual space is a metric space.  This is not tautologous, although I don't have the expertise to evaluate whether or not it's true.  But, here I'm not sure that a sim-max game can explain this, since the metric space is imposed by the modeler.

We agree that the argument needed more clarification and have thus adapted the last two paragraphs of Section 2.1. What we originally meant was closer to possibility 1. For that reason we added some additional motivation for considering convex categories. Namely, we believe this is intuitive for words that typically relate to one-dimensional scales, like 'tall' and 'short' for height. Furthermore, we added reference to work that shows that convexity is also observable in color categorization in a large number of languages (namely the World Color Survey data). We do not claim that convexity necessarily applies to all vocabulary that relates to perceptually continuous stimuli, but that it is a reasonable assumption for a number of cases and that for these cases signaling games can provide an interesting explanation for the phenomenon.

We do not think that the explanandum is a tautology. First, the metric space tries to capture the physical properties of the potential stimuli (think of height, for example). This by itself implies nothing regarding categorization. Imagine that the agents had available as many messages as states; any arbitrary one-to-one association between states and messages would do as well, and similarity would play no role whatsoever. When we limit the number of messages, the implication that if one state triggers the use of a certain message than similar states will trigger the use of the same message is not direct. Think about the states in the borderline between the use of two messages. Think also about the possibility of solutions such as that depicted in Figure 5a. We believe that the relation between characterizing the state space as metric and the obtaining of the partitions that we do out of sim-max games is neither obvious nor trivial.
Second, the relation between physical objective similarity and subjective psychological similarity is supported by work in experimental psychology that studies human performance in stimulus identification tasks. We added references to this on top of Section 3.2 to further motivate our assumptions. Regarding the relation between this and utility, our main motivation is communicative success: the higher the similarity between the state picked out by the receiver based on the message selected by the sender and the state that triggered the sender to select that message, the more successful their interaction will be. If I ask you for a 'red' cloth thinking of strawberry red, I would be happiest if the cloth you bring me is actually strawberry red, but could be satisfied if it is just crimson instead.

> Small comments:
>
> I don't follow the sentence on page 1, “Since the the existence...”  Why do unclear borderline cases entail inefficiency?

This argument is put forward by Lipman (2009). Since it would be difficult to accurately summarize the position without straying too much away from our contribution, we rephrased the statement to more clearly direct the reader to the appropriate reference.

> I think footnote 2 should be moved into the main text.  I'm skeptical if JMR's results would hold for any monotonic utility function on any metric space.  I think it might be better to start with euclidean space and utility function in the text (or an informal gloss).  Drop the generality that is implied by describing the game as taking place in any-old metric space and having any-old utility function that monotonically decreasing in distance, since this generality is never used in the paper.

**Moved footnote into the main text. Not sure how to address the rest.**

> Section 3.2, I would say this is a noisy game, not noisy replicator dynamics, since the dynamics remains deterministic.  I'm worried that “noisy … dynamics” suggests a stochastic dynamics.

**Michael, please address this one too.**

> Page 7, the number of states on the previous page was $n$, now it's $n_s$.

Thank you for catching this. We corrected $n$ on top of Section 4.1 to $n_s$.

> Page 8, I take it from the figures that there are only two messages.  I don't recall being told that, although it's entirely possible I missed it.

This is correct, a statement regarding the number of messages considered in the simulations was missing. We added a note on this at end of Section 4.1.
# Comments

## Referee: 1

> This paper is very nicely written and the technical results are 1) novel, 2) interesting and 3) of the right level for a publication in philosophy.
>
> 1) The author(s) should motivate the assumption of confusability of stimuli a bit more.  One or two sentences and a citation about related empirical work should do it.

**What should we cite here?**

**- Individual differences in taste perception related to genetic variation: Bufe et al. The Molecular Basis of Individual Differences in Phenylthiocarbamide and Propylthiouracil Bitterness Perception. Current Biology, 2005, 15, 1-6**

**- Genetic variation related to variation in odour perception: Keller et al. Genetic variation in a human odorant receptor alters odour perception. Nature, 2007, 449, 468-472**

**- Just-noticeable difference? https://en.wikipedia.org/wiki/Just-noticeable_difference**

**- Visual uncertainty influences behavior: Van Bergen, R. S., Ma, W. J., Pratte, M. S., & Jehee, J. F. M. (2015). Sensory uncertainty decoded from visual cortex predicts behavior. Nature Neuroscience, 18(12), 1728–1730. http://doi.org/10.1038/nn.4150**

**- This looks very relevant: Barthelmé S, Mamassian P (2009) Evaluation of Objective Uncertainty in the Visual System. PLoS Comput Biol 5(9): e1000504. doi:10.1371/journal.pcbi.1000504**

**- Nosofsky**


> 2) Section 4.2 is labeled 'Experimental set-up' and then describes simulation results.  Since there is an active debate in the philosophy of modeling about whether computer simulations should be thought of as experiments or not (with probably more philosophers leaning towards not), I would recommend relabeling this as 'Simulation set-up' or some such.

**Made the change**


## Referee: 2

> This paper presents and analyzes an interesting variation on the traditional Lewis-style sender receiver games which is meant to model the formation of vague lingusitic categories that range over a (relatively) large state space.  I believe that the model presented is interesting and the analysis is conceptually sound.  I am, however, somewhat concerned about the clarity of the arguments surrounding the application of the model to linguistic phenomena.  As a result, I recommend that the authors revise the paper to make it more clear what the model is, in fact, explaining.
>
> There are essentially two motivations that I see in the paper.
>
> Motivation One: Lipman's problem – it seems intuitive that evolution would reward precision, but vagueness is ubiquitous.  What gives?
>
> Here I'm not really sure that the model provides an answer to this problem.  The agents in the model are getting very close to being as precise as they can be given the constraints imposed by the modeler.  So, all the explanatory work is being done by the modeler's choices.  And, I think the authors would agree their choices are sufficiently arbitrary as to not provide clear explanations.  (I don't mean this is a criticism of the model, just a point about what parts can be used to explain.)

**It does not follow immediately 

> To put this a slightly different way, what exactly is the answer that the model is providing to Lipman's problem?  It strikes me that the answer is “evolution can't make them any more precise.”  But this answer was an obvious answer to Lipman's problem without the authors' model, and I don't know what the model adds.
>
> One final thought on Lipman's problem, I find it strange that the authors don't discuss partial pooling equilibria as a potential answer to this question.  These actually do provide – at least some – explanation for why evolution might not lead to more precision even when more precision is possible.
>
> Motivation Two: The behavior of linguistic categories
>
> I think the argument on the top of page 3 needs to be spelled out a little bit.  First and foremost, what does it mean to say that linguistic categories are “well-behaved and orderly”?   I see two possibilities of what the author might mean here.
>
> 1. That we group together similar things in our linguistic concepts.  That is we don't have “similarity-gaps” in our linguistic concepts where x and y are in the same category but z is not – where S(x,z) > S(x, y).  But are our categories convex in that sense?   And what exactly does that mean to say they are convex, since we are the people who impose the metric on the space in first place?  I'm a little worried that the explanandum here is a tautology – we see similar things as similar.  Furthermore, because of the relatively strong assumptions about how the similarity and utility functions are related, it's not really clear to me that this model provides much of an explanation.
>
> 2. That our linguistic conceptual space is a metric space.  This is not tautologous, although I don't have the expertise to evaluate whether or not it's true.  But, here I'm not sure that a sim-max game can explain this, since the metric space is imposed by the modeler.
>
> Small comments:
>
> I don't follow the sentence on page 1, “Since the the existence...”  Why do unclear borderline cases entail inefficiency?
>
> I think footnote 2 should be moved into the main text.  I'm skeptical if JMR's results would hold for any monotonic utility function on any metric space.  I think it might be better to start with euclidean space and utility function in the text (or an informal gloss).  Drop the generality that is implied by describing the game as taking place in any-old metric space and having any-old utility function that monotonically decreasing in distance, since this generality is never used in the paper.

**Moved footnote into the main text. Not sure how to address the rest.**

> Section 3.2, I would say this is a noisy game, not noisy replicator dynamics, since the dynamics remains deterministic.  I'm worried that “noisy … dynamics” suggests a stochastic dynamics.

**The reviewer has a point that the whole game is noisy, not just the dynamic. No changes made yet.**

> Page 7, the number of states on the previous page was $n$, now it's $n_s$.

**Good catch. Changed $n$ on page 6 to $\ns$**

> Page 8, I take it from the figures that there are only two messages.  I don't recall being told that, although it's entirely possible I missed it.

**Correct. Added note on this at end of Section 4.1**
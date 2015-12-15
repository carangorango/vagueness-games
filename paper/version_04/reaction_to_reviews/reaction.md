This paper presents and analyzes an interesting variation on the traditional Lewis-style sender receiver games which is meant to model the formation of vague lingusitic categories that range over a (relatively) large state space.  I believe that the model presented is interesting and the analysis is conceptually sound.  I am, however, somewhat concerned about the clarity of the arguments surrounding the application of the model to linguistic phenomena.  As a result, I recommend that the authors revise the paper to make it more clear what the model is, in fact, explaining.
	
	the main contribution is the evolutionary dynamic; the signaling game model has been introduced and defended elsewhere

There are essentially two motivations that I see in the paper.

Motivation One: Lipman's problem – it seems intuitive that evolution would reward precision, but vagueness is ubiquitous.  What gives?

Here I'm not really sure that the model provides an answer to this problem.  The agents in the model are getting very close to being as precise as they can be given the constraints imposed by the modeler.  So, all the explanatory work is being done by the modeler's choices.  And, I think the authors would agree their choices are sufficiently arbitrary as to not provide clear explanations.  (I don't mean this is a criticism of the model, just a point about what parts can be used to explain.)

To put this a slightly different way, what exactly is the answer that the model is providing to Lipman's problem?  It strikes me that the answer is “evolution can't make them any more precise.”  But this answer was an obvious answer to Lipman's problem without the authors' model, and I don't know what the model adds.

One final thought on Lipman's problem, I find it strange that the authors don't discuss partial pooling equilibria as a potential answer to this question.  These actually do provide – at least some – explanation for why evolution might not lead to more precision even when more precision is possible.  

	our contribution is not the explanation itself: "evolution cannot make them any more precise, because of natural limitations" but a formalism that cashes out this idea in a way that does not prevent the formation of linguistic categories altogether AND that has a possibly fitness-enhancing side effect as well (regularization of categories, prevention of inefficiencies); as concerns partial pooling equilibria: see O'Connor for why these don't arise in sim-max games, and would also not be an account of "higher-order" vagueness)

Motivation Two: The behavior of linguistic categories

I think the argument on the top of page 3 needs to be spelled out a little bit.  First and foremost, what does it mean to say that linguistic categories are “well-behaved and orderly”?   I see two possibilities of what the author might mean here. 

1. That we group together similar things in our linguistic concepts.  That is we don't have “similarity-gaps” in our linguistic concepts where x and y are in the same category but z is not – where S(x,z) > S(x, y).  But are our categories convex in that sense?   And what exactly does that mean to say they are convex, since we are the people who impose the metric on the space in first place?  I'm a little worried that the explanandum here is a tautology – we see similar things as similar.  Furthermore, because of the relatively strong assumptions about how the similarity and utility functions are related, it's not really clear to me that this model provides much of an explanation.

		fair point, but we can spell this out more clearly: convexity is a generalization (Gardenfors etc.) and may easily be wrong; but work on color terms, spatial propositions etc. seems to confirm this; there are *independent* data points about what stimuli are similar and which are covered by the same word (think: psychophysic experiments vs. language-use); so there is a genuine empirical issue here, something that needs to be explained; our assumption is that this is driven not by some cognitive/innate constrained on category formation but by the requirements of successful communication; the assumption that utility is influenced by similarity is the empirically-testable explanans here;

2. That our linguistic conceptual space is a metric space.  This is not tautologous, although I don't have the expertise to evaluate whether or not it's true.  But, here I'm not sure that a sim-max game can explain this, since the metric space is imposed by the modeler.

		fair as well; we stipulate this in order to be able to work with notions like "similarity" and "convexity" etc.; it would even be possible to generalize the notion of conceptual spaces to use interval orders for state-similarity (or some such) but then we cannot as easily analyze them; but yes: the logic of argument is: if similarity is given and affects utilities (in the right way), then we see regular linguistic categories, like we arguably do


Small comments:

I don't follow the sentence on page 1, “Since the the existence...”  Why do unclear borderline cases entail inefficiency?  

	spell out

I think footnote 2 should be moved into the main text.  I'm skeptical if JMR's results would hold for any monotonic utility function on any metric space.  I think it might be better to start with euclidean space and utility function in the text (or an informal gloss).  Drop the generality that is implied by describing the game as taking place in any-old metric space and having any-old utility function that monotonically decreasing in distance, since this generality is never used in the paper. 

	okay, easy to change

Section 3.2, I would say this is a noisy game, not noisy replicator dynamics, since the dynamics remains deterministic.  I'm worried that “noisy … dynamics” suggests a stochastic dynamics.

	agree that "noisy dynamics" is misleading, but it's not a noisy game either; depends on where we draw the line between game and solution concept; best speak of a deterministic "noisy-imitation dynamic" or some such

Page 7, the number of states on the previous page was $n$, now it's $n_s$.

	easy fix

Page 8, I take it from the figures that there are only two messages.  I don't recall being told that, although it's entirely possible I missed it.

	easy fix

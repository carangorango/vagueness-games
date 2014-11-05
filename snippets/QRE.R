library(MCMCpack) # for Dirichlet distribution
library(ggplot2)
library(reshape2)

source('~/Desktop/data/svn/vagueness-games/helper_functions.R')

len = 1
ns = 50
lambda = 15
tolerance = 0.5

states = seq(0, len, length.out = ns)
priors = rep(1/ns, ns)
utils = get.confusion.matrix(states = states, alpha = tolerance)

sen = rdirichlet(ns,rep(1,2))
rec = rdirichlet(2, rep(1,ns))


for (i in 1:100){
  eu.s = get.eu.s(rec = rec, utils = utils)
  senNext = get.qbr(utils = eu.s, lambda = lambda)
  eu.r = get.eu.r(sen = sen, utils = utils, priors = priors)
  recNext = get.qbr(utils = eu.r, lambda = lambda)
  if (all(as.vector(sen) == as.vector(senNext))) {
    show("converged")
  }
  sen = senNext
  rec = recNext
}

outPlot = plot.strats(sen,rec,states)

show(outPlot)
filename = paste("paper/plots/exampleStratQRE_tolerance0", tolerance*10, ".pdf", sep = "", collapse = "")
ggsave(outPlot, file = filename, height = 5, width = 5)

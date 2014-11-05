require('plyr')
require('reshape2')
theme_set(theme_bw())

source('~/Desktop/data/svn/vagueness-games/helper_functions.R')
source('~/Desktop/data/svn/vagueness-games/data-analysis.R')

plot.and.save.language.by.index = function(data, index){
  ns = data[index,]$Number.of.states
  tolerance = data[index,]$Tolerance
  impairment = data[index,]$Impairment
  stratPlot = plot.language.byindex(data,index)
  filename = paste("~/Desktop/data/svn/vagueness-games/paper/plots/strat_example_", "ind", index, ".pdf", sep = "", collapse = "")
  pdf(file = filename, height = 2.75, width = 3)
  show(stratPlot)
  dev.off()
  show(stratPlot)
}

stratsToPlot = c(1201, 1001, 3098, 3452, 41, 23)

for (strat in stratsToPlot){
  plot.and.save.language.by.index(data,strat)
}


show(ds[stratsToPlot,])

d = subset(data, Number.of.states == 6 & Tolerance == 0.2 & Impairment == 0 & Speaker.Convex.Cat == 1)


plot.and.save.language.by.index(d, which.min(d$Expected.utility))
plot.and.save.language.by.index(d, which.max(d$Expected.utility))
d[c(which.min(d$Expected.utility), which.max(d$Expected.utility)),]
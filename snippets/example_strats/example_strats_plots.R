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
  filename = paste("~/Desktop/data/svn/vagueness-games/paper/plots/strat_example_", "NS-", ns,                    "_tol-", tolerance, "_imp", impairment, "_ind", index, ".pdf", sep = "", collapse = "")
  pdf(file = filename, height = 5, width = 5)
  show(stratPlot)
  dev.off()
}

stratsToPlot = c(1201, 1001, 3098, 3452)

# for (strat in stratsToPlot){
#   plot.and.save.language.by.index(data,strat)
# }


show(ds[stratsToPlot,])

d = subset(data, Number.of.states == 6 & Tolerance == 0.3 & Impairment == 0.05 & Speaker.Convex.Cat == 1)


# plot.and.save.language.by.index(d, which.min(d$Expected.utility))
# plot.and.save.language.by.index(d, which.max(d$Expected.utility))
# d[c(which.min(d$Expected.utility), which.max(d$Expected.utility)),]
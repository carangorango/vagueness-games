require('plyr')
require('reshape2')

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

plot.and.save.language.by.index(data,1201)
plot.and.save.language.by.index(data,1001)
plot.and.save.language.by.index(data,3098)
plot.and.save.language.by.index(data,3452)

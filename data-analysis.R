require(ggplot2)
require(reshape)
require(gridExtra)

theme_set(theme_bw())

plot.language <- function(speaker.filename, hearer.filename) {

    speaker.filename = paste("~/Desktop/data/svn/vagueness-games/", speaker.filename, sep="",col="")
    hearer.filename = paste("~/Desktop/data/svn/vagueness-games/" , hearer.filename , sep="",col="")
  
    speaker <- read.csv(speaker.filename, header=FALSE, colClasses='numeric')
    hearer <- read.csv(hearer.filename, header=FALSE, colClasses='numeric')

    stopifnot(ncol(speaker) == nrow(hearer), nrow(speaker) == ncol(hearer))
    
    nstates <- nrow(speaker)
    nmessages <- nrow(hearer)
    
    states <- 0:(nstates-1)/(nstates-1)
    
    melted.speaker <- melt(speaker, measure.vars=1:nmessages)
    melted.hearer <- melt(as.data.frame(t(hearer)), measure.vars=1:nmessages)
    
    melted.speaker$State <- states
    melted.hearer$State <- states
    
    melted.speaker$role = "sender"
    melted.hearer$role = "receiver"
    
    plotData = rbind(melted.speaker, melted.hearer)
    plotData$role = factor(plotData$role, levels = c("sender", "receiver"))
    
    p = ggplot(plotData, aes(x = State, y = value)) +
      geom_line(aes(linetype=variable)) + labs(title='',x='State',y='') +
      theme(legend.position = 'none') + 
      facet_grid(role ~ ., scales = "free_y")
    
    return(p)
      
}

plot.cluster <- function(language.names, data) {
    
    plots <- list()
    for (i in 1:length(language.names)) {
        plots[[i]] <- plot.language(data[language.names[i],'Speaker.strategy.file'], data[language.names[i],'Hearer.strategy.file'])
    }
    do.call(grid.arrange, plots)
    
}

do.stuff <- function(timestamp) {
    x <<- read.csv(paste(sep='','results/', timestamp,'.csv'), colClasses=c('numeric','factor','numeric','numeric','numeric','factor','numeric','numeric','numeric','numeric','numeric','numeric','numeric','numeric','numeric','numeric','character','character'))
    width <- 8
    height <- 5
    ggplot(x, aes(x=factor(Impairment), y=Speaker.entropy)) + geom_boxplot() + xlab('Impairment') + ylim(0, 1) + ylab(expression(E(sigma)))
    ggsave(filename=paste(sep='', 'paper/plots/', 'Speaker-entropy-', timestamp, '.png'), width=width, height=height)
    ggplot(x, aes(x=factor(Impairment), y=Hearer.entropy)) + geom_boxplot() + xlab('Impairment') + ylim(0, 1) + ylab(expression(E(rho)))
    ggsave(filename=paste(sep='', 'paper/plots/', 'Hearer-entropy-', timestamp, '.png'), width=width, height=height)
    ggplot(x, aes(x=factor(Impairment), y=Speaker.informativity)) + geom_boxplot() + xlab('Impairment') + ylim(0, 1) + ylab(expression(I(sigma)))
    ggsave(filename=paste(sep='', 'paper/plots/', 'Speaker-informativity-', timestamp, '.png'), width=width, height=height)
    ggplot(x, aes(x=factor(Impairment), y=Hearer.informativity)) + geom_boxplot() + xlab('Impairment') + ylim(0, 1) + ylab(expression(I(rho)))
    ggsave(filename=paste(sep='', 'paper/plots/', 'Hearer-informativity-', timestamp, '.png'), width=width, height=height)
    ggplot(x, aes(x=factor(Impairment), y=Speaker.Voronoiness)) + geom_boxplot() + xlab('Impairment') + ylim(0, 1) + ylab(expression(V(sigma)))
    ggsave(filename=paste(sep='', 'paper/plots/', 'Speaker-Voronoiness-', timestamp, '.png'), width=width, height=height)
    ggplot(x, aes(x=factor(Impairment), y=Hearer.Voronoiness)) + geom_boxplot() + xlab('Impairment') + ylim(0, 1) + ylab(expression(V(rho)))
    ggsave(filename=paste(sep='', 'paper/plots/', 'Hearer-Voronoiness-', timestamp, '.png'), width=width, height=height)
    ggplot(x, aes(x=factor(Impairment), y=Expected.utility)) + geom_boxplot() + xlab('Impairment') + ylim(0, 1) + ylab(expression(EU(sigma,rho)))
    ggsave(filename=paste(sep='', 'paper/plots/', 'Expected-utility-', timestamp, '.png'), width=width, height=height)
    ggplot(x, aes(x=factor(Impairment), y=Iterations)) + geom_boxplot() + xlab('Impairment')
    ggsave(filename=paste(sep='', 'paper/plots/', 'Iterations-', timestamp, '.png'), width=width, height=height)
}
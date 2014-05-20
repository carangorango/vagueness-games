require(ggplot2)
require(reshape)
require(gridExtra)

theme_set(theme_minimal())

plot.language <- function(speaker.filename, hearer.filename) {

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
    
    speaker.plot <- ggplot(melted.speaker, aes(x=State, y=value, colour=variable)) +
        geom_line() + labs(title='Speaker',x='State',y='') +
        theme(legend.position = 'none') + ylim(0,1)
    hearer.plot <- ggplot(melted.hearer, aes(x=State, y=value, colour=variable)) +
        geom_line() + labs(title='Hearer',x='State',y='') + 
        theme(legend.position = 'none')
    
    arrangeGrob(speaker.plot, hearer.plot)
    
}

plot.cluster <- function(language.names, data) {
    
    plots <- list()
    for (i in 1:length(language.names)) {
        plots[[i]] <- plot.language(data[language.names[i],'Speaker.strategy.file'], data[language.names[i],'Hearer.strategy.file'])
    }
    do.call(grid.arrange, plots)
    
}
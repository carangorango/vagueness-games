library(likert)
library(tidyverse)

read.data <- function() {
    measurement_data <<- tibble()
    for (fname in dir('.', pattern = '*.csv')) {
        x <- read_csv(fname)
        x$sender.converged <- parse_logical(toupper(x$sender.converged))
        x$receiver.converged <- parse_logical(toupper(x$receiver.converged))
        x$file <- fname
        x$populations <- as.character(summarise(x, paste(unique(impairment), collapse='/')))
        x$initial.proportions <- as.character(summarise(filter(x, iteration == 0), paste(proportion, collapse='/')))
        x$number.of.populations <- as.integer(summarise(x, length(unique(impairment))))
        measurement_data <<- rbind(measurement_data, x)
    }
    measurement_data$sim.id <<- as.integer(factor(measurement_data$file))
}

plot.proportion <- function(interaction.type, population.scenario, simulation.id=NULL) {
    dt <- filter(measurement_data, 
                 populations == population.scenario, 
                 interaction == interaction.type)
    if (!is.null(simulation.id)) {
        dt <- filter(dt, sim.id == simulation.id)
    }
    p <- ggplot(dt, aes(x=iteration, y=proportion)) +
        geom_line(aes(linetype=factor(impairment))) +
        labs(x=expression(i), y=expression(P(alpha)), linetype=expression(alpha))
    if (is.null(simulation.id)) {
        p <- p + facet_grid(. ~ sim.id) +
            scale_x_continuous(breaks=c(100,200)) + theme(axis.text.x = element_text(angle=45))
    }
    return(p)
}

plot.convex.percentage <- function(interaction.type) {
    dt <- filter(measurement_data, interaction == interaction.type | populations == '0', impairment == 0)
    p <- ggplot(dt, aes(x=iteration)) +
        stat_summary(fun.y='mean', geom='line', aes(y=sender.convex, linetype=factor(populations))) +
        labs(x=expression(i), y='Convex percentage', linetype='Scenario') + theme_bw()
    return(p)
}

plot.convex.cases <- function(interaction.type, population.scenario) {
    dt <- filter(measurement_data, interaction == interaction.type, populations == population.scenario) %>% 
        group_by(impairment, sim.id) %>% filter(sender.convex == 1) %>% 
        summarise(convex.it = first(iteration))
    p <- ggplot(dt) + geom_point(aes(x=convex.it, y=reverse.levels(factor(sim.id)), shape=factor(impairment))) +
        scale_shape(solid = FALSE) +
        labs(x=expression(i), y='Simulation', shape=expression(alpha))
    return(p)
}

plot.sender.entropy <- function(interaction.type) {
    dt <- filter(measurement_data, interaction == interaction.type | populations == '0', impairment == 0)
    p <- ggplot(dt, aes(x=iteration)) +
        # geom_point(alpha=0.1) +
        stat_summary(fun.y='mean', geom='line', aes(y=sender.entropy, linetype=factor(populations))) +
        labs(x=expression(i), y=expression(E(sigma^alpha)), linetype='Scenario') + theme_bw()
    return(p)
}

plot.receiver.entropy <- function(interaction.type) {
    dt <- filter(measurement_data, interaction == interaction.type | populations == '0', impairment == 0)
    p <- ggplot(dt, aes(x=iteration)) +
        # geom_point(alpha=0.1) +
        stat_summary(fun.y='mean', geom='line', aes(y=receiver.entropy, linetype=factor(populations))) +
        labs(x=expression(i), y=expression(E(rho^alpha)), linetype='Scenario') + theme_bw()
    return(p)
}

plot.total.entropy <- function(interaction.type) {
    dt <- filter(measurement_data, interaction == interaction.type | populations == '0')
    p <- ggplot(dt, aes(x=iteration)) +
        # geom_point(alpha=0.1) +
        stat_summary(fun.y='mean', geom='line', aes(y=sender.entropy + receiver.entropy, linetype=factor(impairment), color=factor(populations))) +
        labs(x=expression(i), y=expression(E(sigma^alpha)+E(rho^alpha)), linetype=expression(alpha), color='Scenario')
    return(p)
}

plot.language <- function(sim, impairment) {
    fname <- unique(filter(measurement_data, sim.id == sim)$file)
    fname.parts <- strsplit(fname, '-')
    simulation.id <- paste(fname.parts[[1]][1:3], collapse='-')

    message.names <- c('m1','m2')
    sigma <- read_csv(paste0('strategies/', simulation.id, '-speaker-', impairment, '.csv'), col_names = message.names)
    nstates <- nrow(sigma)
    state.names <- paste0('t', as.character(0:29/29))
    sigma <- add_column(sigma, State = state.names)
    sigma <- gather(sigma, 'Message', 'Sender', 1:2)

    rho <- read_csv(paste0('strategies/', simulation.id, '-hearer-', impairment, '.csv'), col_names = state.names)
    rho <- add_column(rho, Message = message.names)
    rho <- gather(rho, 'State', 'Receiver', 1:nstates)

    lang <- full_join(sigma, rho, by=c('State', 'Message'))
    lang <- gather(lang, 'Role', 'Probability', 3:4)
    lang$State <- as.double(substring(lang$State, 2))
    lang$Role <- factor(lang$Role, levels=c('Sender','Receiver'))
    ggplot(lang, aes(x=State, y=Probability, linetype=Message)) + 
        geom_line() +
        facet_grid(Role ~ ., scales = 'free_y') +
        theme_bw() + theme(legend.position="none") + labs(y=NULL)
}

plot.eu <- function(interaction.type, population.scenario, sim.identificator) {
    dt <- filter(measurement_data, 
                 interaction == interaction.type, 
                 populations == population.scenario,
                 sim.id == sim.identificator)
    dt2 <- filter(dt, sender.convex == 1) %>% group_by(impairment) %>% summarise(convex.it = first(iteration))
    p <- ggplot(dt, aes(x=iteration)) +
        geom_line(aes(y=sender.eu, linetype=factor(impairment)), color='red') +
        geom_line(aes(y=receiver.eu, linetype=factor(impairment)), color='green') +
        geom_vline(data = dt2, mapping = aes(xintercept = convex.it, linetype = factor(impairment))) +
        labs(x=expression(i), y=expression(EU), linetype=expression(alpha))
    return(p)
}

plot.eu.cases <- function(interaction.type, population.scenario) {
    dt <- filter(measurement_data, interaction == interaction.type, populations == population.scenario)
    p <- ggplot(dt, aes(x=iteration)) +
        geom_line(aes(y=sender.eu+receiver.eu, linetype=factor(impairment))) +
        facet_grid(. ~ sim.id) +
        labs(x=expression(i), y=expression(EU(sigma^alpha)+EU(rho^alpha)), linetype=expression(alpha), color='Scenario')
    return(p)
}

plot.eu.mean <- function(interaction.type, population.scenario=NULL) {
    if (is.null(population.scenario)) {
        dt <- filter(measurement_data, interaction == interaction.type | populations == '0')
        p <- stat_summary(fun.y='mean', geom='line', aes(y=sender.eu+receiver.eu, linetype=factor(impairment), color=factor(populations)))
    } else {
        dt <- filter(measurement_data, interaction == interaction.type, populations == population.scenario)
        p <- stat_summary(fun.y='mean', geom='line', aes(y=sender.eu+receiver.eu, linetype=factor(impairment)))
    }
    p <- ggplot(dt, aes(x=iteration)) + p +
        labs(x=expression(i), y=expression(EU(sigma^alpha)+EU(rho^alpha)), linetype=expression(alpha), color='Scenario')
    return(p)
}

show.languages <- function(interaction.type, population.scenario) {
    dt <- filter(measurement_data, interaction == interaction.type, populations == population.scenario)
    for (sim.id in unique(dt$sim.id)) {
        for (impair in unique(dt$impairment)) {
            imp <- if (impair == 0) '0.0' else as.character(impair)
            print(plot.language(sim.id, imp) + ggtitle(paste(sim.id, imp)))
            readline()
        }
    }
}

final.proportions <- function(interaction.type, population.scenario) {
    dt <- filter(measurement_data, interaction == interaction.type, populations == population.scenario) %>%
        group_by(sim.id, impairment) %>% summarise(final.proportion = last(proportion))
    return(dt)
}

initial.eu <- function(interaction.type, population.scenario) {
    dt <- filter(measurement_data, interaction == interaction.type, populations == population.scenario) %>%
        group_by(sim.id, impairment) %>% summarise(initial.eu = nth(sender.eu, 2)+nth(sender.eu, 2))
    return(dt)
}


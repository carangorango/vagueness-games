source('~/Desktop/data/svn/vagueness-games/data-analysis.R')

theme_set(theme_bw())
greyPalette = c("#999999", "#222222", "#999999", "#000000", "#999999", "#000000", "#999999", "#000000")


##################
## load data
# data = read.csv('~/Desktop/data/svn/vagueness-games/results/20140918-142408.varTolerance.csv', 
data = read.csv('~/Desktop/data/svn/vagueness-games/results/20150729-104740.csv', 
                colClasses=c('numeric','factor','numeric','numeric','numeric',
                             'factor','numeric','numeric','numeric','numeric',
                             'numeric','numeric','numeric','numeric','numeric',
                             'numeric','numeric','numeric','character','character'))

# no idea why these numbers are messed up, but this fix seems to solve it
data$Speaker.Voronoiness = ifelse(data$Speaker.Voronoiness > 1, 
                                  yes = data$Speaker.Voronoiness / 1000, 
                                  no = data$Speaker.Voronoiness)
data$Hearer.Voronoiness = ifelse(data$Hearer.Voronoiness > 1, 
                                 yes = data$Hearer.Voronoiness / 1000, 
                                 no = data$Hearer.Voronoiness)

ds = data[,c(1,4,5,7,8,11:17)] # only relevant data
dm = melt(ds,id.vars = c("Number.of.states", "Impairment", "Tolerance")) # melted data

###################

plot.language.byindex = function(dataFrame,rowindex){
  plot.language(dataFrame[rowindex,]$Speaker.strategy.file,
                dataFrame[rowindex,]$Hearer.strategy.file)
}



plot.language.MinMaxProperty = function(dataFrame,colindex){
  show(names(dataFrame)[colindex])
  show(summary(dataFrame[,colindex]))
  p = arrangeGrob(plot.language.byindex(dataFrame,which.min(dataFrame[,colindex])),
                  plot.language.byindex(dataFrame,which.max(dataFrame[,colindex])))
}

###################

get.confusion.matrix = function(states,alpha){
  ns = length(states)
  if (alpha <= 0){
    return(diag(rep(1,ns)))
  }
  C = matrix(0,nrow=ns, ncol=ns)
  for (i in 1:ns){
    for (j in 1:ns){
      C[i,j] = exp( - (states[i]-states[j])^2 / (alpha^2) )
    }
  }
  return(C)
}

# Reading a strategy.

read.speaker.strategy = function(dataFrame = data, rowIndex){
  speaker.filename = paste("~/Desktop/data/svn/vagueness-games/", 
                           dataFrame[rowIndex,]$Speaker.strategy.file, sep="",col="")
  speaker <- prop.table(as.matrix(read.csv(speaker.filename, header=FALSE, colClasses='numeric')),1)
  return(as.matrix(speaker))
}

read.hearer.strategy = function(dataFrame = data, rowIndex){
  hearer.filename = paste("~/Desktop/data/svn/vagueness-games/", 
                          dataFrame[rowIndex,]$Hearer.strategy.file, sep="",col="")
  hearer <- prop.table(as.matrix(read.csv(hearer.filename, header=FALSE, colClasses='numeric')),1)
  return(as.matrix(hearer))
}

read.strategy.byString = function(String){
  speaker.filename = paste("~/Desktop/data/svn/vagueness-games/", 
                           String, sep="",col="")
  speaker <- prop.table(as.matrix(read.csv(speaker.filename, header=FALSE, colClasses='numeric')),1)
  return(as.matrix(speaker))
}


################### best responses etc.


get.eu.r = function(sen,utils,priors){
  n.states = dim(sen)[1]
  n.messages = dim(sen)[2]
  eu.r = matrix(0,n.messages,n.states)
  for (m in 1:n.messages) {
    pf <- priors %*% sen[,m]
    for (t in 1:n.states) {
      eu.r[m,t] <- ((sen[,m]*priors)%*%utils[t,])/pf
    }
  }
  return(eu.r)
}

get.eu.s = function(rec,utils){
  eu.s = utils %*% t(rec)
  return(eu.s)
}

get.br <- function(utils) {
  # utils: matrix with choice points in rows and choices in column
  br <- t(apply(utils,1,function(x) x==max(x)))
  for (i in 1:dim(br)[1]){
    if (sum(br[i,]) == 0){
      br[i,] = 1/dim(br)[2]
    }
  }
  return(prop.table(br,1))
}

get.qbr = function(utils,lambda,succ.prop=F){
  # returns the quantal best response given:
  # utils: matrix of expected utilities
  # lambda: rationality parameter
  # succ.prob: boolean parameter;
  #  if false, a single lamda is used for each choice point
  #  as in standard quantal response;
  #  if true, each choice point receives a lambda
  #  proportional to the maximal probability of 
  #  communicative success;
  #  motivation is that decision makers may be more
  #  rational when they can be sure of success than
  #  when they cannot;
  #  the latter is only a first idea for solving
  #  Horn's DoPL using IQR
  if (succ.prop) {
    lambda.matrix =  matrix( 
      rep( lambda * (1-(1 - apply(utils,1,max))) , each=dim(utils)[2]),
      byrow=T,nrow=dim(utils)[1])
    #     lambda.matrix =  matrix( 
    #       rep( lambda * (apply(utils,1,max) + minimum) / (maximum - minimum), each=dim(utils)[1]),
    #       byrow=T,nrow=dim(utils)[2])
  }
  if (succ.prop == F) {
    lambda.matrix = lambda
  }
  prop.table(exp(lambda.matrix*utils),1)
}



optimal.strategies = function(ns) {
  # Optimal sender & receiver strategy [
  #  works ONLY for 2 messages, ns %% 2 == 0 and ns/2 %% 2 == 1,  and flat priors only
  if (!(ns %% 2 == 0 & (ns/2) %% 2 == 1)) {
    stop("cannot get optimal strategies for this state number")
  }
  sen = matrix(0, nrow =ns, ncol = 2)
  sen[1:(ns/2),1] = 1
  sen[(ns/2+1):ns,2] = 1
  rec = matrix(0, nrow = 2, ncol = ns)
  rec[1,median(1:(ns/2))] = 1
  rec[2,median((ns/2+1):ns)] = 1
  return(list(sen,rec))
}

#####################################

## plotting functions

plot.sender.strat = function(sen,states){
  senMelt = melt(sen, varnames = c("state", "message"))
  senMelt$state = rep(states, dim(sen)[2])
  senMelt$message = factor(senMelt$message)
  senPlot = ggplot(data = senMelt, aes(x = state, y = value)) + 
    geom_line(aes(linetype=message)) + labs(title='Sender',x='State',y='') +
    theme(legend.position = 'none') + ylim(0,1)
}

plot.receiver.strat = function(rec,states){
  recMelt = melt(rec, varnames = c("message", "state"))
  recMelt$state = rep(states, each = dim(rec)[1])
  recMelt$message = factor(recMelt$message)
  recPlot = ggplot(data = recMelt, aes(x = state, y = value)) + 
    geom_line(aes(linetype=message)) + labs(title='Receiver',x='State',y='') + 
    theme(legend.position = 'none')
}

plot.strats = function(sen, rec, states){
  senMelt = melt(sen, varnames = c("state", "message"))
  senMelt$state = rep(states, dim(sen)[2])
  senMelt$message = factor(senMelt$message)
  senMelt$role = "sender"
  recMelt = melt(rec, varnames = c("message", "state"))
  recMelt$state = rep(states, each = dim(rec)[1])
  recMelt$message = factor(recMelt$message)
  recMelt$role = "receiver"
  plotData = rbind(senMelt, recMelt)
  plotData$role = factor(plotData$role, levels = c("sender", "receiver"))
  outplot = ggplot(data = plotData, aes(x = state, y = value)) + 
    geom_line(aes(linetype=message)) + labs(title='',x='State',y='') +
    theme(legend.position = 'none') + facet_grid(role ~ ., scale = "free_y")
  return(outplot)
}

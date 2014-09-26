computeD = FALSE
computeEU = FALSE

require('plyr')
require('reshape2')

source('~/Desktop/data/svn/vagueness-games/helper_functions.R')

data = read.csv('~/Desktop/data/svn/vagueness-games/results/20140918-142408.varTolerance.csv', 
                colClasses=c('numeric','factor','numeric','numeric','numeric',
                             'factor','numeric','numeric','numeric','numeric',
                             'numeric','numeric','numeric','numeric','numeric',
                             'numeric','numeric','numeric','character','character'))

# Hellinger distance.

HD = function(x, y){
  return( sqrt(sum(sapply(1:length(x), function(i) (sqrt(x[i]) - sqrt(y[i]))^2  )) ) / (sqrt(2)) )
}

# Distance between two strategis as Hellinger distances at each choice point.

strategy.distance = function(P,Q){
  nc = dim(P)[1]
  sum(sapply(1:nc, function(x) return(HD(P[x,], Q[x,]) ) ) ) / nc 
}


# Get HD-strategy distance between two strategies.

speaker.strategy.distance = function(data = data, i , j){
  S1 = read.speaker.strategy(data,i)
  S2 = read.speaker.strategy(data,j)
  d1 = strategy.distance(S1,S2)
  d2 = strategy.distance(S1,S2[,c(2,1)])
  return(min(d1,d2))
}

speaker.strategy.distance.ByString = function(String1 , String2){
  S1 = read.strategy.byString(String1)
  S2 = read.strategy.byString(String2)
  d1 = strategy.distance(S1,S2)
  d2 = strategy.distance(S1,S2[,c(2,1)])
  return(min(d1,d2))
}

hearer.strategy.distance = function(data = data, i , j){
  H1 = read.hearer.strategy(data,i)
  H2 = read.hearer.strategy(data,j)
  d1 = strategy.distance(H1,H2)
  d2 = strategy.distance(H1,H2[c(2,1),])
  return(min(d1,d2))
}


# # Show that this works on two strategies that have 'reversed message use'.
# 
# i = 3504
# j = 3505
# show(arrangeGrob(plot.language.byindex(data,i), plot.language.byindex(data,j)))
# show(speaker.strategy.distance(data,i,j))
# show(hearer.strategy.distance(data,i,j))
# 
# # get average distance in a vector of strategies
# 
# speaker.vector.distance = function(Svec){
#   ns = length(Svec)
#   D = 0
#   for (i in 1:(ns-1)){
#     for (j in (i+1):ns){
#       d = speaker.strategy.distance.ByString(Svec[i],Svec[j])
#       D = c(D,d)
#     }
#   }
#   return(mean(D[-1]))
# }
# 
# # test this:
# 
# d = subset(data, Tolerance == 0.2 & Impairment == 0 & Number.of.states == 6)
# Svec = d$Speaker.strategy.file
# show(speaker.vector.distance(Svec))
# 
# # compute distances for speaker strategies
# 
ds = data[,c(1,4,5,19)] # only relevant "data" is speaker strategy file name
# ds = subset(ds,Number.of.states == 50 & Impairment == 0 & Tolerance <= 0.3)
dm = melt(ds,id.vars = c("Number.of.states", "Impairment", "Tolerance")) # melted data

if (computeD == TRUE){
  D = ddply(dm, .(Number.of.states, Impairment, Tolerance), summarise, 
            inGroupDistance = speaker.vector.distance(value))
} else{
  D = read.csv("~/Desktop/data/svn/vagueness-games/snippets/exploring_uniformity_from_impairment/D.csv")
}

pd <- position_dodge(.01)
sp = ggplot(D, aes(x=Impairment, y=inGroupDistance)) + 
  geom_point(position = pd) + geom_line()
sp + facet_grid(Number.of.states ~ Tolerance)

# compute average EU between different strategies from the same parameter triple

expected.utility = function(S,H,U,invert=FALSE) {
  # assumes that priors are flat
  ns = dim(S)[1]
  if (!invert){ 
    return(1/ns * (sum(sapply(1:ns, function(t) sum(sapply(1:2, function(m) sum(sapply(1:ns, function(t2) S[t,m]*H[m,t2]*U[t,t2])) )))))) 
  } else{
    return(max(expected.utility(S,H,U), 
               expected.utility(S,H[c(2,1),],U)))
  }
}

expected.utility.byIndeces = function(data, i, j){
  # i is sender strat index, j is hearer strat index
  ns = data[i,]$Number.of.states
  states = seq(0,1,length.out = ns)
  tol = data[i,]$Tolerance
  U = get.confusion.matrix(states,tol)
  S = read.speaker.strategy(dataFrame = data, rowIndex = i)
  H = read.hearer.strategy(dataFrame = data, rowIndex = j)
  eu1 = expected.utility(S,H,U)
  eu2 = expected.utility(S,H[c(2,1),],U)
  return(max(eu1,eu2))
}

# Optimal sender & receiver strategy [
#  works ONLY for 2 messages, ns %% 2 == 0 and ns/2 %% 2 == 1,  and flat priors only

optimal.strategies = function(ns) {
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

# utility of optimal sender & receiver strategy

optimalEU = function(ns, alpha){
  states = seq(0, 1, length.out = ns)
  OptStrat = optimal.strategies(ns)
  sen = OptStrat[[1]]
  rec = OptStrat[[2]]
  U = get.confusion.matrix(states,alpha)
  return(expected.utility(sen, rec, U))
}

if (computeEU){
  
  data$Speaker.meanEU = 0
  data$Hearer.meanEU = 0
  range = 1:nrow(data)
  pb <- txtProgressBar(min = 0, max = length(range), style = 3)
  
  for (i in range){
    dsub = subset(data, Impairment == data[i,]$Impairment &
                        Tolerance == data[i,]$Tolerance &
                        Number.of.states == data[i,]$Number.of.states)
    ns = data[i,]$Number.of.states
    states = seq(0,1,length.out = ns)
    alpha = data[i,]$Tolerance
    EUopt = optimalEU(ns,alpha)
    U = get.confusion.matrix(states,alpha)
    sen = read.strategy.byString(String = data[i,]$Speaker.strategy.file)
    rec = read.strategy.byString(String = data[i,]$Hearer.strategy.file)
    data[i,]$Speaker.meanEU = mean(sapply(1:nrow(dsub), function(k) {
                                    expected.utility(sen,
                                                     read.strategy.byString(dsub[k,]$Hearer.strategy.file),
                                                     U, invert = TRUE) })) / EUopt
    data[i,]$Hearer.meanEU = mean(sapply(1:nrow(dsub), function(k) {
      expected.utility(read.strategy.byString(dsub[k,]$Speaker.strategy.file),
                       rec,
                       U, invert = TRUE) })) / EUopt  
    setTxtProgressBar(pb, i)
  }
  
  close(pb)
  write.csv(data, paste("~/Desktop/data/svn/vagueness-games/snippets/exploring_uniformity_from_impairment/dataSec",Sys.time() , ".csv", sep = "", collapse = ""))
} else{
  data = read.csv("~/Desktop/data/svn/vagueness-games/snippets/exploring_uniformity_from_impairment/dataSec.csv")
}



meanEUs = ddply(data,
                   .(Number.of.states, Impairment, Tolerance), 
                   summarise, 
                   Speaker.meanEU = mean(Speaker.meanEU),
                   Hearer.meanEU = mean(Hearer.meanEU),
                    convexProportion = mean(Speaker.Convex.Cat),
                    meanEU = mean(Expected.utility))

# mean EUs of speaker and hearer strategies are pretty much perfectly aligned
qplot(meanEUs$Speaker.meanEU, meanEUs$Hearer.meanEU)

# it therefore suffices to show only the sender's part

sPlot = ggplot(meanEUs, aes(x=Impairment, y=Speaker.meanEU)) + 
  geom_point() + facet_grid(Number.of.states ~ Tolerance) + geom_line() +
  ylab("average EU against group")

# show(sPlot)

# Combine distance and average Group EU

D$withinGroupEU = meanEUs$Speaker.meanEU
D$individualEU = meanEUs$meanEU
D$convexProportion = meanEUs$convexProportion

Dmelt = melt(D, id.vars = c("Number.of.states", "Impairment", "Tolerance"))

combPlot = ggplot(Dmelt, aes(x=Impairment, y=value, color = variable)) + 
  geom_point() + facet_grid(Number.of.states ~ Tolerance) + geom_line()

# show(combPlot)



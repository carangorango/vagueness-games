computeD == FALSE

data = read.csv('~/Desktop/data/svn/vagueness-games/results/20140918-142408.varTolerance.csv', 
                colClasses=c('numeric','factor','numeric','numeric','numeric',
                             'factor','numeric','numeric','numeric','numeric',
                             'numeric','numeric','numeric','numeric','numeric',
                             'numeric','numeric','numeric','character','character'))

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

# Hellinger distance.

HD = function(x, y){
  return( sqrt(sum(sapply(1:length(x), function(i) (sqrt(x[i]) - sqrt(y[i]))^2  )) ) / (sqrt(2)) )
}

# Distance between two strategis as Hellinger distances at each choice point.

strategy.distance = function(P,Q){
  nc = dim(P)[1]
  sum(sapply(1:nc, function(x) return(HD(P[x,], Q[x,]) ) ) ) / nc 
}

# Reading a strategy.

read.speaker.strategy = function(dataFrame = data, rowIndex){
  speaker.filename = paste("~/Desktop/data/svn/vagueness-games/", 
                           dataFrame[rowIndex,]$Speaker.strategy.file, sep="",col="")
  speaker <- prop.table(as.matrix(read.csv(speaker.filename, header=FALSE, colClasses='numeric')),1)
  return(as.matrix(speaker))
}

read.speaker.strategy.byString = function(String){
  speaker.filename = paste("~/Desktop/data/svn/vagueness-games/", 
                           String, sep="",col="")
  speaker <- prop.table(as.matrix(read.csv(speaker.filename, header=FALSE, colClasses='numeric')),1)
  return(as.matrix(speaker))
}

read.hearer.strategy = function(dataFrame = data, rowIndex){
  hearer.filename = paste("~/Desktop/data/svn/vagueness-games/", 
                           dataFrame[rowIndex,]$Hearer.strategy.file, sep="",col="")
  hearer <- prop.table(as.matrix(read.csv(hearer.filename, header=FALSE, colClasses='numeric')),1)
  return(as.matrix(hearer))
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
  S1 = read.speaker.strategy.byString(String1)
  S2 = read.speaker.strategy.byString(String2)
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


# Show that this works on two strategies that have 'reversed message use'.

i = 3504
j = 3505
show(arrangeGrob(plot.language.byindex(data,i), plot.language.byindex(data,j)))
show(speaker.strategy.distance(data,i,j))
show(hearer.strategy.distance(data,i,j))

# get average distance in a vector of strategies

speaker.vector.distance = function(Svec){
  ns = length(Svec)
  D = 0
  for (i in 1:(ns-1)){
    for (j in (i+1):ns){
      d = speaker.strategy.distance.ByString(Svec[i],Svec[j])
      D = c(D,d)
    }
  }
  return(mean(D[-1]))
}

# test this:

d = subset(data, Tolerance == 0.2 & Impairment == 0 & Number.of.states == 6)
Svec = d$Speaker.strategy.file
show(speaker.vector.distance(Svec))

# compute distances for speaker strategies

ds = data[,c(1,4,5,19)] # only relevant "data" is speaker strategy file name
# ds = subset(ds,Number.of.states == 50 & Impairment == 0 & Tolerance <= 0.3)
dm = melt(ds,id.vars = c("Number.of.states", "Impairment", "Tolerance")) # melted data

if (computeD == TRUE){
  D = ddply(dm, .(Number.of.states, Impairment, Tolerance), summarise, 
            inGroupDistance = speaker.vector.distance(value))
}
else{
  D = read.csv("~/Desktop/data/svn/vagueness-games/snippets/exploring_uniformity_from_impairment/D.csv")
}

pd <- position_dodge(.01)
sp = ggplot(D, aes(x=Impairment, y=inGroupDistance)) + 
  geom_point(position = pd) + geom_line()
sp + facet_grid(Number.of.states ~ Tolerance, scales="free")

# compute average EU between different strategies from the same parameter triple

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

expected.utility = function(S,H,U,states) {
  # assumes that priors are flat
  return(1/ns * (sum(sapply(1:ns, function(t) sum(sapply(1:2, function(m) sum(sapply(1:ns, function(t2) S[t,m]*H[m,t]*U[t,t2])) )))))) 
}

expected.utility.byIndeces = function(data, i, j){
  # i is sender strat index, j is hearer strat index
  ns = data[i,]$Number.of.states
  states = seq(0,1,length.out = ns)
  tol = data[i,]$Tolerance
  U = get.confusion.matrix(states,tol)
  S = read.speaker.strategy(dataFrame = data, rowIndex = i)
  H = read.hearer.strategy(dataFrame = data, rowIndex = j)
  eu1 = expected.utility(S,H,U,states)
  eu2 = expected.utility(S,H[c(2,1),],U,states)
  return(max(eu1,eu2))
}

i = 1
j = 2
show(arrangeGrob(plot.language.byindex(data,i),plot.language.byindex(data,j)))
show(expected.utility.byIndeces(data, i, j))

data$rowIndex = 1:nrow(data)
data$meanEUinGroup = rep(0,nrow(data))

for (i in 3501:3550){
  dsub = subset(data, Impairment == data[i,]$Impairment &
                Tolerance == data[i,]$Tolerance &
                Number.of.states == data[i,]$Number.of.states)
  data[i,]$meanEUinGroup = mean(sapply(dsub$rowIndex, function(j) expected.utility.byIndeces(data,i, j)))
}

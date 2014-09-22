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

D = ddply(dm, .(Number.of.states, Impairment, Tolerance), summarise, 
            inGroupDistance = speaker.vector.distance(value))

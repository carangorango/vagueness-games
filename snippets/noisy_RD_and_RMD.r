n.s = 2
n.m = 2

C = matrix(c(.8,.2,.2,.8),nrow=n.s)
C = prop.table(C,1)
rownames(C) = 1:n.s
colnames(C) = 1:n.s

pureS = rep("d",n.m^n.s)
c = 1
for (i in 1:n.s){
  for (j in 1:n.m){
    pureS[c] = paste(i,j,sep="")
    c = c+1
  }
}

Q = matrix(0,nrow=length(pureS), ncol=length(pureS))
colnames(Q) = pureS
rownames(Q) = pureS

for (i in 1:dim(Q)[1]){
  s1 = strsplit(rownames(Q)[i],split="")[[1]]
  for (j in 1:dim(Q)[2]){
    s2 = strsplit(colnames(Q)[j],split="")[[1]]
    x = prod( sapply(1:n.s, function(t) sum(sapply(1:n.s, function(t2) ifelse(s2[t] == s1[t2], C[t,t2], 0 ) ) ) ) )
    Q[i,j] = x
  }
}

show(Q)

mixed2behavioral = function(mixedS,pureS,n.s,n.m) {
  b = matrix(0,n.s,n.m)
  rownames(b)=1:n.s
  colnames(b)=1:n.m
  for (i in 1:n.s){
    for (j in 1:n.m){
      b[i,j] = sum( sapply(1:length(pureS), function(p) ifelse(strsplit(pureS[p],split="")[[1]][i]==j ,mixedS[p] ,0)) ) 
    }
  }
  return(b)
}

mixedS = c(.24,.56,.06,.14)
mixedS = c(1/3,1/3,1/3,0)
mixedS = c(2/3,0,1/3,0)


# show(mixed2behavioral(c(.24,.56,.06,.14), pureS,n.s,n.m))
# show(mixed2behavioral(c(.2,.6,.1,.1), pureS,n.s,n.m))

mutate = function(mixedS,Q){
  m = rep(0,length(mixedS))
  for (i in 1:length(mixedS)){
    m[i] = sum(sapply(1:length(mixedS), function(j) Q[j,i] * mixedS[j]))
  }
  return(m)
}

mut = mutate(mixedS,Q) 
show(mut)
show(mixed2behavioral(mut,pureS,n.s,n.m))

perturbe = function(b,C){
  return(b %*% t(C))
}

b = matrix(c(2/3,1/3,
             2/3,1/3),nrow=2,byrow=T)
rownames=1:n.s
colnames=1:n.s

show(perturbe(b,C))
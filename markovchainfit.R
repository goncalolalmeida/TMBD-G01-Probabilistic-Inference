library(markovchain)
#getting from matrix / data.frame
data(holson) #load a data.frame (also it works with matrices)
head(holson) #load a matrix of pop * time observations
data<-read.csv("Covid19stateTransition.csv")
singleMc<-markovchainFit(data=data,name="covid19") #fit the MC
P<-singleMc$estimate@transitionMatrix
P
round(P,2)
#getting from list

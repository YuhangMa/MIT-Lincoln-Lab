speeds <- read.table('car-speeds.csv', 
  sep=",", header=TRUE
  )



subset(speeds, State=='Utah')

moments <- function(vec){
  mm <- mean(vec)
  ll <- sd(vec)
  n=length(vec)
  ret <- data.frame(mean=mm, sd=ll, nn = n)
  return(ret)
}





speed_summary2 <- ddply(speeds, c('Color'), function(vec){
  moments(vec$Speed)
})

speed_summary3 <- ddply(speeds, c('State'), function(vec){
  moments(vec$Speed)
})




library(lattice)
summary(speeds)
histogram(~Speed|State, speeds)
histogram(~Speed|State*Color, speeds)


install.packages('latticeExtra')
library(latticeExtra)
useOuterStrips(
  densityplot(~Speed|State*Color, speeds)
)


myfun<-function(i)
{
  rr <- rnorm(10, mean=i,sd=1)
}

a <- matrix(nrow=10, 
   ncol=10)

b<-seq(1:10)
b

myfun(b)

c<-ldply(b,myfun)

### A differnt way

d <-ldply(1:10, function(x) {
  rnorm(10, x)}
)


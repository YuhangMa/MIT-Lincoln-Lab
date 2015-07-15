speeds <- read.table('car-speeds.csv', 
  sep=",", header=TRUE
)

## mean / sd of cars in utah by color
subset(speeds, State=='Utah')

moments <- function(vec) {
  mm <- mean(vec)
  ll <- sd(vec)
  ret <- data.frame(mean=mm, sd=ll)
  return(ret)
}

speed_summary <- ddply(
  speeds, c('Color','State'), function(df){
    moments(df$Speed)
})

## next step:
## summarize by just color
## then add n=length(vec) to moments function


library(lattice)
summary(speeds)
histogram(~Speed|State, speeds)
## ugly
histogram(~Speed|State*Color, speeds)
## less ugly
## don't do this now
install.packages('latticeExtra')
library(latticeExtra)
useOuterStrips(
  densityplot(~Speed|State*Color, speeds)
)

## use ldply to make a data.frame
## that has 10 draws of rnorm each
## for mean = 1:10
## then use bwplot to plot results
## bonus for 
## *indentation
## *useful variable names
## * useful comments

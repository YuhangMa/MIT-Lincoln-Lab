## Looking at car speed data and random samples with different means

## Car speeds
speeds <- read.table('car-speeds.csv', sep=",", header=TRUE)
utahcars <- subset(speeds,State=='Utah')

# mean, standard dev, and length
moments <- function(thedata) {
  mm <- mean(thedata)
  sd <- sd(thedata)
  n <- length(thedata)
  return(data.frame(mean=mm,sd=sd,length=n))
}

# find mean, stdev, and # of utah cars
moments(utahcars$Speed)

library(plyr)

# split by color and state, find the moments of each combination
speed_summary <- ddply(
  speeds, c('Color','State'), function(df) {
    moments(df$Speed)
  }
)
# split by color, find the moments of each
speed_summary2 <- ddply(
  speeds, c('Color'), function(df) {
    moments(df$Speed)
  }
)
# different types of plotting
library(lattice)
summary(speeds)
histogram(~Speed|State,speeds)# y~x|conditional
histogram(~Speed|State*Color,speeds)
library(latticeExtra)
useOuterStrips(histogram(~Speed|State*Color,speeds))
useOuterStrips(densityplot(~Speed|State*Color,speeds))


## advanced -- use ldply to make a data.frame that has 10 draws of rnorm each for mean=1:10
## then use bwplot to plot results
## bonus points: *indentation, useful variable names, comments

mean <- (1:10)
# create long x 2 list of mean,sample
data <- ldply(mean,
  function(x){
    data.frame(mean=x,draw=rnorm(10,mean=x))
  }
)
# box-and-whisper plot
bwplot(mean~draw,data)

# matrix form - doesn't work with lattice
mean <- (1:10)
data <- ldply(mean,
  function(x){
    rnorm(10,mean=x)
  }
)


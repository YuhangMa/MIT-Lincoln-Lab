speeds <- read.table('car-speeds.csv', sep = ",", header = TRUE)

## mean / sd of cars in Utah by color

moments <- function(vec) {
  mvec <- mean(vec)
  sdvec <- sd(vec)
  lenvec <- length(vec)
  ret <- data.frame(mean = mvec,sd = sdvec, length = lenvec)
  return(ret)
}

speed_summary <- ddply(speeds, c('Color', 'State'), function(df){moments(df$Speed)})

library(lattice)
histogram(~Speed|State, speeds)

library(latticeExtra)
useOuterStrips(histogram(~Speed|State*Color, speeds))
useOuterStrips(densityplot(~Speed|State*Color, speeds))

## use ldply to make a dataframe that has 10 draws of normal distn
## each w/ mean = 1:10 then use bwplot to plot results

generate <- function(m,n = 10){
  x <- data.frame(mean = m, draw = rnorm(n, mean = m))
  return(x)
}
data <- ldply((1:10), generate)
bwplot(mean~draw, data)
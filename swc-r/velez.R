## This is not very interesting
## draw from 2 distributions
## number of draws (samples)
nn <- 50
v1 <- rnorm(50)
v2 <- rexp(50)
plot(v1,v2)
plot(v2,v1)
plot(v1,v2)
plot(v1,v2,main = "v1 vs. v1")
v3 <-rnorm(100, mean=10, sd = 0.1)
hist(v3,xlab = "grams")

speeds <- read.table ('car-speeds.csv', sep = ',', header = TRUE)

subset(speeds, State =='Utah'& Color=='White')

moments <-function(vec){
  mm <-mean (vec)
  ll <-sd(vec)
  ret <- data.frame(mean=mm, sd=ll)
  return(ret)
}

#To marginalize by color
speed_summary <- ddply(
  speeds, c('Color','State'), function(df){
  moments(df$Speed)
})

##next step
#Summarize by just color, 
#then add n =length(vec) to moments function

moments2 <-function(vec){
  mm <-mean (vec)
  ll <-sd(vec)
  ret <- data.frame(n=length(vec),mean=mm, sd=ll)
  return(ret)
}

speed_summary2 <- ddply(
  speeds, c('Color'), function(df){  #marginalize by colors in the speeds structure
    moments2(df$Speed)  #df: dataframe -->creates a new table, showing the mean, sd and number of cars (comes from the moments 2 function)
  })


library(lattice)
summary(speeds)

histogram(~Speed|State,speeds)
histogram(~Speed|State*Color,speeds)


install.packages('latticeExtra')

library('latticeExtra')
useOuterStrips(
  densityplot(~Speed|State*Color, speeds)
)



## Use ldply to make a data.frame
## that has 10 drws of rnorm each
## for mean = 1:10
## then use bwplot to plot results


meanDraws <-function(mean2){
  v4 <- rnorm(10, mean = mean2)
  ret <- data.frame(mean = mean2, v4)
  return(ret)
}

summary2 <- ldply(1:10, meanDraws)
  
bwplot(~v4|mean, summary2) ## plot of the mean draws




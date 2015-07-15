# THIS FILE DOES NOT HAVE MUCH USE SINCE PACKAGES WOULD NOT INSTALL :)

# draw from 2 distributions normal and exponential; 50 observations each

#a<-rnorm(5)
#b<-1:5

#v1<-rnorm(50)
#v2<-rexp(50)
#v1
#plot(v1,v2)
#plot(v2,v1, main="Title goes here")

# histogram of 100 draws from normal  mean 10 sd of 0.1 with x-axis labeled
#a<-rnorm(
#  100,
#  mean=10,
#  sd=0.1)
#hist(a, main = "Histogram of", xlab = 'here')


speeds<- read.table('car-speeds.csv', sep=",", header=TRUE)
dim(speeds)
summary(speeds)
str(speeds) # tells you the structure of the data
speeds$State
subset(speeds, State=='Colorado')
Utah<-subset(speeds, State=='Utah')
WhiteUtah<-subset(Utah, Color=='White')
mean(WhiteUtah$Speed)
sd(WhiteUtah$Speed)

Utah<-subset(speeds, State=='Utah')
RedUtah<-subset(Utah, Color=='Red')
mean(RedUtah$Speed)
sd(RedUtah$Speed)

Utah<-subset(speeds, State=='Utah')
BlueUtah<-subset(Utah, Color=='Blue')
mean(BlueUtah$Speed)
sd(BlueUtah$Speed)

Utah<-subset(speeds, State=='Utah')
BlackUtah<-subset(Utah, Color=='Black')
mean(BlackUtah$Speed)
sd(BlackUtah$Speed)

cbind(mean(WhiteUtah$Speed),
      sd(WhiteUtah$Speed),mean(RedUtah$Speed),
      sd(RedUtah$Speed),mean(BlueUtah$Speed),
      sd(BlueUtah$Speed),mean(BlackUtah$Speed),
      sd(BlackUtah$Speed))

moments<-function(vec){
  mu <-mean(vec)
  sigma <-sd(vec)
  ret <-data.frame(mean=mu,sd=sigma)
  return(ret)
}
moments(subset(speeds,State=='Utah')$Speed)
install.packages('plyr')
speed_summary<-ddply(speeds, c('Color', 'State'), function(df){moments(df$Speed)})

library(lattice)
summary(speeds)
histogram(~Speed|Color, speeds)

histogram(~Speed|State, speeds)

histogram(~Speed|Color*State, speeds) # Maybe too many plots? :)

install.packages('latticeExtra')
library(latticeExtra)

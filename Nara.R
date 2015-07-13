## This is not very interesting
## draw from 2 distributions
##
nn<-50
v1<-rnorm(nn)
v2<-rexp(nn)
plot(v1,v2)
plot(v2,v1,main="title")


#100 from normal(mean=10,sd=.01) with x-axis label
v3<-rnorm(100, mean = 10, sd = .01)
hist(v3,xlab="N(10,.1)")

hist(rnorm(100, mean = 10, sd = .01),xlab="N(10,.1)")

#next excercise
speeds<-read.table('car-speeds.csv',sep=",",header=TRUE)

#find mean/sd speed of each color of cars in Utah

utah.speeds<-subset(speeds,State=='Utah')
utah.black<-subset(utah.speeds,Color=='Black')
utah.blue<-subset(utah.speeds,Color=='Blue')
utah.red<-subset(utah.speeds,Color=='Red')
utah.white<-subset(utah.speeds,Color=='White')

#mean/sd speed of Utah cars
moments <- function(vec){
  mm<-mean(vec)
  ll<-sd(vec)
  ret<-data.frame(mean=mm,sd=ll) #return
  return(ret)
}

moments(subset(speeds,State=='Utah')$Speed)

#find mean/sd speed of each color/state of cars
install.packages('plyr')
library(plyr)

speed_summary<-ddply(
  speeds,c('Color','State'),function(df){
    moments(df$Speed)
})

#summarize by just color, then add n=length(vec) to moments function

moments2 <- function(vec){
  mm<-mean(vec)
  ll<-sd(vec)
  ret<-data.frame(n=length(vec),mean=mm,sd=ll) #return
  return(ret)
}

speed_summary2<-ddply(
  speeds,'Color',function(df){
    moments2(df$Speed)
  })

library(lattice)
summary(speeds)
histogram(~Speed|State, speeds)
histogram(~Speed|State*Color, speeds)
##don't do this now
install.packages('latticeExtra')
library(latticeExtra)
useOuterStrips(histogram(~Speed|State*Color, speeds))
useOuterStrips(densityplot(~Speed|State*Color, speeds))

#use ldply to make a data.frame
#that has 10 draws of rnorm each
#for mean=1:10
#then use bwplot to plot results
#bonus for indentation, useful variable names, comments
rnorm.mean<-function(mm){
  rand =  rnorm(10,mean=mm)
  rt<-data.frame(mean=mm, rand)
  return(rt)
} #10 rnorm sample generator given mean=mm

data.frame1<-ldply(1:10,rnorm.mean)
bwplot(~rand|mean,data.frame1)


#mkdir swc-r
#git mv *.R swc -r
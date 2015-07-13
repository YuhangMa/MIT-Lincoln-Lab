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

## Draw from 2 distributions
nn <- 50 # number of draws
v1 <- rnorm(nn)
v2 <- rexp(nn)
plot(v1,v2,main="v1 vs v2")
plot(v2,v1)
# historgram
v3 <- rnorm(100,mean=10,sd=0.1)
hist(v3,xlab="sample value")
#hist(rnorm(100,mean=10,sd=0.1),xlab="sample value")

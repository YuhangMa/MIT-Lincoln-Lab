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


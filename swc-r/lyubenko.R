# draw from 2 distributions normal and exponential; 50 observations each

a<-rnorm(5)
b<-1:5

v1<-rnorm(50)
v2<-rexp(50)
v1
plot(v1,v2)
plot(v2,v1, main="Title goes here")

# histogram of 100 draws from normal  mean 10 sd of 0.1 with x-axis labeled
a<-rnorm(
  100,
  mean=10,
  sd=0.1)
hist(a, main = "Histogram of", xlab = 'here')

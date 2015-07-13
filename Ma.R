## This is only a test file.
## Get a histogram of 100 draws from a normal distribution w/ mean 
## of 10 and sd of 0.1 and meaningful x-axis

v <- rnorm(100, mean = 10, sd = 0.1)
hist(v, xlab = 'population')

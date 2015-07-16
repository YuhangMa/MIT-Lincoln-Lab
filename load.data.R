## data downloaded from 
## http://apps.who.int/gho/data/node.ebola-sitrep.quick-downloads?lang=en
## saved csvs in dir data with name "cases.countryname.csv"
##
library(plyr)
## names of all data files
.files <- dir('data', patt='cases.*.csv')
## read each file
## combine into one data.frame
cases <- ldply(.files, function(.file) {
    .fullname <- paste0('data/',.file)
    ret <- read.table(.fullname, header=T, sep=',')
    return(ret)
})

## helper scripts
source("mk.helpers.R")
## load packages, installing if needed
load_install('simecol')
load_install('tidyr')
load_install('ggplot2')

## list to store everything in
sir <- list()

## main model, simecol object
sir$mod <- new("odeModel",
    ## transition function
    main = function(time, state, pars) {
        ## sum state vector
        N <- sum(state)
        with(as.list(state), {
            ## first compute flows/transitions
            infect <- (pars['beta']*S*I)/N
            recover <- (pars['gamma']*I)
            ## then compute state deltas from flows
            dS <- -infect 
            dI <- infect - recover
            dR <- recover
            ## finally, return deltas as list
            ## for solver
            list(c(dS, dI, dR))
        })
    },
    ## add any equations needed above 
    equations = list(
        f = function(x, y, k) { x*y }
    ),
    ## parameterized per day
    parms = c(
        beta = 0.1, ## contact rate, 
        gamma = 0.05 ## per day
    ),
    ## time points to evaluate system at
    times = seq(1, 300, 1),
    ## initial conditions
    init = c(S=1e3, I=5, R=0),
    solver = "lsoda"
)

## simulate! results stored in model object
sir$mod <- sim(sir$mod)

## simulation results stored in
## slot 'out' in list member 'mod' in list sir
## see str(sir$mod) for details
sir$result <- as.data.frame(sir$mod@out)
## use tidyr to reshape for lattice 
sir$result <- gather(
    data=sir$result, key='state', value='value', -time
)


sir$plot.ts <- { 
    ggplot(sir$result,
        aes(x=time, y=value, color=state)
    ) + 
    geom_line() +
    xlab('Days') + ylab('Individuals') +
    ## plotting options, see ?theme and ?theme_bw
    #theme_bw() +
    theme(legend.position=c(x=0.95,y=0.90))
}
    

plot(sir$plot.ts )

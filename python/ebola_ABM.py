import random
import matplotlib.pyplot as plt
import copy
import numpy as np
from person import person
from colors import colors
from city import city

statetonum = {'S':0, 'E':1, 'I':2, 'H':3, 'F':4, 'R':5, 'D':6}
numtostate = {0:'S', 1:'E', 2:'I', 3:'H', 4:'F', 5:'R', 6:'D'}
# IDEAS:
# could count number infected via funeral vs family vs community
# could track number of days until no more 'I' class (disease is dead)
# check rates of different countries
# more countries, etc.
# come up with references for funeral size, etc. to validate our parameters

class ebola:
    def __init__(self, width = 70, height = 70, days = 500, pop_size = 1000, var = [], density = []):
        self.width = width      # width of map
        self.height = height    # height of map
        self.days = days        # number of days to simulate
        self.pop_size = pop_size # population size
        self.num_cities = len(var)
        self.city_den = copy.deepcopy(density)
        
        self.grid = [[[] for j in range(self.width)] for i in range(self.height)] # store list of population indices at each grid cell
        self.grid_home = [[[] for j in range(self.width)] for i in range(self.height)]
        self.pop = [person() for i in range(self.pop_size)]
        self.cities = [city(self.width, self.height, var[i], density[i]) for i in range(self.num_cities)]
        #for i in range(self.num_cities):
        #    print self.cities[i].loc.x, self.cities[i].loc.y
        self.R = [0 for i in range(self.pop_size)]
        self.repro = 0
        
        # TODO: list of probabilities - maybe change this?
        self.travel_prob = 0.2
        self.home_prob = 0.5        # chance go home each timestep
        self.non_local_prob = 0.5   # chance for non-local travel
        self.fam_size_a = 3
        self.fam_size_b = 6
        # CONTACT RATES
        self.b_fam = 0.1
        self.b_com = 0.006
        self.b_fun = 0.2          # funeral contact rate
        # PROBABILITIES
        self.i_mortality = 0.5
        self.h_prob = 0.233 #0.248 
        self.h_mortality = 0.5
        # TIMEOUTS
        self.incubation_time = 11
        self.i_death_time = 8   # use random timeout, [7,9]
        self.i_death_time_a = 7
        self.i_death_time_b = 9
        self.funeral_time = 2.01    # use constant, 2
        self.funeral_time_c = 2
        self.r_time = 10            # use constant, 15
        self.pre_h_time = 4.5 #4.6      # use random timeout, 1-5
        self.pre_h_time_a = 3
        self.pre_h_time_b = 6
        self.h_recover_time = 5.5 # use random timeout, 13-18
        self.h_recover_time_a = 5
        self.h_recover_time_b = 6
        self.h_death_time = 3.51   # use random timeout, 8-12
        self.h_death_time_a = 3
        self.h_death_time_b = 4
        
        # count number infected in each way
        self.funeral_count = 0
        self.family_count = 0
        self.comm_count = 0
        self.numberoffunerals = 0
        self.num = [0 for i in range(7)]
        # total number in each state SEIHRFD
        for i in range(7):
            if i == 0:
                self.num[i] = self.pop_size
            else:
                self.num[i] = 0
        self.numlist = [[] for i in range(7)]
    
    # functions to increment/decrement number in each state (to clean up code)
    def get_community(self, indiv):
        return self.cities[indiv.community]

    def updatenum(self, pre, post):
        self.num[statetonum[pre]] -= 1
        self.num[statetonum[post]] += 1

    def updatethelists(self):
        for i in range(7):
            self.numlist[i].append(self.num[i])
        
    # distribute the population throughout the map
    def populate(self): ## NOT SETTING 0'S FAMILY
        i = 0
        while i < self.pop_size:           
            # family head establishes family location and such
            which_city = random.random()   # first individual decides whether which city
            temp = 0
            while(sum(self.city_den[0:temp+1]) < which_city):
                temp += 1
            family_num = random.randint(self.fam_size_a, self.fam_size_b)

            # initialize all of family's lists of family members
            for j in range(i, min(i+family_num, self.pop_size)): # TODO: index off by 1?
                self.pop[j].index = j
                self.pop[j].community = temp
                self.pop[j].home_community = temp
                    
                if j != i:
                    self.pop[j].home.copy(self.pop[i].home)
                else:
                    self.pop[j].home.gen_pos(self.get_community(self.pop[i]), self.width, self.height)

                self.pop[j].pos.copy(self.pop[j].home)
                self.pop[j].family = range(i, min(i+family_num,self.pop_size))
            
            self.grid_home[int(self.pop[i].home.x)][int(self.pop[i].home.y)].extend(range(i, min(i+family_num, self.pop_size)))
            self.grid[int(self.pop[i].home.x)][int(self.pop[i].home.y)].extend(range(i,min(i+family_num,self.pop_size)))

            i = i + family_num

    # movement of a healthy or exposed individual
    def travel(self, indiv):
        self.grid[int(indiv.pos.x)][int(indiv.pos.y)].remove(indiv.index) # remove self from grid
        temp = random.random() # will he go home?
        if temp < self.home_prob and not(indiv.is_home):      # go home with 50% chance
            indiv.pos.copy(indiv.home)
            indiv.is_home = True
            indiv.community = indiv.home_community
        else:
            temp = random.random()
            if temp < (1-self.city_den[indiv.community])/2:  #self.non_local_prob:    # non-local travel, change community
                which_city = random.random()  # make sure you don't travel to same city
                temp_densities = copy.deepcopy(self.city_den)
                temp_densities.pop(indiv.community)
                temp = 0
                # error checking: if temp = num_cities -1, indiv goes to last city
                while(sum(temp_densities[0:temp+1])/(1-self.city_den[indiv.community]) < which_city):
                    temp += 1
                if temp >= indiv.community: # adjust for index
                    temp += 1

                indiv.community = temp
                
            indiv.pos.gen_pos(self.get_community(indiv), self.width, self.height)
            indiv.is_home = False

        # put self back on grid
        self.grid[int(indiv.pos.x)][int(indiv.pos.y)].append(indiv.index)


    def susceptible(self, indiv):
        temp = random.random()
        if temp < self.travel_prob:
            self.travel(indiv)


    def exposed(self, indiv):
        if random.random() < self.travel_prob:
            self.travel(indiv)
        if indiv.timeout == 0:
            indiv.state = 'I'
            self.updatenum('E','I')
            temp = random.random()
            if temp < self.h_prob:
                indiv.will_h = True
                indiv.timeout = random.randint(self.pre_h_time_a, self.pre_h_time_b) # pre-hospital period
            elif temp < self.h_prob + (1-self.h_prob)*self.i_mortality:
                indiv.will_die = True
                indiv.timeout = random.randint(self.i_death_time_a, self.i_death_time_b) # infected death period
            else:
                indiv.will_die = False
                indiv.timeout = self.r_time # infected recovery period
        else:
            indiv.timeout = indiv.timeout - 1
            
            
    def infect(self, indiv):
        tempx = int(indiv.pos.x) # is this linking or copying?
        tempy = int(indiv.pos.y)
        nearx = [x+tempx for x in [-1,0,1]]
        neary = [x+tempy for x in [-1,0,1]]
        for x in nearx:
            for y in neary:
                # check grid bounds
                if (x >= 0 and x < self.height and y >= 0 and y < self.width):
                    # propagate infection in each grid cell
                    for z in self.grid[x][y]:
                        if (indiv.family) and (self.pop[z].index in indiv.family) and (self.pop[z].state == 'S'): # within grid
                            #print 'im a family member'
                            if random.random() < self.b_fam: # family member
                                self.R[indiv.index] += 1
                                self.family_count += 1
                                self.pop[z].state = 'E'
                                self.pop[z].timeout = self.incubation_time
                                self.updatenum('S','E')
                        elif self.pop[z].state == 'S':
                            if random.random() < self.b_com: # community member
                                self.R[indiv.index] += 1
                                self.comm_count += 1
                                self.pop[z].state = 'E'
                                self.pop[z].timeout = self.incubation_time
                                self.updatenum('S','E')


    def infected(self, indiv):
        self.infect(indiv)
        if indiv.will_h and indiv.timeout == 0:
            indiv.state = 'H'
            self.updatenum('I','H')
            if random.random() < self.h_mortality:
                indiv.will_die = True
                indiv.timeout = random.randint(self.h_death_time_a, self.h_death_time_b) # hospital death period
            else:
                indiv.will_die = False
                indiv.timeout = random.randint(self.h_recover_time_a, self.h_recover_time_b) # hospital recovery period
        elif indiv.will_die and indiv.timeout == 0:
            indiv.state = 'F'
            indiv.timeout = self.funeral_time_c
            self.updatenum('I','F')
            self.funeral(indiv)
        elif indiv.timeout == 0: # will_die = False
            indiv.state = 'R'
            self.updatenum('I','R')
        else: # timeout != 0
            indiv.timeout = indiv.timeout - 1
         
#
    def hospitalized(self, indiv):
        # will_die determined by infect on initial hospitalization
        # TODO: infect people in hospital? no?
        if indiv.timeout == 0: # die or recover
            if indiv.will_die:
                indiv.state = 'D'
                self.updatenum('H','D')
            else:
                indiv.state = 'R'
                self.updatenum('H','R')
        else:
            indiv.timeout = indiv.timeout - 1


    def funeral(self, indiv):
        self.numberoffunerals += 1
        # remove self from grid, change grid index, change pos to home            
        self.grid[int(indiv.pos.x)][int(indiv.pos.y)].remove(indiv.index)
        indiv.pos.copy(indiv.home)
        self.grid[int(indiv.pos.x)][int(indiv.pos.y)].append(indiv.index)
        indiv.is_home = True
        indiv.community = indiv.home_community
        # return healthy family members home
        
        for i in indiv.family:
            if self.pop[i].state in ('S', 'E', 'R'):
                self.grid[int(self.pop[i].pos.x)][int(self.pop[i].pos.y)].remove(self.pop[i].index)
                self.pop[i].pos.copy(self.pop[i].home)
                #self.pop[i].grid_index = len(self.grid[int(self.pop[i].pos.x)][int(self.pop[i].pos.y)])
                self.grid[int(self.pop[i].pos.x)][int(self.pop[i].pos.y)].append(self.pop[i].index)
                self.pop[i].is_home = True
                self.pop[i].community = self.pop[i].home_community
        # infect people if current location is close to initial location...
        tempx = int(indiv.pos.x)
        tempy = int(indiv.pos.y)
        for z in self.grid[tempx][tempy]:
            # check for original neighbors who are still nearby (including family)
            if int(self.pop[z].home.x) == tempx and int(self.pop[z].home.y) == tempy and self.pop[z].state == 'S':
                if random.random() < self.b_fun:
                    self.R[indiv.index] += 1
                    self.funeral_count += 1
                    self.pop[z].state = 'E'
                    self.pop[z].timeout = self.incubation_time
                    self.updatenum('S','E')
        
                
    def funeralized(self, indiv):
        if indiv.timeout == 0:
            indiv.state = 'D'
            self.updatenum('F','D')
        else:
            indiv.timeout = indiv.timeout - 1


    def recovered(self, indiv): # TODO: do we want this?
        if random.random() < self.travel_prob:
            self.travel(indiv)


    def dead(self, indiv):
        # do nothing...
        pass


    def update(self, indiv):
        # check state, do action -- think about order later
        if indiv.state == 'S':
            self.susceptible(indiv)
        elif indiv.state == 'E':
            self.exposed(indiv)
        elif indiv.state == 'H':
            self.hospitalized(indiv)
        elif indiv.state == 'R': # recovered
            self.recovered(indiv)
        elif indiv.state == 'F':
            self.funeralized(indiv)
        elif indiv.state == 'I':
            self.infected(indiv)

    def spatialplot(self, file_name):
        #statetocolor = {'S':'k', 'E':'y', 'I':'r', 'H':'m', 'F':'c', 'R':'g', 'D':'b'}

        legend = colors()
        categories = [[[] for j in range(2)] for i in range(7)]

        fig, ax = plt.subplots(figsize=(10,10))
        for z in self.pop:
            categories[statetonum[z.state]][0].append(random.gauss(z.pos.y,.5))
            categories[statetonum[z.state]][1].append(random.gauss(z.pos.x,.5))

        for i in range(7):
            ax.scatter(categories[i][0], categories[i][1], color = legend.tableau20[i], label = numtostate[i])

        for z in self.cities:
            ax.scatter(z.loc.y, z.loc.x, color='black', marker='*')
#            print z.loc.x, z.loc.y

        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        #red_patch = mpatches.Patch(color='r', label='The red data')
        #plt.legend(handles=[red_patch])
        plt.legend(bbox_to_anchor=(1, 1), loc=2)
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)
        plt.savefig(file_name)

    def curveplot(self, file_name):

        legend = colors()
        fig, ax = plt.subplots(figsize=(16,10))

        for i in range(7):
            plt.plot(range(self.days+1), self.numlist[i], '-', color = legend.tableau20[i], linewidth = 4, label = numtostate[i])

#        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, mode="expand", borderaxespad=0.)
        handles, labels = ax.get_legend_handles_labels()
        lgd = ax.legend(handles, labels, bbox_to_anchor=(1, 1), loc=2)
        ax.set_xlim([0, self.days+1])
        ax.set_ylim([0, self.pop_size])
        ax.set_xlabel("Time")
        ax.set_ylabel("Population")
        plt.rcParams.update({'font.size': 24})
        plt.savefig(file_name, bbox_extra_artists=(lgd,), bbox_inches='tight')
        
    def main(self):
        self.populate()
#        self.spatialplot('distribution_pre.jpg')
#        self.check_density()
#        print self.num
        self.pop[0].state = 'I' # sucks to be you
        self.pop[0].will_h = False
        self.pop[0].will_die = True
        self.pop[0].timeout = random.randint(self.h_death_time_a, self.h_death_time_b)
        self.num[statetonum['S']] -= 1
        self.num[statetonum['I']] += 1
        self.updatethelists()
        system_state = ''
        for t in range(self.days):
            for z in self.pop:
                self.update(z)
                system_state += z.state
            #print system_state
            system_state = ''
            self.updatethelists()
            if t == 30:
#                print '5 R', sum(self.R)/float(self.pop_size - self.R.count(0) + 1)
                #print 'inherent', sum(self.R)/float(self.pop_size - self.num[0] - self.num[1])
                self.repro = sum(self.R)/float(self.pop_size - self.num[statetonum['S']] - self.num[statetonum['E']])
#            print 'current grid at time ', t
#            for i in range(self.pop_size):
#                print 'person ', self.pop[i].index, self.grid[int(self.pop[i].pos.x)][int(self.pop[i].pos.y)]
        print self.family_count, self.comm_count, self.funeral_count
        print self.num
#        print 'R', sum(self.R)/float(self.pop_size - self.R.count(0) + 1)
#        print 'sdfsd', sum(self.R)/float(self.pop_size - self.num[0] - self.num[1])

        self.spatialplot('distribtution.jpg')
        self.curveplot('outbreak.jpg')
            
if __name__ == "__main__":
    numsim = 1
    ##h = [0 for i in range(numsim)]
    ##c = [0 for i in range(numsim)]
    ##f = [0 for i in range(numsim)]
    ##pec_h = 0
    ##pec_c = 0
    ##pec_f = 0
    r = 0
    day = 250
    #nlist = [[0 for j in range(day+1)] for i in range(7)]
    #outbreak = 0.98
    #num_outbreak = 0
    ##frac_inf = [0. for i in range(numsim)]


    #legend = colors()
    #fig, ax = plt.subplots(figsize=(24,15))

    for t in range(numsim):
        ebola_run = ebola(var = [5,1,1], density = [.8,.1,.1], days = day)
    #ebola_run = ebola(var = [20,5], density = [.8,.2])
        ebola_run.main()
        ##h[t] = ebola_run.family_count
        ##c[t] = ebola_run.comm_count
        ##f[t] = ebola_run.funeral_count
        r += ebola_run.repro

        ##if ebola_run.num[statetonum['S']]/float(ebola_run.pop_size) < outbreak:
        ##    sum_inf = ebola_run.family_count + ebola_run.comm_count + ebola_run.funeral_count
        ##    pec_h += ebola_run.family_count/float(sum_inf)
        ##    pec_c += ebola_run.comm_count/float(sum_inf)
        ##    pec_f += ebola_run.funeral_count/float(sum_inf)
        ##   num_outbreak += 1

        ##print 'susceptible percentage:', ebola_run.num[statetonum['S']]/float(ebola_run.pop_size)
        ##frac_inf[t] = 1. - ebola_run.num[statetonum['S']]/float(ebola_run.pop_size)

        #for i in range(7):
        #    if numtostate[i] in ('S', 'D', 'R'):
        #        plt.plot(range(ebola_run.days+1), ebola_run.numlist[i], '-', color = legend.tableau20[i], alpha = 0.2)#, label = numtostate[i])
        
        #if ebola_run.num[statetonum['S']]/float(ebola_run.pop_size) < outbreak:
        #    for i in range(7):
        #        for j in range(day+1):
        #            nlist[i][j] += ebola_run.numlist[i][j]
        #    num_outbreak +=1
        #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, mode="expand", borderaxespad=0.)

    #print the histogram
    ##n, bins, patches = plt.hist(frac_inf, 10, facecolor=legend.tableau20[6])
    ##plt.rcParams.update({'font.size': 42})
    ##plt.xlabel('Fraction of people infected')
    ##plt.ylabel('Number of trials')
    ##plt.axis([0, 1, 0, numsim])
    ##plt.savefig('Histogram.jpg')

    #print the average time series
    #for i in range(7):
    #    for j in range(day+1):
    #        nlist[i][j] = nlist[i][j]/float(num_outbreak)
    #for i in range(7):
    #    if numtostate[i] in ('S', 'D', 'R'):
    #        plt.plot(range(day+1), nlist[i], '-', color = legend.tableau20[i], linewidth = 4, alpha = 1, label = numtostate[i])
    #handles, labels = ax.get_legend_handles_labels()
    #lgd = ax.legend(handles, labels, bbox_to_anchor=(1, 1), loc=2)
    #plt.rcParams.update({'font.size': 24})#presentation:42
    #ax.set_xlim([0, ebola_run.days+1])
    #ax.set_ylim([0, ebola_run.pop_size])
    #ax.set_xlabel("Time")
    #ax.set_ylabel("Population")
    #plt.savefig("Average Time Series.jpg", bbox_extra_artists=(lgd,), bbox_inches='tight')
    #plt.savefig("Average Time Series.jpg")
    
    ##print the stacked bar chart
    ##ind = np.arange(numsim)
    ##width = 0.35
    ##sum_hc = [h[i]+c[i] for i in range(numsim)]
    ##family = plt.bar(ind, h, width, color=legend.tableau20[3])
    ##community = plt.bar(ind, c, width, color=legend.tableau20[5], bottom=h)
    ##funeral = plt.bar(ind, f, width, color=legend.tableau20[6], bottom=sum_hc)
    ##plt.ylabel('Number of People')
    ##plt.xlabel('Trial Number')
    ##plt.xticks(ind+width/2., range(numsim))
    ##plt.legend((family, community, funeral), ('Housholds', 'Communities', 'Funerals'), loc = 'best')
    ##plt.savefig('Stacked Bar Char.jpg')

    #print pec_h/num_outbreak, pec_c/num_outbreak, pec_f/num_outbreak









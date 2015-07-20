import random

from person import person
from city import city

class ebola:
    def __init__(self, width = 500, height = 200, days = 50, pop_size = 3, num_cities = 1, num_villages = 1):
        self.width = width      # width of map
        self.height = height    # height of map
        self.days = days        # number of days to simulate
        self.pop_size = pop_size # population size
        
        self.grid = [[[] for i in range(self.width)] for j in range(self.height)] # store list of population indices at each grid cell
        self.grid_home = [[[] for i in range(self.width)] for j in range(self.height)]
        self.pop = [person() for i in range(self.pop_size)]
        self.cities = [city(self.width, self.height, 20) for i in range(num_cities)]
        
        # list of probabilities
        self.travel_prob = 0.2
        self.home_prob = 0.5 # chance go home each timestep
        self.non_local_prob = 0.1 # chance for non-local travel
        self.fam_size_a = 3
        self.fam_size_b = 6

    
    # distribute the population throughout the map
    def populate(self):
        family_rem = 0   # bookkeeping - keep track of place in family; family members remaining to calculate
        for i in range(self.pop_size):
            self.pop[i].index = i
            if family_rem == 0:         # first individual decides location
                self.pop[i].home.x = random.randint(0,self.height-1) #.gen_pos(self.pop[i].community, self.width, self.height)
                self.pop[i].home.y = random.randint(0,self.width-1)
            else:
                self.pop[i].home = self.pop[i-1].home
            self.pop[i].pos = self.pop[i].home
            self.pop[i].in_city = True

            if family_rem == 0:
                family_rem = random.randint(self.fam_size_a, self.fam_size_b) - 1  # calculate family size (minus one for self) -- fam size is fam_rem + 1
                # initialize all of family's lists of family members
                for j in range(family_rem):
                    if i+j < self.pop_size:
                        self.pop[i+j].family = range(i, min(i+family_rem+1,self.pop_size)).remove(i+j) # may be empty at edge case
            else:
                family_rem = family_rem - 1 # bookkeeping - keep track of place in family
            self.grid_home[int(self.pop[i].home.x)][int(self.pop[i].home.y)].append(i)
            self.grid[int(self.pop[i].home.x)][int(self.pop[i].home.y)].append(i)


    # movement of a healthy or exposed individual
    def travel(self, indiv):
        print self.grid[int(indiv.pos.x)][int(indiv.pos.y)]
        print 'removing ', indiv.index
        self.grid[int(indiv.pos.x)][int(indiv.pos.y)].remove(indiv.index) # remove self from grid
        indiv.pos.x = random.randint(0,self.width-1) #.gen_pos(indiv.community, self.width, self.height)
        # somehow indiv.pos and the grid cell are linked
        # print them
        print 'current grid before adding person ', indiv.index
        for i in range(self.pop_size):
            print self.grid[int(self.pop[i].pos.x)][int(self.pop[i].pos.y)]
        # put individual back in the grid
        self.grid[int(indiv.pos.x)][int(indiv.pos.y)].append(indiv.index)


    def main(self):
        self.populate() # initialize grid
        for t in range(self.days):
            for z in self.pop:
                print 'updating individual ', z.index
                self.travel(z)
            print 'current grid at time ', t
            for i in range(self.pop_size):
                print 'person ', self.pop[i].index, self.grid[int(self.pop[i].pos.x)][int(self.pop[i].pos.y)]

if __name__ == "__main__":
    ebola_run = ebola()
    ebola_run.main()

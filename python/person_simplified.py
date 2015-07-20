from coordinates import coordinates
from city import city

#from sets import Set
#['S', 'E', 'I', 'H', 'R', 'F', 'D'])

class person:
    def __init__(self):
        self.index = 0              # index in the population
        self.home = coordinates()   # initial location
        self.pos = coordinates()    # current location
        self.community = city()     # current city/village
        self.state = 'S'            # current diseased state
#        self.alive = True          # whether he is alive
        self.in_city = True         # if he's in a city (vs village)
        self.timeout = 0            # counting variable
        self.will_die = False       # if hospitalized, will they die?
        self.will_h = False         # if infected, will they go to the hospital?
        self.family = []            # list of family indices
from coordinates import coordinates
#from sets import Set
#['S', 'E', 'I', 'R', 'H', 'F'])

class city:
    def __init__(self, width=1, height=1, var=1, rel_density = 0):
        self.loc = coordinates()                # center of city
        self.loc.gen_city_loc(width, height)    # center of city
        self.var = var                          # variance of population distribution
        self.rel_density = rel_density          # relative density, should be a % of the total population
        
    def copy(self, foreign):
        self.loc.x = foreign.loc.x
        self.loc.y = foreign.loc.y
        self.var = foreign.var
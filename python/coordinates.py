import random

class coordinates:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # generate a city's center location
    def gen_city_loc(self, width, height):
        self.x = random.random()*height
        self.y = random.random()*width

    # generate a position for an individual within a city
    def gen_pos(self, city, width, height):
        while True:
            temp_x = random.gauss(city.loc.x, city.var)
            if temp_x >= 0 and temp_x < height:
                self.x = temp_x
                break

        while True:
            temp_y = random.gauss(city.loc.y, city.var)
            if temp_y >= 0 and temp_y < width:
                self.y = temp_y
                break

    def copy(self, foreign):
        self.x = foreign.x
        self.y = foreign.y
import math
import sympy
import sys
import pickle



class Obstacle:

    def __init__(self, x, y, radius, estimateRadius=None, key=None):
        self.x = x
        self.y = y
        self.radius = radius
        #self.area = math.pi * radius**2
        self.estimateRadius = estimateRadius
        self.key=key
        self.circle = sympy.Circle(sympy.Point(self.x, self.y), radius)

    def same_position(self, obstacle):
        if obstacle.x == self.x and obstacle.y == self.y:
            return True
        return False




import math
import sympy
import sys
import pickle


'''
classe Obstacle per identificare un ostacolo.
x, y: coordinate della posizione dell'ostacolo
radius: raggio dell'ostacolo
estimateRadius: raggio stimato dai robot
key: identificativo dell'ostacolo
'''
class Obstacle:

    def __init__(self, x, y, radius, estimateRadius=None, key=None):
        self.x = x
        self.y = y
        self.radius = radius
        #self.area = math.pi * radius**2
        self.estimateRadius = estimateRadius
        self.key=key
        self.circle = sympy.Circle(sympy.Point(self.x, self.y), radius)





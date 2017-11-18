import sympy
import numpy

'''
classe che tiene traccia delle informazioni riguardo alla tangente
x1, y1: coordinate del punto di partenza della retta
x2, y2: coordinate del punto di intersezione della tangente con la circonferenza
slope: coefficiente angolare della retta tangente
obstacle: oggetto di tipo Obstacle a cui è tangente la retta
'''
class Tangent:
    def __init__(self, x1=None, y1=None, x2=None, y2=None, slape=None, obstacle=None):
        self.x1 = x1
        self.y1 = y1
        self.p1 = sympy.Point(x1, y1)
        self.x2 = x2
        self.y2 = y2
        self.p2 = sympy.Point(x2, y2)
        self.slape = slape
        self.obstacle = obstacle

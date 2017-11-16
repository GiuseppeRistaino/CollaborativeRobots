import sympy
import numpy

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

    def same_slape(self, m):
        if str(m) != 'oo' and str(self.slape) != 'oo':
            if sympy.N(self.slape, 1) == sympy.N(m, 1):
                return True
        return False
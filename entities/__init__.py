from entities.Obstacle import *
from entities.RobotPeer import *

obstacles = []
o1 = Obstacle(0, 0, 1, 1, key=0)
o2 = Obstacle(0, 2, 1, 1, key=1)
o3 = Obstacle(-2, 4, 1, 1, key=2)
o4 = Obstacle(-2, -4, 1, 1, key=3)
obstacles.append(o1)
obstacles.append(o2)
obstacles.append(o3)
obstacles.append(o4)
r = Robot(0, 0, sympy.Point(-8, 0), obstacles, 'r', ("127.0.0.1", 8080))

obs = pickle.dumps(r.obstacles)
print(sys.getsizeof(r))

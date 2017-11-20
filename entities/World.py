from entities.Obstacle import *
from entities.Robot import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle

class World:

    def __init__(self):
        self.obstacles = []
        o1 = Obstacle(0, 0, 1, key=0)
        o2 = Obstacle(0, 2, 1, key=1)
        o3 = Obstacle(-2, 4, 1, key=2)
        #o4 = Obstacle(-2, -4, 1)
        self.obstacles.append(o1)
        self.obstacles.append(o2)
        #self.obstacles.append(o3)
        #self.obstacles.append(o4)

        targetPoint = sympy.Point(8, 0)

        self.r1 = Robot(-2, 3, targetPoint, 'r')
        self.r1.initialize_obstacles(self.obstacles)
        self.r2 = Robot(-5, 0, targetPoint, 'b')
        self.r2.initialize_obstacles(self.obstacles)
        self.r3 = Robot(-7, -1, targetPoint, 'g')
        self.r3.initialize_obstacles(self.obstacles)

        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))

        self.pointRobot_r1, = self.ax.plot([self.r1.x], [self.r1.y], 'ro', lw=1)
        self.pointRobot_r2, = self.ax.plot([self.r2.x], [self.r2.y], 'bo', lw=1)
        self.pointRobot_r3, = self.ax.plot([self.r3.x], [self.r3.y], 'go', lw=1)

        self.r1.start_actions(plt, self.ax, self.pointRobot_r1)
        self.r2.start_actions(plt, self.ax, self.pointRobot_r2)
        self.r3.start_actions(plt, self.ax, self.pointRobot_r3)
        #self.r3.start_actions(plt, self.circles_r3, self.pointRobot_r3)
        #MyThread(self.fig, self.r1, self.ax, self.obstacles, targetPoint).start()
        #MyThread(self.fig, self.r2, self.ax, self.obstacles, targetPoint).start()
        #self.r1.Thread_Animation(plt, self.r1, self.ax, self.obstacles, targetPoint).start()
        #self.r2.Thread_Animation(plt, self.r2, self.ax, self.obstacles, targetPoint).start()

        #self.circles_r1 = self.draw_obstacles(self.r1)
        #self.circles_r2 = self.draw_obstacles(self.r2)

        #self.draw_obstacles(self.r1)
        #self.draw()
        plt.show()

    '''
    # initialization function: plot the background of each frame
    def init_anim(self):
        self.pointRobot_r1.set_data([self.r1.x], [self.r1.y])
        #self.pointRobot_r2.set_data([self.r2.x], [self.r2.y])
        return self.pointRobot_r1, self.pointRobot_r2

    def animate(self, i):
        self.update_circles(self.circles_r1)
        self.update_circles(self.circles_r2)
        self.ax.redraw_in_frame()
        x1, y1 = self.r1.move()
        x2, y2 = self.r2.move()
        self.pointRobot_r1.set_data([x1], [y1])
        self.pointRobot_r2.set_data([x2], [y2])
        return self.pointRobot_r1, self.pointRobot_r2

    def update_circles(self, circles):
        for circle, obstacle in circles.items():
            circle.set_radius(obstacle.estimateRadius)

    def draw_obstacles(self, robot):
        circles = {}
        for obstacle in robot.obstacles:
            circle = plt.Circle((obstacle.x, obstacle.y), obstacle.estimateRadius,
                                 color=robot.color, fill=False)
            self.ax.add_artist(circle)
            circles[circle] = obstacle
        return circles

    def draw(self):
        # Intervall = 1000 perchè il robot si move di tot metri al secondo
        anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init_anim,
                                       interval=1000, blit=True)

        plt.show()
    '''


if __name__ == '__main__':
    world = World()
    #world.draw()
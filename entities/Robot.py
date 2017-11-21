from threading import Thread, Event, Lock
from entities.Obstacle import *

from util.Algorithms import *
import numpy as np
import time
from Communication.Client import *


class Robot:

    VELOCITY = 1  #metri al secondo
    VISIBILITY = 0.5 #visibilità del robot per stimare il raggio degli ostacoli
    TIME_INTERVAL = 0.5 #secondi - il tempo entro il quale vogliamo vedere la prossima posizione del robot
    # l'arrivo alla posizione target del robot viene valutata all'interno di un cerchio di raggio stimato dalla velocità
    # e dallo step temporale con cui sta viaggiando il robot
    ESTIMATE_TARGET_RADIUS = (VELOCITY * TIME_INTERVAL) / 2
    #Gli stati del sistema ibrido
    STATES = ("MOVE", "STOP")
    TP_CLOCK = 8.0  #clock per l'aggiornamento dell'algoritmo di pianificazione
    TE_CLOCK = 4.0  #clock per l'aggiornamento della stima del raggio degli ostacoli
    TC_CLOCK = 6.0  #clock per la comunicazione

    def __init__(self, x, y, targetPoint, color):
        self.x = x
        self.y = y
        self.color = color
        self.zp = 0.0 #timer per l'aggiornamento della funzione plan
        self.state = self.STATES[1]
        self.targetPoint = targetPoint
        self.obstacles = []
        #self.initialize_obstacles(obstacles)
        self.obstaclesCopy = []
        self.theta = 0.0
        self.speed = 0.0
        self.event_TP_Clock = Event()
        self.event_TE_Clock = Event()
        self.event_TC_Clock = Event()
        self.lock = Lock()
        #self.Thread_TP_Clock(self, self.event_TP_Clock, self.lock).start()
        #self.Thread_TE_Clock(self, self.event_TE_Clock, self.lock).start()

    #restutuisce la distanza da un ostacolo
    def get_distance_from_obstacle(self, x, y, obstacle):
        return sympy.Point(obstacle.x, obstacle.y).distance(sympy.Point(x, y))

    #restituisce la distanza dal target
    def get_distance_from_target(self):
        return self.targetPoint.distance(sympy.Point(self.x, self.y))

    #calcola la stima del raggio dell'ostacolo
    def estimate_radius(self, obstacle):
        estimatedRadius = obstacle.radius + self.VISIBILITY * (self.get_distance_from_obstacle(self.x, self.y, obstacle) - obstacle.radius)
        return estimatedRadius

    #inizializza la stima dei raggi di una lista di ostacoli e li aggiunge alla lista obstacles.
    def initialize_obstacles(self, obstacles):
        for obstacle in obstacles:
            estimateRadius = self.estimate_radius(obstacle)
            self.obstacles.append(Obstacle(obstacle.x, obstacle.y, obstacle.radius, estimateRadius, key=obstacle.key))

    #esegue un calcolo della stima degli ostacoli e aggiorna di conseguenza il raggio (estimateRadius) degli ostacoli a quello minore
    def estimate_obstacles(self):
        for obstacle in self.obstacles:
            estimateRadius = self.estimate_radius(obstacle)
            if estimateRadius < obstacle.estimateRadius:
                obstacle.estimateRadius = estimateRadius

    #aggiorna la stima del raggio di un ostacolo comparandolo a quella di un'altro ostacolo (con lo stesso id)
    def compare_obstacles(self, otherObstacles):
        for obstacle in self.obstacles:
            for other in otherObstacles:
                if other.key == obstacle.key:
                    if other.estimateRadius < obstacle.estimateRadius:
                        obstacle.estimateRadius = other.estimateRadius

    #restituisce le componenti dello spostamento
    def get_component_direction(self):
        x = self.speed * np.cos(self.theta) * self.TIME_INTERVAL
        y = self.speed * np.sin(self.theta) * self.TIME_INTERVAL
        return x, y

    #verifica se al prossimo step il robot va a schiantarsi su un ostacolo
    def check_crash(self, stepX, stepY):
        x = self.x + stepX
        y = self.y +stepY
        crash = False
        for obstacle in self.obstaclesCopy:
            distance = self.get_distance_from_obstacle(x, y, obstacle)
            if distance < obstacle.estimateRadius:
                crash = True
                print("CRASHING")
                break
        return crash

    #muove il robot attraverso le componenti dello spostamento
    def move(self):
        #se il robot si trova all'interno della circonferenza stimata alla posizione target allora è giunto a dstinazione e deve fermarsi
        if self.get_distance_from_target() < self.ESTIMATE_TARGET_RADIUS:
            self.event_TP_Clock.set()   #ferma l'aggiornamento della pianificazione
            self.event_TE_Clock.set()   #ferma l'aggiornamento della stima degli ostacoli
            self.event_TC_Clock.set()   #stoppa la comunicazione, anche se questa attavità dovrebbe continuare a svolgerla così che anche i robot che non sono ancora giunti a destinazione possano usufruire della sua informazione
            self.speed = 0.0    #fermati
            self.state = self.STATES[1] #cambia lo stato in STOP
        #se il robot non è giunto a destinazione allora si deve muovere
        if self.state == self.STATES[0]:
            x, y = self.get_component_direction()
            crash = self.check_crash(x, y)
            if not crash:
                self.x += x
                self.y += y
        return self.x, self.y

    def plan(self, obstacleCopy):
        '''
        durante la pianificazione il robot si ferma.
        è possibile disabilitare questa istruzione dato che anche se il robot continua a muoversi si fermerà non appena
        incontrerà un ostacolo lungo il suo cammino.
        '''
        #self.speed = 0.0
        '''
        Il robot si deve per forza fermare perchè nel caso in cui si muovesse mentre sta pianificando,
        la posizione in cui si trova non combacerebbe con quella iniziale del percorso. Quindi andando a calcolare
        la direzione da intraprendere risulterebbe sballata. Si potrebbe pensare di utilizzare le coordinate del
        percorso e non quelle del robot quando si va a calcolare i coefficiente angolare...In questo caso però
        il percorso che sta effettuando il robot non combacerebbe con quello calcolato durante la pianificazione.
        Quindi sarà necessario realizzare un controllo di 'Check Collision' onde evitare che il robot vada a sbattere
        da qualche parte.
        '''
        startPoint = sympy.Point(self.x, self.y)
        #verifica se il target si trova all'interno di un ostacolo
        if self.in_obstacle(self.targetPoint):
            print("Errore: punto irraggiungibile (Encloses Detected)")
        else:
            path = build_path(startPoint, self.targetPoint, obstacleCopy)
            #direction = line_slope(self.x, self.y, path[1].x, path[1].y)      Qui il robot si calcola la direzione a partire dalle proprie coordinate
            if path:
                direction = line_slope(path[0].x, path[0].y, path[1].x, path[1].y)  #la direzione è il coefficiente angolare della retta passante per due punti
                slape_rad = np.arctan(float(direction))
                if path[1].x > path[0].x:
                    self.theta = slape_rad
                elif path[1].x < path[0].x:
                    self.theta = np.pi + slape_rad
                else:
                    self.theta = slape_rad
        #print(self.theta)
        self.speed = self.VELOCITY
        if self.state == self.STATES[1]:
            self.state = self.STATES[0]
        return self.theta

    #verifica se un punto si trova all'interno di un ostacolo
    def in_obstacle(self, point):
        encloses = False
        for obstacle in self.obstacles:
            distance = point.distance(sympy.Point(obstacle.x, obstacle.y))
            if distance <= obstacle.estimateRadius:
                encloses = True
        return encloses

    #effettua una copia degli ostacoli
    def copy_obstacle(self):
        obstaclesCopy = []
        for obstacle in self.obstacles:
            obstaclesCopy.append(Obstacle(obstacle.x, obstacle.y, obstacle.radius, obstacle.estimateRadius, key=obstacle.key))
        return obstaclesCopy

    #fa partire tutti i thread che eseguono le operazioni del robot
    def start_actions(self, plt, ax, pointRobot):
        #start thread per la pianificazione
        self.Thread_TP_Clock(self, self.event_TP_Clock, self.lock).start()
        #start thread per l'aggiornamento della stime del raggio degli ostacoli
        self.Thread_TE_Clock(self, self.event_TE_Clock, self.lock, plt, ax).start()
        #start thread per l'animazione
        self.Thread_Animation(plt, self, pointRobot).start()
        #start thread per la comunicazione
        Client(self, self.event_TC_Clock, self.lock).start()

    '''
    Thread per la pianificazione
    '''
    class Thread_TP_Clock(Thread):
        def __init__(self, robot, event, lock):
            Thread.__init__(self)
            self.robot = robot
            self.stopped = event
            self.lock = lock

        def run(self):
            while not self.stopped.wait(self.robot.TP_CLOCK):
                '''Invece di effettuare il lock su tutta la pianificazione lo dovremmo fare solo sulla copia della lista degli ostacoli per aumentare la concorrenza'''
                self.lock.acquire()
                self.robot.obstaclesCopy = self.robot.copy_obstacle()
                self.lock.release()
                print(self.name +" sta pianificando la prossima mossa...")
                self.robot.plan(self.robot.obstaclesCopy)

    '''
    Thread per l'aggiornamento degli ostacoli
    '''
    class Thread_TE_Clock(Thread):
        def __init__(self, robot, event, lock, plt, ax):
            Thread.__init__(self)
            self.plt = plt
            self.ax = ax
            self.robot = robot
            self.stopped = event
            #self.circles = circles
            self.lock = lock

        def run(self):
            #self.robot.initialize_obstacles(self.obstacles)
            self.circles = self.draw_obstacles(self.robot)
            while not self.stopped.wait(self.robot.TE_CLOCK):
                self.lock.acquire()
                print(self.name +" sta aggiornando la stima degli ostacoli...")
                self.robot.estimate_obstacles()
                self.lock.release()
                self.update_circles(self.circles)
                self.plt.draw()

        #aggiorna il disegno degli ostacoli
        def update_circles(self, circles):
            for circle, obstacle in circles.items():
                circle.set_radius(obstacle.estimateRadius)

        #disegna gli ostacoli sul plot
        def draw_obstacles(self, robot):
            circles = {}
            for obstacle in robot.obstacles:
                circle = self.plt.Circle((obstacle.x, obstacle.y), obstacle.estimateRadius,
                                    color=robot.color, fill=False)
                self.ax.add_artist(circle)
                circles[circle] = obstacle
            return circles

    '''
    Thread per l'animazione
    '''
    class Thread_Animation(Thread):
        def __init__(self, plt, robot, pointRobot):
            Thread.__init__(self)
            self.plt = plt
            self.robot = robot
            self.stopped = Event()
            self.pointRobot = pointRobot

        def run(self):
            while not self.stopped.wait(self.robot.TIME_INTERVAL):
                print(self.name + " sta disegnando...")
                x, y = self.robot.move()
                self.pointRobot.set_data([x], [y])
                self.plt.draw()
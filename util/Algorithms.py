import shapely.geometry as sh
from util.EquationSolver import *
from util.Search import *
from util.GeometryElements import *
import sympy
import numpy
'''
Algoritmo per la ricerca:
parto dal punto startPoint.
da questo trovo le tangenti agli ostacoli che si trovano lungo il percorso (usciranno sempre due tengenti)
Ciascuna tangente ha il punto p1 (startPoint) e il punto p2 (di tangenza)

Iniziare la creazione del grafo creando gli archi che partono da p1 e arrivano a p2 (con il relativo peso - distanza).

Tracciare le tangenti dal punto targetPoint agli ostacoli lungo il percorso (usciranno sempre due tangenti)
Ciascuna tangente ha il punto p1 (targetPoint) e il punto p2 (di tangenza)

PROBLEMA: come associare i punti sulla circonferenza in modo da formare l'arco del settore circolare???
RISULUZIONE: basta prendere ogni arci di circonferenza che parte dal punto p2 di ciascuna tangente dell'insieme di quelle che partono
dal punto di start e arriva al punto p2 di ciascuna tangente che parte dal punto di target.
Quindi aggiungere al grafo i punti delle rette tangenti con peso sugli archi pari alla lunghezza dell'arco di circonferenza

Ripetere l'algoritmo fino a che il percorso è libero da ostacoli
'''

'''
Funzione che calcola gli ostacoli che sono presenti lungo il segmento che unisce i punti startPoint e targetPoint.
RETURN: lista degli ostacoli lungo il percorso
'''
def get_path_obstacles(startPoint, targetPoint, obstacles):
    obstaclesPath = []
    segment = sh.LineString([(startPoint.x,startPoint.y), (targetPoint.x, targetPoint.y)])  #costruzione del segmento con la libreria shapely
    for obstacle in obstacles:  #controllo se un ostacolo è presente sul percorso
        circle = sh.Point(obstacle.x, obstacle.y).buffer(obstacle.estimateRadius).boundary
        intersections = circle.intersection(segment)
        if intersections:
            obstaclesPath.append(obstacle)  # aggiungo l'ostacolo presente sul tragitto all'array
    #aggiungiamo alla lista anche gli ostacoli che intersecano quelli che si trovano lungo il percorso
    for obstacle in obstacles:
        circle = sh.Point(obstacle.x, obstacle.y).buffer(obstacle.estimateRadius).boundary
        for obstaclePath in obstaclesPath:
            circlePath = sh.Point(obstaclePath.x, obstaclePath.y).buffer(obstaclePath.estimateRadius).boundary
            #intersections = obstacle.circle.intersection(obstaclePath.circle)
            intersections = circle.intersection(circlePath)
            if intersections and obstacle not in obstaclesPath:
                obstaclesPath.append(obstacle)
    return obstaclesPath

'''
Funzione per il calcolo delle tangenti agli ostacoli che si trovano lungo il percorso dato un determinato punto (non prende le tangenti che intersecano altri ostacoli)
RETURN: list(tangenti)
'''
def get_tangentials(point, obstaclesInPath):
    tangentials = []
    for obstacle in obstaclesInPath:
        #troviamo le tangenti alla circonferenza
        results = tangent_of_circle(point.x, point.y, obstacle.x, obstacle.y, obstacle.estimateRadius)
        if results:
            for result in results:
                x = None
                y = None
                m = None
                for elem, value in result.items():
                    if str(elem) == 'm':
                        m = value
                    elif str(elem) == 'x':
                        x = value
                    elif str(elem) == 'y':
                        y = value
                tangent = Tangent(x1=point.x, y1=point.y, x2=x, y2=y, slape=m, obstacle=obstacle)
                tangentials.append(tangent)
    return tangentials

def remove_tangents(tangentials, obstaclesInPath):
    tangentTmp = []
    for tangent in tangentials:
        for obstacle in obstaclesInPath:
            if tangent.obstacle is not obstacle:
                #intersection = intersect_line_circle(tangent.slape, tangent.x1, tangent.y1, obstacle.x, obstacle.y, obstacle.estimateRadius)
                intersection = intersect_line_line_inc(tangent.slape, tangent.x1, tangent.y1, obstacle.x, obstacle.y)
                x = None
                y = None
                for elem, value in intersection.items():
                    if str(elem) == 'x':
                        x = value
                    elif str(elem) == 'y':
                        y = value
                distance = float(sympy.Point(x, y).distance(sympy.Point(obstacle.x, obstacle.y)))
                if distance <= obstacle.estimateRadius and tangent in tangentials:
                    tangentTmp.append(tangent)

    for tng in tangentTmp:
        if tng in tangentials:
            tangentials.remove(tng)
    return tangentials


def remove_obstacle(tangentials, obstacles):
    for tangent in tangentials:
        if tangent.obstacle in obstacles:
            obstacles.remove(tangent.obstacle)
    return obstacles


def build_graph(graph, startPoint, targetPoint, obstacles):
    obstaclesCopy = obstacles.copy()
    nodeList = [startPoint]
    while nodeList:
        startPoint = nodeList.pop(0)
        obstaclesInPath = get_path_obstacles(startPoint, targetPoint, obstaclesCopy)
        tangentials = get_tangentials(startPoint, obstaclesInPath)
        remove_tangents(tangentials, obstaclesInPath)
        graph.edges[startPoint] = {}
        if tangentials:
            for tangent in tangentials:
                if tangent.obstacle is not None:
                    graph.edges[startPoint][tangent.p2] = sympy.Segment(startPoint, tangent.p2).length

            #qui aggiungere: trova le tangenti dal targetPoint e aggiungere gli archi al grafo
            tangentialsTarget = get_tangentials(targetPoint, obstaclesInPath)
            remove_tangents(tangentialsTarget, obstaclesInPath)
            for tangent in tangentials:
                graph.edges[tangent.p2] = {}
                for tangentTarget in tangentialsTarget:
                    if tangent.obstacle is tangentTarget.obstacle:
                        bow = bow_circumference(tangent.p2.x, tangent.p2.y, tangentTarget.p2.x, tangentTarget.p2.y,
                                                tangent.obstacle.estimateRadius)
                        graph.edges[tangent.p2][tangentTarget.p2] = bow
                        nodeList.append(tangentTarget.p2)
                if not graph.edges[tangent.p2]:
                    for tangentTarget in tangentialsTarget:
                        if tangentTarget.p2 not in nodeList:
                            graph.edges[tangent.p2][tangentTarget.p2] = sympy.Segment(tangentTarget.p2, tangent.p2).length
                            nodeList.append(tangentTarget.p2)
        else:
            graph.edges[startPoint][targetPoint] = sympy.Segment(startPoint, targetPoint).length
        remove_obstacle(tangentials, obstaclesCopy)
    return graph

def build_path(startPoint, targetPoint, obstacles):
    graph = SimpleGraph()
    #startPoint = sympy.Point(sympy.N(startPoint.x, 2), sympy.N(startPoint.y, 2))
    startPoint = sympy.Point(startPoint.x, startPoint.y)
    graph = build_graph(graph, startPoint, targetPoint, obstacles)
    path = []
    if startPoint in graph.edges.keys():
        came_from, cost_so_far = a_star_search(graph, startPoint, targetPoint)
        path = reconstruct_path(came_from, startPoint, targetPoint)
    return path
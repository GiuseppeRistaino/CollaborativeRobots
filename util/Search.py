import heapq
import sympy


class Node():
    def __init__(self, pointSympy):
        self.point = pointSympy

    def __eq__(self, other):
        return self

    def __lt__(self, other):
        return self



class SimpleGraph:
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        return self.edges[id]

    def cost(self, from_node, to_node):
        return self.edges[from_node][to_node]


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(Node(start), 0)
    came_from = {}  # determina una coppia di nodi dove l'uno è la partenza e l'altro è l'arrivo
    cost_so_far = {}  # determina una coppia: nodo e il costo per arrivarci
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current.point == goal:
            break

        for next in graph.neighbors(current.point):
            new_cost = cost_so_far[current.point] + graph.cost(current.point, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[
                    next] = new_cost  # mi ritrovo nella lista anche un elemento che non potrebbe far parte del path finale (infatti nella ricerca si controllano sempre tutti gli archi e quindi i nodi raggiungibili
                priority = new_cost
                frontier.put(Node(next), priority)
                came_from[next] = current.point

    return came_from, cost_so_far


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


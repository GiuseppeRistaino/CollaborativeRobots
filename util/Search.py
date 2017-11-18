import heapq
import sympy

'''
classe Nodo utile per tenere traccia delle informazioni riguardanti un nodo del grafo.
pointSympy: classe Point della libreria sympy
'''
class Node():
    def __init__(self, pointSympy):
        self.point = pointSympy

    #funzione per confrontare due oggitti di tipo Nodo.
    def __eq__(self, other):
        return self

    #funzione per confrontare due oggitti di tipo Nodo.
    def __lt__(self, other):
        return self


'''
classe utile alla costruzione del grafo.
edges: dizionario che fa corrispondere a ciascun nodo (id) un dizionario nel quale ciascun nodo corrisponde un arco (cost).
'''
class SimpleGraph:
    def __init__(self):
        self.edges = {}

    #funzione che restituisce i nodi adiacenti al nodo (id)
    def neighbors(self, id):
        return self.edges[id]

    #funzione che restituisce il costo dell'arco a partire dal nodo (from_node) ad arrivare al nodo (to_node)
    def cost(self, from_node, to_node):
        return self.edges[from_node][to_node]

'''
classe per la creazione di una coda a priorità utilizzando la classe heapq.
Oridna gli elementi al suo interno utilizzando una priorità crescente.
Nel caso in cui gli elementi mostrano una prorità uguale vengono utilizzate le funzioni __eq__ ed __lt__ per
determinare le loro posizioni nella coda.
'''
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

'''
funzione per l'implementazione dell'algoritmo a-star.
utilizzando una coda a priorità viene determinato il percorso minimo con il rispettivo costo complessivo per attraversarlo,
partendo dal nodo start e arrivando al nodo goal di un dato grafo.
graph: oggetto SimpleGraph
start: sympy.Point
goal: sympy.Point

N.B.: la coda a priorità deve contenere oggetti di tipo Nodo per la possibilità di poterli confrontare nel caso in cui
abbiano la stessa priorità.
'''
def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(Node(start), 0)
    came_from = {}  # determina una coppia di nodi dove l'uno è la partenza e l'altro è l'arrivo
    cost_so_far = {}  # determina una coppia: nodo e il costo per arrivarci
    came_from[start] = None #si inizia dal nodo start
    cost_so_far[start] = 0  #per raggiungere il nodo start ho speso un costo 0

    while not frontier.empty():
        current = frontier.get()

        if current.point == goal:
            break

        for next in graph.neighbors(current.point):
            new_cost = cost_so_far[current.point] + graph.cost(current.point, next)
            #se il costo appena calcolato per arrivare al next è minore rispetto a quello calcolato in precedenza allora aggiorna cost_so_far
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost  # mi ritrovo nella lista anche un elemento che non potrebbe far parte del path finale (infatti nella ricerca si controllano sempre tutti gli archi e quindi i nodi raggiungibili
                priority = new_cost
                frontier.put(Node(next), priority)
                came_from[next] = current.point

    return came_from, cost_so_far

'''
funzione per la costruzione del percorso a partire dal dizionario came_from.
RETURN: lsita di punti che fanno parte del path
'''
def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
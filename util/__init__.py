from util.Search import *
from entities.Obstacle import *
import sympy

if __name__ == '__main__':
    #intersect_line_circle(0, 0, 0, 0, 0, 1)
    startPoint = sympy.Point(2, 0)
    endPoint = sympy.Point(-2,0)
    obstacle1 = Obstacle(0, 0, 1)
    obstacle2 = Obstacle(0, 2, 1)
    obstacles = []
    obstacles.append(obstacle1)
    obstacles.append(obstacle2)
    #build_graph(startPoint, endPoint, obstacles)

    a = Node('A', 0, 0)
    b = Node('B', 10, 10)
    c = Node('C', 30, 30)
    d = Node('D', 50, 50)
    e = Node('E', 100, 100)

    example_graph = SimpleGraph()
    '''
    example_graph.edges = {
        a: {b: 5},
        b: {a: 2, c: 3, d: 4},
        c: {a: 3},
        d: {e: 2, a: 5},
        e: {b: 5}
    }
    '''
    example_graph.edges[a] = {}
    example_graph.edges[a][b] = 5
    example_graph.edges[b] = {}
    example_graph.edges[b][a] = 2
    example_graph.edges[b] = {}
    example_graph.edges[b][e] = 4

    print(example_graph.cost(a, b))

    come_from, cost_so_far = a_star_search(example_graph, a, e)
    print(come_from)
    print(cost_so_far)
    print(reconstruct_path(come_from, a, e))
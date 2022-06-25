import copy

class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)      
    def construct_graph(self, nodes, init_graph):
        graph = {}
        for node in nodes:
            graph[node] = {}
        graph.update(init_graph)  
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value                 
        return graph
    def get_nodes(self):
        return self.nodes
    def get_outgoing_edges(self, node):
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    def value(self, node1, node2):
        return self.graph[node1][node2]

def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
    shortest_path = {}
    previous_nodes = {}
    max_value = float("inf")
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[start_node] = 0
    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                previous_nodes[neighbor] = current_min_node
        unvisited_nodes.remove(current_min_node)
    return shortest_path
    


def solution(map):
    height = len(map)
    width = len(map[0])

    columns = [str(x) for x in range(width)]
    rows = [str(x) for x in range(height)]

    nodes = []
    for c in columns:
        for r in rows:
            nodes.append(c + "_" + r)

    costs = [item * 1000 + 1 for sublist in map for item in sublist]
    results = []
    for i, cost in enumerate(costs):
        if cost > 1000:
            new_costs = copy.deepcopy(costs)

            new_costs[i] -= 1000

            init_graph = {}
            for node in nodes:
                init_graph[node] = {}

            for i, node in enumerate(nodes):
                if (i + 1) % width != 0:
                    init_graph[node][nodes[i + 1]] = max(new_costs[i], new_costs[i + 1])
                if i < len(nodes) - width:
                    init_graph[node][nodes[i + width]] = max(new_costs[i], new_costs[i + width])
            graph = Graph(nodes, init_graph)

            shortest_path = dijkstra_algorithm(graph=graph, start_node="0_0")
            result = shortest_path.get(nodes[-1]) + 1

            results.append(result)

    return min(results) 

test = [
    [0, 0, 0, 0, 0, 0], 
    [1, 1, 1, 1, 1, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 1, 1, 1, 1, 1], 
    [0, 1, 1, 1, 1, 1], 
    [0, 0, 0, 0, 0, 0]
]

print(solution(test))

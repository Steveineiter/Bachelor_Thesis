# Idea from https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/


class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = []

    def add_edge(self, source, destination, weight):
        self.graph.append([source, destination, weight])

    def find(self, parent, element):
        if parent[element] == element:
            return element
        return self.find(parent, parent[element])

    def union(self, parent, rank, x, y):
        x_root = self.find(parent, x)
        y_root = self.find(parent, y)

        if rank[x_root] < rank[y_root]:
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:
            parent[y_root] = x_root

    def kruskal_minimum_spanning_tree(self):
        result = []
        sorted_edges_index = 0
        result_index = 0

        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []

        for node in range(self.vertices):
            parent.append(node)
            rank.append(0)

        while result_index < self.vertices - 1:
            source, destination, weight = self.graph[sorted_edges_index]
            sorted_edges_index = sorted_edges_index + 1
            x = self.find(parent, source)
            y = self.find(parent, destination)

            if x != y:
                result_index = result_index + 1
                result.append([source, destination, weight])
                self.union(parent, rank, x, y)

        minimumCost = 0
        print("Edges in the constructed MST")
        for u, v, weight in result:
            minimumCost += weight
            print("%d -- %d == %d" % (u, v, weight))
        print("Minimum Spanning Tree", minimumCost)


## Testing:
# list_of_words = ["Zelda", "Link", "Foo", "Bar", "Risk", "Think"]
# lenght_of_words = len(list_of_words)
# g = Graph(lenght_of_words ** 2 - lenght_of_words)
#
# matrix = [
#     [0, 5, 5, 5, 5, 5],
#     [5, 0, 4, 4, 2, 2],
#     [5, 4, 0, 3, 4, 5],
#     [5, 4, 3, 0, 4, 5],
#     [5, 2, 4, 4, 0, 3],
#     [5, 2, 5, 5, 3, 0],
# ]
#
# for i in range(lenght_of_words):
#     for j in range(lenght_of_words):
#         if i != j:
#             g.add_edge(i, j, matrix[i][j])
# g.kruskal_minimum_spanning_tree()
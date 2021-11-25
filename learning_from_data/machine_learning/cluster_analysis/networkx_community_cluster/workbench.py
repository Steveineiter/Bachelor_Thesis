import networkx as nx
from sklearn.metrics import silhouette_score
from networkx.algorithms.community import greedy_modularity_communities
import numpy as np
import matplotlib.pyplot as plt

G = nx.Graph()

# Nodes
G.add_node(1)
G.add_nodes_from([2, 3])
G.add_nodes_from([
    (4, {"color": "green"}),
    (5, {"color": "red"})
])
H = nx.path_graph(10)
G.add_nodes_from(H)  # getting nodes of second_graph
G.add_node(H)  # adding the whole second_graph as one node

# Edges
G.add_edge(1, 2)
e = (2, 3)
G.add_edge(*e)
G.add_edges_from([(1, 2), (1, 3)])
G.add_edges_from(H.edges)
print(G)
G.clear()
print(G)

G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1, 2)
G.add_node("spam")        # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, 'm')

print(G.number_of_nodes())
print(G.number_of_edges())
G.add_node(1)
print(G)

DG = nx.DiGraph()
DG.add_edge(2, 1)
DG.add_edge(1, 3)
DG.add_edge(2, 4)
DG.add_edge(1, 2)
assert list(DG.successors(2)) == [1, 4]
assert list(DG.edges) == [(2, 1), (2, 4), (1, 3), (1, 2)]

# Examining elements of a graph
print(list(G.nodes))
print(list(G.edges))
print(list(G.adj[1]))
print(G.degree[1])
print(G.edges([2, "m"]))
print(G.degree([2, 3]))

# Removing elements from a graph
print("\nRemoving")
print(list(G.nodes))
G.remove_node(2)
G.remove_nodes_from("spam")
print(list(G.nodes))
G.remove_edge(1, 3)

# Using the graph constructors
print("\ngraph constructors")
print(G.edges)
G.add_edge(1, 2)
H = nx.DiGraph(G)  # create a DiGraph using the connections from G
print(list(H.edges()))
edge_list = [(0, 1), (1, 2), (2, 3)]
H = nx.Graph(edge_list)

# Accessing edges and neighbors
print("\naccessing edges and neighbors")
G = nx.Graph([(1, 2, {"color": "yellow"})])
print(G[1])
print(G[1][2])
print(G.edges[1, 2])

G.add_edge(1, 3)
G[1][3]["color"] = "blue"
G.edges[1, 2]["color"] = "red"
print(G.edges[1, 2])

print("\nFG")
FG = nx.Graph()
FG.add_weighted_edges_from([(1, 2, 0.125), (1, 3, 0.75), (2, 4, 1.2), (3, 4, 0.375)])
for n, nbrs in FG.adj.items():
    for nbr, eattr in nbrs.items():
        wt = eattr["weight"]
        if wt < 0.5:
            print(f"({n}, {nbr}, {wt:.3}")

for (u, v, wt) in FG.edges.data('weight'):
    if wt < 0.5:
        print(f"({u}, {v}, {wt:.3})")

# Adding attributes to graphs, nodes, and edges
# Graph attributes
print("\nAttributes")
# G = nx.Graph(day="Friday")
G = nx.Graph(foowererero="baroo")
print(G.graph)

G.graph["day"] = "Friday"
print(G.graph)
G.graph["day"] = "Monday"
print(G.graph)

# Node attributes
G.add_node(1, time="5pm")
G.add_nodes_from([3], time="2pm")
print(G.nodes[1])
G.nodes[1]["room"] = 714
print(G.nodes.data())

# Edge Attributes
G.add_edge(1, 2, weight=4.7)
G.add_edges_from([(3, 4), (4, 5)], color="red")
G.add_edges_from([(1, 2, {"color": "blue"}), (2, 3, {"weight": 8})])
G[1][2]["weight"] = 4.69
G.edges[3, 4]["weight"] = 4.2
print(G.edges.data())

# Directed graphs
print("\nDirected graphs")
DG = nx.DiGraph()
DG.add_weighted_edges_from([(1, 2, 0.5), (3, 1, 0.75)])
print(DG.out_degree(1, weight="weight"))
print(DG.degree(1, weight="weight"))
print(list(DG.successors(1)))
print(list(DG.neighbors(1)))

# Analyzing graphs
print("\nAnalyzing graphs")
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3)])
G.add_node("spam")
print(list(nx.connected_components(G)))
print(sorted(d for n, d in G.degree()))
print(nx.clustering(G))
sp = dict(nx.all_pairs_shortest_path(G))
print(sp[3])

# Drawing graphs
# print("\nDrawing graphs")
# G = nx.petersen_graph()
# subax1 = plt.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')
# subax2 = plt.subplot(122)
# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
# plt.show()


# Testing
G = nx.Graph()
G.add_node("foo")
G.add_edge("foo", "bar", weight=1)
print(G.nodes.data())
print(G.edges.data())
G["foo"]["bar"]["weight"] = 3
G["bar"]["foo"]["weight"] = 33
G.add_edge("foo", "bar", color="pink")
try:
    G["seikon"]["qwaser"]["weight"] = 69  # doesnt work because it has to be added first
except KeyError:
    G.add_edge("seikon", "qwaser", weight=1)

G["qwaser"]["seikon"]["weight"] = 39

print(G.edges.data())


# community algo
G = nx.karate_club_graph()
G.add_edge(1, 2, weight=2)
c = list(greedy_modularity_communities(G))
print(sorted(c))
foo = np.array(G.nodes)
bar = list()
for element in foo:
    for i in range(len(c)):
        if element in c[i]:
            bar.append(i)
print(silhouette_score(foo.reshape(-1, 1), bar))

from sklearn import metrics
from sklearn.metrics import pairwise_distances
from sklearn import datasets
X, y = datasets.load_iris(return_X_y=True)


import numpy as np
from sklearn.cluster import KMeans
kmeans_model = KMeans(n_clusters=4, random_state=1).fit(X)
labels = kmeans_model.labels_
print(metrics.silhouette_score(X, labels, metric='euclidean'))
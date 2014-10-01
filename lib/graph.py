import networkx as nx
import matplotlib.pyplot as plt


# is_to_degree=True will give number of nodes pointing to node. False is opposite
def get_sorted_degrees(graph, is_to_degree=True):
    weights = {}
    nodes = set()
    for node in graph.iterkeys():
        for adj in graph[node].iterkeys():
            index = adj if is_to_degree else node
            try:
                weights[index] += 1
            except:
                weights[index] = 1
            nodes.add(adj)

    return weights, sorted(nodes, key=lambda x: weights[x], reverse=True)


# plots a graph
def plot(graph):
    g = nx.DiGraph()
    labels = []
    for node in graph.iterkeys():
        g.add_node(node)
        labels.append(node)

    for node1 in graph.iterkeys():
        for node2 in graph[node1].iterkeys():
            try:
                g.add_edge(node1, node2)
            except:
                g.add_node(node2)
                g.add_edge(node1, node2)

    nx.draw(g, with_labels=True, font_size=9, font_color='b')
    plt.show()
    return g
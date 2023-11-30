import networkx as nx
import matplotlib.pyplot as plt

# Create a graph
G = nx.Graph()

# Add nodes and edges
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_edge(1, 2, label="connection 1")
G.add_edge(2, 3, label="connection 2")
G.add_edge(1, 3, label="connection 3")

pos = nx.spring_layout(G)
#pos = nx.kamada_kawai_layout(G)

# Draw the graph
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, font_size=20)
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Show the plot
plt.show()

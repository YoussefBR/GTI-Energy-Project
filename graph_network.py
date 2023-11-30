import networkx as nx
import matplotlib.pyplot as plt

# Create a graph
G = nx.Graph()

# Add nodes and edges
G.add_node("tacos")
G.add_node("pizza")
G.add_node("ur mom")
G.add_edge("tacos", "pizza")
G.add_edge("ur mom", "tacos")
G.add_edge("pizza", "ur mom")

# Draw the graph
nx.draw(G, with_labels=True, node_color='skyblue', node_size=700, font_size=20)

# Show the plot
plt.show()

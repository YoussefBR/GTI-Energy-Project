import networkx as nx
import matplotlib.pyplot as plt
import coherence_network as cn
import random as rm

# Create a graph
#G = nx.Graph()

# Add nodes and edges
#G.add_node("center")
#G.add_node("tacos")
#G.add_node("pizza")
#G.add_node("ur mom")
#G.add_edge("center", "pizza")
#G.add_edge("center", "tacos")
#G.add_edge("center", "ur mom")

# coherence network testing
#co_net = cn.build_network(["tacos", "cheese", "pizza", "spagehti", "oranges", "tamaoto sauce", "beans", "trash", "jelly", "snacks", "meat", "carrots", "candy", "pasta", "evil"], 15)

class triple:
     def __init__(self, subject, object, frequency):
        self.subject = subject
        self.object = object
        self.frequency = frequency

# random generation of triples and frequencies
l = ["tacos", "cheese", "pizza", "spagehti", "oranges", "tamaoto sauce", "beans", "trash", "jelly", "snacks", "meat", "carrots", "candy", "pasta", "evil"]
triples = []
frequencies ={}
for x in range(50):
    rand_num1 = rm.randint(0,14)
    rand_num2 = rand_num1
    while rand_num1 == rand_num2:
        rand_num2 = rm.randint(0,14)
    frequency = rm.randint(1,50)
    triples.append(triple(l[rand_num1], l[rand_num2], frequency))
    frequencies[(l[rand_num1], l[rand_num2])] = frequency

sorted_items_by_values = sorted(frequencies.items(), key=lambda x: x[1])
sorted_frequencies = dict(sorted_items_by_values)

print(sorted_frequencies)

co_net, score = cn.find_best_network(triples, frequencies)

print("center:", {co_net.center}, "score:", score)

# Draw the graph
nx.draw(co_net.graph, with_labels=True, node_color='skyblue', node_size=700, font_size=20)

# Show the plot
plt.show()
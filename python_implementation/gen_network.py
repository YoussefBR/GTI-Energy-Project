import networkx as nx
import matplotlib.pyplot as plt
import python_implementation.coherence_network as cn
import python_implementation.triple_extraction as te

class triple:
     def __init__(self, subject, verb, object, frequency):
        self.subject = subject
        self.verb = verb
        self.object = object
        self.frequency = frequency

# extract triples from file
te.main()
extracted_triples = te.getTriples()
connections = te.getWordConnections()

# convert triples from file into triples the coherence network can handle
triples = []
frequencies = {}
for e_triple in extracted_triples:
    triples.append(triple(e_triple[0][0], e_triple[0][1], e_triple[0][2], e_triple[1]))
    frequencies[(e_triple[0][0], e_triple[0][2])] = e_triple[1]

# find best network
co_net, score = cn.find_best_network(triples, frequencies, connections)

# output center
print("center:", {co_net.center}, "score:", score)

# Draw the graph
nx.draw(co_net.graph, with_labels=True, node_color='skyblue', node_size=700, font_size=20)

# Show the plot
plt.show()
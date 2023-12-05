import networkx as nx
import matplotlib.pyplot as plt
import coherence_network as cn
import triple_extraction as te

class triple:
     def __init__(self, subject, verb, object, frequency):
        self.subject = subject
        self.verb = verb
        self.object = object
        self.frequency = frequency

te.main()
extracted_triples = te.getTriples()
words_by_freq = te.getWordsByFreq()

triples = []
frequencies = {}
for e_triple in extracted_triples:
    triples.append(triple(e_triple[0][0], e_triple[0][1], e_triple[0][2], e_triple[1]))
    frequencies[(e_triple[0][0], e_triple[0][2])] = e_triple[1]

co_net, score = cn.find_best_network(triples, frequencies)

print("center:", {co_net.center}, "score:", score)

pos = nx.spring_layout(co_net.graph)
# Draw the graph
nx.draw(co_net.graph, pos, with_labels=True, node_color='skyblue', node_size=700, font_size=20)

# Show the plot
plt.show()
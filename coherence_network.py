import networkx as nx
import random

class coherence_network:
    def __init__(self, graph, center):
        self.graph = graph
        self.center = center

    def score():
        return
    
def next_connection(concepts, num_concepts, count, order, prev_concept, weight, G):
    next_concept = concepts[order[count[0]]]
    G.add_node(next_concept)
    G.add_edge(prev_concept, next_concept, weight=weight)

    count[0] += 1

    if count[0] < num_concepts and random.random() > 0.5:
        next_connection(concepts, num_concepts, count, order, next_concept, weight * 0.9, G)

    # 33% chance of continuing horizontally off the previous node
    while count[0] < num_concepts and random.random() < 0.33:
        next_connection(concepts, num_concepts, count, order, prev_concept, weight, G)

def build_network(concepts, num_concepts):
    G = nx.Graph()

    # Randomly mix up the order of concepts added to the network
    order = list(range(num_concepts))
    random.shuffle(order)

    # Add center
    center_concept = concepts[order[0]]
    G.add_node(center_concept)
    co_net = coherence_network(G, center_concept)

    # Tracking
    count = [1]  # to track count of concepts, as a list to update cross-function
    cont = 2  # Decides whether to continue or not at 80% chance, initialized to continue

    while count[0] < num_concepts and cont > 0:
        
        next_concept = concepts[order[count[0]]]
        G.add_node(next_concept)
        G.add_edge(center_concept, next_concept, weight=1)

        count[0] += 1

        # 67% chance to add a random node onto the last node
        while count[0] < num_concepts and random.random() > 0.33:
            next_connection(concepts, num_concepts, count, order, next_concept, 0.9, G)

        # 80% chance to continue
        cont = random.randint(0, 4)

    return co_net
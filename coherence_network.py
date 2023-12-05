import networkx as nx
import random
#import math

class coherence_network:
    def __init__(self, graph, center):
        self.graph = graph
        self.center = center

# adds next node and recursively calls at 50% chance, then out at 50% chance
def next_connection(triples, num_triples, td, prev_concept, concept, weight, G):
    
    if weight < .3:
        return
    
    num_to_add = random.randint(1, len(td[concept]))
    order = list(range(len(td[concept])))
    random.shuffle(order)

    #next_concept = concepts[order[count[0]]]
    #G.add_node(next_concept)
    
    for x in range(num_to_add):

        if not td[concept][order[x]] == prev_concept:

            G.add_edge(concept, td[concept][order[x]], weight = weight)

    #count[0] += 1

            if random.random() > 0.5:
                next_connection(triples, num_triples, td, concept, td[concept][order[x]], weight * 0.5, G)

    # 33% chance of continuing horizontally off the previous node
    #while count[0] < num_concepts and random.random() < 0.33:
    #    next_connection(concepts, num_concepts, count, order, prev_concept, weight, G)

# builds random coherence network from given concepts
def build_network(triples, triple_dict):
    
    G = nx.Graph()
    num_triples = len(triples)

    # Randomly mix up the order of concepts added to the network
    #top_20_percent = math.ceil((num_triples * .2))
    #order = list(range(top_20_percent))
    #random.shuffle(order)

    # Add center
    if random.random() > .5:
        center_concept = triples[(random.randint(0,int(num_triples * .2)))].subject
    else:
        center_concept = triples[(random.randint(0,int(num_triples * .2)))].object
    G.add_node(center_concept)
    co_net = coherence_network(G, center_concept)

    #order = list(range(num_triples))

    # Tracking
    #count = [1]  # to track count of concepts, as a list to update cross-function
    #cont = 2  # Decides whether to continue or not at 80% chance, initialized to continue

    num_to_add = random.randint(1, len(triple_dict[center_concept]))
    order = list(range(len(triple_dict[center_concept])))
    random.shuffle(order)

    for x in range(num_to_add):
        
        G.add_edge(center_concept, triple_dict[center_concept][order[x]], weight = 1)

        #next_concept = concepts[order[count[0]]]
        #G.add_node(next_concept)
        #G.add_edge(center_concept, next_concept, weight=1)

        #count[0] += 1

        # 67% chance to add a random node onto the last node
        if random.random() > 0.33:
            next_connection(triples, num_triples, triple_dict, center_concept, triple_dict[center_concept][order[x]], 0.5, G)

        # 80% chance to continue
        #cont = random.randint(0, 4)

    return co_net

# scores coherence of network 
def netwowk_score(graph, frequencies):
    score = 0
    # assuming frequencies is dictionary such that {(concept1, concept2) : frequency_of_ideas_in_triples}, score becomes sum of freuencies with wieght based on how far from center
    nodes_to_remove = []
    for edge in graph.edges:
        node1, node2 = edge
        if graph[node1][node2]['weight'] == 0:
            if node1 not in nodes_to_remove:
                nodes_to_remove.append(node1)
            if node2 not in nodes_to_remove:
                nodes_to_remove.append(node2)
        if (node1, node2) in frequencies:
            score += graph[node1][node2]['weight'] * frequencies[(node1, node2)]
        if (node2, node1) in frequencies:
            score += graph[node1][node2]['weight'] * frequencies[(node2, node1)]
    graph.remove_nodes_from(nodes_to_remove)
    return score

# adds edge to graph given tuple of 2 nodes
def add_t_edge(G, nodes):
    node1, node2 = nodes
    G.add_node(node1)
    G.add_node(node2)
    G.add_edge(node1, node2, weight = 0)

# helper function that recursively calls for give_weights
def rec_weights(G, node, prev_node, weight):
    nodes_to_remove = []
    for edge in G.edges(node):
        n1, n2 = edge
        if not (n1 == prev_node or n2 == prev_node):
            if G[n1][n2]['weight'] < weight:
                G[n1][n2]['weight'] = weight
                # find weights for next node
                if n1 == node:
                    nodes_to_remove.extend(rec_weights(G, n2, node, weight * .5))
                else:
                    nodes_to_remove.extend(rec_weights(G, n1, node, weight * .5))
    if weight == .25:
        nodes_to_remove.append(node)
    return nodes_to_remove

# give weights to edges based on location in network
def give_weights(network):
    nodes_to_remove = []
    for edge in network.graph.edges(network.center):
        n1, n2 = edge
        network.graph[n1][n2]['weight'] = 1
        # find weights for connceted nodes
        if n1 == network.center:
            nodes_to_remove = rec_weights(network.graph, n2, network.center, .5)
        else:
            nodes_to_remove = rec_weights(network.graph, n1, network.center, .5)
    for node in nodes_to_remove:
        if network.graph.has_node(node):
            network.graph.remove_node(node)
    return

# does crossover of networks
def crossover(parent1, parent2):
    G1 = nx.Graph()
    G2 = nx.Graph()
    edges1 = []
    edges2 = []
    for edge in parent1.graph.edges():
        edges1.append(edge)
    for edge in parent2.graph.edges():
        edges2.append(edge)
    # add first center edge to each to ensure center is carried correctly
    len1 = len(edges1)
    len2 = len(edges2)
    if len1 > 0:
        add_t_edge(G1, edges1[0])
    if len2 > 0:
        add_t_edge(G2, edges2[0])
    # add edges 80% p1->c1 and p2->c2 for each edge and 20% chance p1->c2 and p2->c1
    if len1 > len2:
        for x in range(1, len2):
            if random.random() > .2:
                add_t_edge(G1, edges1[x])
                add_t_edge(G2, edges2[x])
            else:
                add_t_edge(G1, edges2[x])
                add_t_edge(G2, edges1[x])
        # after all nodes in shorter graph used
        for x in range(len2, len1):
            if random.random() > .2:
                add_t_edge(G1, edges1[x])
            else:
                add_t_edge(G2, edges1[x])
    else:
        for x in range(1, len1):
            if random.random() > .2:
                add_t_edge(G1, edges1[x])
                add_t_edge(G2, edges2[x])
            else:
                add_t_edge(G1, edges2[x])
                add_t_edge(G2, edges1[x])
        # after all nodes in shorter graph used
        for x in range(len2, len1):
            if random.random() > .2:
                add_t_edge(G2, edges2[x])
            else:
                add_t_edge(G1, edges2[x])
    child1 = coherence_network(G1, parent1.center)
    child2 = coherence_network(G2, parent2.center)
    give_weights(child1)
    give_weights(child2)
    return(child1, child2)

#finds the best coherence network by randomlmy generating networks based off the triples, scoring them on their coherence and optimzing the best one with the genetic algorithm
def find_best_network(triples, frequencies, trip_dict):
    # make a list of concepts
    #concepts = []
    #for triple in triples:
    #    if triple.subject not in concepts:
    #        concepts.append(triple.subject)
    #    if triple.object not in concepts:
    #        concepts.append(triple.object)
    # find best coherence network
    best_network = None
    best_score = 0
    first = True
    networks = [] # tracks networks and score
    for x in range(100):
        # fills out preiouvsly held 40 networks
        if first:
            for y in range(80):
                for z in range(5):
                    network = build_network(triples, trip_dict)
                    score = netwowk_score(network.graph, frequencies)
                    if score > best_score:
                        best_network = network
                        best_score = score
                networks.append((best_network, best_score))
                best_score = 0
        # finds 10 new coherence networks
        for y in range(20):
            for z in range(5):
                network = build_network(triples, trip_dict)
                score = netwowk_score(network.graph, frequencies)
                if score > best_score:
                    best_network = network
                    best_score = score
            networks.append((best_network, best_score))
            best_score = 0
        random.shuffle(networks)
        # crossover
        next = []
        for y in range(50):
            children = crossover(networks[2 * y][0], networks[(2 * y) + 1][0])
            next.append(children[0])
            next.append(children[1])
        # find best 40 to cotinue next iteration
        networks = []
        for co_net in next:
            networks.append((co_net, netwowk_score(co_net.graph, frequencies)))
        networks = sorted(networks, key=lambda x: x[1])
        networks = networks[20:]
    return networks[79]
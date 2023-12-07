import networkx as nx
import random

# object that basically extends networkx graph by adding a tracker for which node is the center
class coherence_network:
    def __init__(self, graph, center):
        self.graph = graph
        self.center = center

# adds random number of edges to the node "concept"
def next_connection(td, prev_concept, concept, weight, G):
     # sets node depth at 3
    if weight < .3:
        return
    # randomly decide how many and which of the connections to add
    num_to_add = random.randint(1, len(td[concept]))
    order = list(range(len(td[concept])))
    random.shuffle(order)
    # add chosen edges to network
    for x in range(num_to_add):
        if not td[concept][order[x]] == prev_concept:
            G.add_edge(concept, td[concept][order[x]], weight = weight)
            # 50% chance to add further connections to each node that is being added
            if random.random() > 0.5:
                next_connection(td, concept, td[concept][order[x]], weight * 0.5, G)

# builds random coherence network from given triples
def build_network(triples, triple_dict): 
    G = nx.Graph()
    num_triples = len(triples)
    # Add center, randomly chosen from top 20% highest scoring triples, 50/50 chance of choosing the subject or object
    if random.random() > .5:
        center_concept = triples[(random.randint(0,int(num_triples * .2)))].subject
    else:
        center_concept = triples[(random.randint(0,int(num_triples * .2)))].object
    G.add_node(center_concept)
    co_net = coherence_network(G, center_concept)
    # randomly decide how many and which of the connections to add to the center node
    num_to_add = random.randint(1, len(triple_dict[center_concept]))
    order = list(range(len(triple_dict[center_concept])))
    random.shuffle(order)
    # add chosen edges
    for x in range(num_to_add):
        G.add_edge(center_concept, triple_dict[center_concept][order[x]], weight = 1)
        # 67% chance to connections to each node, edge weights decrease by half for each increase depth
        if random.random() > 0.33:
            next_connection(triple_dict, center_concept, triple_dict[center_concept][order[x]], 0.5, G)
    return co_net

# scores coherence of network based off distance from center and their frequency value, as well as prunes unconnected nodes
def netwowk_score(graph, frequencies):
    score = 0
    nodes_to_remove = []
    for edge in graph.edges:
        node1, node2 = edge
        # finds unconnected nodes to remove for pruning
        if graph[node1][node2]['weight'] == 0:
            if node1 not in nodes_to_remove:
                nodes_to_remove.append(node1)
            if node2 not in nodes_to_remove:
                nodes_to_remove.append(node2)
        # scores each node
        if (node1, node2) in frequencies:
            score += graph[node1][node2]['weight'] * frequencies[(node1, node2)]
        if (node2, node1) in frequencies:
            score += graph[node1][node2]['weight'] * frequencies[(node2, node1)]
    # prunes unconected nodes
    graph.remove_nodes_from(nodes_to_remove)
    return score

# adds edge to graph given tuple of 2 nodes
def add_t_edge(G, nodes):
    node1, node2 = nodes
    G.add_node(node1)
    G.add_node(node2)
    G.add_edge(node1, node2, weight = 0)

# helper function that recursively calls for give_weights, and prunes nodes of depth > 3
def rec_weights(G, node, prev_node, weight):
    nodes_to_remove = []
    for edge in G.edges(node):
        n1, n2 = edge
        if not (n1 == prev_node or n2 == prev_node):
            # check if this is the shortest path to this edge before updating weight
            if G[n1][n2]['weight'] < weight:
                G[n1][n2]['weight'] = weight
                # find weights for next node
                if n1 == node:
                    nodes_to_remove.extend(rec_weights(G, n2, node, weight * .5))
                else:
                    nodes_to_remove.extend(rec_weights(G, n1, node, weight * .5))
    # finds nodes that have depth > 3 for pruning
    if weight == .25:
        nodes_to_remove.append(node)
    return nodes_to_remove

# give weights to edges in network based on depth (starting from center node)
def give_weights(network):
    nodes_to_remove = []
    for edge in network.graph.edges(network.center):
        n1, n2 = edge
        # sets weight of depth 1 edges to 1
        network.graph[n1][n2]['weight'] = 1
        # sets the weights for edges that are of depth 2 and so on, decreasing weight by half as depth incereases by 1
        if n1 == network.center:
            nodes_to_remove = rec_weights(network.graph, n2, network.center, .5)
        else:
            nodes_to_remove = rec_weights(network.graph, n1, network.center, .5)
    # prune nodes of depth > 3
    for node in nodes_to_remove:
        if network.graph.has_node(node):
            network.graph.remove_node(node)
    return

# does crossover of 2 networks
def crossover(parent1, parent2):
    G1 = nx.Graph()
    G2 = nx.Graph()
    edges1 = []
    edges2 = []
    for edge in parent1.graph.edges():
        edges1.append(edge)
    for edge in parent2.graph.edges():
        edges2.append(edge)
    # add first center edge to each
    len1 = len(edges1)
    len2 = len(edges2)
    if len1 > 0:
        add_t_edge(G1, edges1[0])
    if len2 > 0:
        add_t_edge(G2, edges2[0])
    # add edges to child graphs, for each edge, pick an edge from each parent, 80% chance p1->c1 and p2->c2 for each edge and 20% chance p1->c2 and p2->c1
    if len1 > len2:
        # pick 1 for each until all edges in shorter graph are used up
        for x in range(1, len2):
            if random.random() > .2:
                add_t_edge(G1, edges1[x])
                add_t_edge(G2, edges2[x])
            else:
                add_t_edge(G1, edges2[x])
                add_t_edge(G2, edges1[x])
        # after all nodes in shorter graph used, 80% chance p1->c1, 20% p1->c2
        for x in range(len2, len1):
            if random.random() > .2:
                add_t_edge(G1, edges1[x])
            else:
                add_t_edge(G2, edges1[x])
    else:
        # pick 1 for each until all edges in shorter graph are used up
        for x in range(1, len1):
            if random.random() > .2:
                add_t_edge(G1, edges1[x])
                add_t_edge(G2, edges2[x])
            else:
                add_t_edge(G1, edges2[x])
                add_t_edge(G2, edges1[x])
        # after all nodes in shorter graph used, 80% chance p2->c2, 20% p2->c1
        for x in range(len2, len1):
            if random.random() > .2:
                add_t_edge(G2, edges2[x])
            else:
                add_t_edge(G1, edges2[x])
    child1 = coherence_network(G1, parent1.center)
    child2 = coherence_network(G2, parent2.center)
    # find weights of child graphs and prune node depth > 3
    give_weights(child1)
    give_weights(child2)
    return(child1, child2)

#finds the best coherence network by randomlmy generating networks based off the triples, scoring them on their coherence and optimzing the best one with the genetic algorithm
def find_best_network(triples, frequencies, trip_dict):
    best_network = None
    best_score = 0
    first = True
    networks = [] # tracks networks and score of each network
    #
    for x in range(100):
        # creates an initial 80 networks to add to population
        if first:
            for y in range(80):
                # creates 5 networks and runs a quick tourney to find the best one and adds that to the population
                for z in range(5):
                    network = build_network(triples, trip_dict)
                    score = netwowk_score(network.graph, frequencies)
                    if score > best_score:
                        best_network = network
                        best_score = score
                networks.append((best_network, best_score))
                best_score = 0
            first = False
        # creates 20 new coherence networks in each iteration, bringing population to 100
        for y in range(20):
            # creates 5 networks and runs a quick tourney to find the best one and adds that to the population
            for z in range(5):
                network = build_network(triples, trip_dict)
                score = netwowk_score(network.graph, frequencies)
                if score > best_score:
                    best_network = network
                    best_score = score
            networks.append((best_network, best_score))
            best_score = 0
        # create the next generation of networks by crossing over randomly paired up networks in the population
        random.shuffle(networks)
        next = []
        for y in range(50):
            children = crossover(networks[2 * y][0], networks[(2 * y) + 1][0])
            next.append(children[0])
            next.append(children[1])
        # find best 80 chldren to cotinue next iteration and eliminates 20 worst ones from gene pool
        networks = []
        for co_net in next:
            networks.append((co_net, netwowk_score(co_net.graph, frequencies)))
        networks = sorted(networks, key=lambda x: x[1])
        networks = networks[20:]
    # return highest scoring network
    return networks[79]
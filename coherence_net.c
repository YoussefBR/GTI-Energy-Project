#include <stddef.h>
#include <stdbool.h>
#include <stdio.h>

// node for each idea in file
typedef struct idea_node {
    char *concept;
    struct idea_node *connect_nodes;
} Node;

// struct for potential coherence network
typedef struct coherence_network{
    Node central_node;
    int file_id[]; // list of related files, will need to number files to keep track of them
} Network;

// struct representing tuple triples
typedef struct triple{
    char *subject;
    char *verb;
    char *object;
} Triple;

// determines if two nodes are positively or negatively related
bool isPositive(char verb[]) {
    return true;
}

// adds node
Node add_node(Node *node, char concept[]){
    Node newNode;
    newNode.concept = concept;
    node.connected_nodes = newNode;
}

/*
How we can build random coherence network:
    1. randomly select center
    2. randomly select node to connect to center
    3. random chance (50%?) to connect a node to this next node
    4. continue to randomly attempt to add on to next added node at 50% chance until fail
    5. on fail, go back to previous unfailed node and add at 75% chance
    6. run step 4 on new path until fail
    7. repeat steps 5-6 until back at center
    8. randomly add node to connect to center at 80%, stop if fail
    9. repeat until all nodes have been added (or fail on center add)
*/

// builds random coherence network
Network build_network(char *concepts[],  int num_concepts) {
    Network network;
    // randomly select center
    int rand_cent = rand() % num_concepts;
    Node center;
    center.concept = concepts[rand_cent];
    network.central_node = center;
    int count = 1;
    bool used [100];
    used[rand_cent] = true;
    // randomly add nodes to center
    while(count < num_concepts) {
        int rand_next = rand_cent;
        while(used[rand_next]) {
            int rand_next = rand() % num_concepts;
        }
        Node next;

        count += 1;

    }
}

// Coherence Network Algorithm: takes list of tuples and builds best coherence network based off of that
Network best_coherence(Triple file_triples[], int length){
    int best_score = 0; // score of best coherence nework
    Network best_network; // best coherence network, instantiated to central_node.concept = NULL in next line
    best_network.central_node.concept = NULL;
    Triple *postive_triples;
    Triple *negative_triples;
    // for each possible coherence network (brute force version)  WE NEED TO FIND A WAY TO FIND EACH POSSIBLE COHERENCE NETWORK
    for(int i = 0; i < sizeof(file_triples); i++) {
        if(isPositve(file_triples[i].verb)) {
            
        }
    }
        // find the score: int current score = network_score(current_network, files_tuples)
        // if score better than best score: if(current_score > best_score) {
            // make this network best newtork and score best score: best_score = current_score; best_network = current_work; }
}

// Coherence Network Scoring function: takes Network network and returns the score
int network_score(Network network, Triple *file_triples) {
    int score = 0;
    return score;
}
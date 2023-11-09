#include <stddef.h>
#include <stdbool.h>

// node for each idea in file
typedef struct idea_node {
    char *concept;
    struct idea_node *connect_nodes;
} Node;

// struct for potential coherence network
typedef struct coherence_network{
    Node central_node;
    int *file_id; // list of related files, will need to number files to keep track of them
} Network;

// struct representing tuple triples
typedef struct tuple{
    char *subject;
    char *verb;
    char *object;
} Tuple;

// determines if two nodes are positively or negatively related
bool isPositive(char verb[]) {
    return true;
}

// Coherence Network Algorithm: takes list of tuples and builds best coherence network based off of that
Network best_coherence(Tuple file_tuples[]){
    int best_score = 0; // score of best coherence nework
    Network best_network; // best coherence network, instantiated to central_node.concept = NULL in next line
    best_network.central_node.concept = NULL;
    Tuple *postive_tuples;
    Tuple *negative_tuples;
    // for each possible coherence network (brute force version)  WE NEED TO FIND A WAY TO FIND EACH POSSIBLE COHERENCE NETWORK
    for(int i = 0; i < sizeof(file_tuples); i++) {
        if(isPositve(file_tuples[i].verb)) {
            
        }
    }
        // find the score: int current score = network_score(current_network, files_tuples)
        // if score better than best score: if(current_score > best_score) {
            // make this network best newtork and score best score: best_score = current_score; best_network = current_work; }
}

// Coherence Network Scoring function: takes Network network and returns the score
int network_score(Network network, Tuple *file_tuples) {
    int score = 0;
    return score;
}
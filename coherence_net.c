
// node for each idea in file
typedef struct idea_node {
    char *concept;
    Node *connect_nodes;
} Node;

// struct for potential coherence network
typedef struct coherence_network{
    Node central_node;
    int* relatedFiles; // will need to number files to keep track of them
} Network;

// Coherence Network Algorithm: takes list of tuples and builds best coherence network based off of that


// Coherence Network Scoring function: takes Network network and returns the score
int network_score(Network network) {
    int score = 0;
    return score;
}
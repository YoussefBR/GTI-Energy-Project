
// node for each idea in file
typedef struct idea_node {
    char *concept;
    Node *connect_nodes;
} Node;

// struct for potential coherence network
typedef struct coherence_network{
    Node central_node;
} Network;

// Coherence Network Algorithm


// Coherence Network Score
int network_score(Network network) {
    int score = 0;
    return score;
}

// struct for each individual file
typedef struct file {
    Node *nodesList;
} File;

// node for each idea in file
typedef struct node {
    char *concept;
    Node *connectNodes;
} Node;

// Coherence Network Algorithm

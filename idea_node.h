#ifndef idea_node
#define idea_node

#include <stddef.h>

typedef struct node Node; 

// Edge structure
typedef struct {
    Node *node; // Pointer to the connected node
    double weight; // Weight of the edge
} Edge;

// Node structure
struct node {
    char *concept; // Pointer to the concept string
    Edge *edges; // Dynamic array of edges
    int num_edges; // Number of edges
    int edge_capacity; // Capacity of the edges array
};

// Function to initialize a node with a given concept
Node* create_node(const char* concept);

// Function to add an edge to a node
// might not need this function for the project 
int add_edge(Node* from, Node* to, double weight);

// Function to connect two nodes bidirectionally
int connect_nodes(Node* node1, Node* node2, double weight);

// Function to free a node
void free_node(Node* node);

#endif // GRAPH_H

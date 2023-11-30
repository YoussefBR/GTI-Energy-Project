#include <stddef.h>
#include <stdlib.h>
#include <string.h>

typedef struct node Node; 

// Edge structure
typedef struct {
    Node *node; 
    double weight; 
} Edge;

// Node structure
struct node {
    char *concept;
    Edge *edges; 
    int num_edges; 
    int edge_capacity; 
};

// Function to initialize a node
Node* create_node(const char* concept) {
    Node* new_node = malloc(sizeof(Node));
    if (!new_node) return NULL;

    new_node->concept = strdup(concept);
    new_node->num_edges = 0;
    new_node->edge_capacity = 10; // can be adjusted later 
    new_node->edges = malloc(new_node->edge_capacity * sizeof(Edge));
    if (!new_node->edges) {
        free(new_node);
        return NULL;
    }
    
    return new_node;
}

// Function to add an edge to a node
int add_edge(Node* from, Node* to, double weight) {
    if (from->num_edges >= from->edge_capacity) {
        // Need to resize the edges array
        int new_capacity = from->edge_capacity * 2;
        Edge* resized_edges = realloc(from->edges, new_capacity * sizeof(Edge));
        if (!resized_edges) {
            return -1; // Realloc failed
        }
        from->edges = resized_edges;
        from->edge_capacity = new_capacity;
    }
    
    // Add the new edge
    from->edges[from->num_edges].node = to;
    from->edges[from->num_edges].weight = weight;
    from->num_edges++;
    
    return 0; 
}

// Function to connect two nodes bidirectionally
int connect_nodes(Node* node1, Node* node2, double weight) {
    if (add_edge(node1, node2, weight) == -1) {
        return -1;
    }
    if (add_edge(node2, node1, weight) == -1) {
        // If adding the edge in the opposite direction fails, rollback the first edge
        // For simplicity, this rollback does not shrink the edges array if it was resized
        node1->num_edges--;
        return -1;
    }
    return 0;
}

// Function to free a node
void free_node(Node* node) {
    free(node->edges);
    free(node->concept);
    free(node);
}

// Free all nodes attached to the current node
void free_network(Node* node) {
    // get any attached nodes and then recursively call free_network on those
    // 
    free(node->edges);
    free(node->concept);
    free(node);
}

/* 
// Example of usage
int main() {
    Node* nodeA = create_node("Node A");
    Node* nodeB = create_node("Node B");
    
    if (connect_nodes(nodeA, nodeB, 0.75) == -1) {
        printf("Failed to connect Node A and Node B.\n");
        // Handle error, free nodes
    }
    
    // ... Use the graph
    
    // Clean up
    free_node(nodeA);
    free_node(nodeB);
    
    return 0;
}
*/
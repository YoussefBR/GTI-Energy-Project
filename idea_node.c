#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

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
    int visited; 
};

// Function to initialize a node
Node* create_node(const char* concept) {
    Node* new_node = malloc(sizeof(Node));
    if (!new_node) return NULL;

    new_node->concept = strdup(concept);
    new_node->num_edges = 0;
    new_node->edge_capacity = 10; // can be adjusted later 
    new_node->edges = malloc(new_node->edge_capacity * sizeof(Edge));
    new_node->visited = 0;
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
    printf("Freeing %s\n", node->concept);
    if (node == NULL) {
        return;
    }

    // Iterate over all edges of the node
    for (int i = 0; i < node->num_edges; i++) {
        Node* connected_node = node->edges[i].node;
        int j = 0;

        // Iterate over all edges of the connected node to find the back-reference
        while (j < connected_node->num_edges) {
            if (connected_node->edges[j].node == node) {
                // Move the last edge to this position to remove the back-reference
                connected_node->edges[j] = connected_node->edges[connected_node->num_edges - 1];
                connected_node->num_edges--;
                // Do not increment j as we need to check the newly moved edge
            } else {
                // Increment j only if no back-reference was found at the current position
                j++;
            }
        }
    }

    // free the node's own resources
    free(node->edges);
    free(node->concept);
    free(node);
}

// dfs function for the free_network function
static void dfs(Node* node, Node*** visited_nodes, int* visited_count, int* capacity) {
    if (node == NULL || node->visited) {
        return;
    }

    node->visited = 1;

    // check that there is enough room in the visited_nodes array
    if (*visited_count >= *capacity) {
        *capacity = *capacity > 0 ? *capacity * 2 : 1;
        *visited_nodes = realloc(*visited_nodes, *capacity * sizeof(Node*));
        if (!(*visited_nodes)) {
            perror("Failed to allocate memory for visited nodes");
            exit(EXIT_FAILURE);
        }
    }

    (*visited_nodes)[*visited_count] = node;
    (*visited_count)++;

    for (int i = 0; i < node->num_edges; i++) {
        dfs(node->edges[i].node, visited_nodes, visited_count, capacity);
    }
}

// free all nodes in the network
void free_network(Node* start_node) {
    Node** visited_nodes = NULL;
    int visited_count = 0, capacity = 0;

    // Start DFS from the start node
    dfs(start_node, &visited_nodes, &visited_count, &capacity);

    // Free all visited nodes
    for (int i = 0; i < visited_count; i++) {
        free_node(visited_nodes[i]);
    }

    // Free the list of visited nodes
    free(visited_nodes);
}


void print_edge_weights(const Node* node) {
    if (node == NULL) {
        printf("Node is NULL\n");
        return;
    }

    printf("Edge weights for node '%s':\n", node->concept);
    for (int i = 0; i < node->num_edges; i++) {
        printf("  Edge %d: Weight = %f\n", i, node->edges[i].weight);
    }
}

// Function to print the concepts of nodes connected to a given node
void print_connected_nodes(const Node* node) {
    if (node == NULL) {
        printf("Node is NULL\n");
        return;
    }

    printf("Connected concepts to node '%s':\n", node->concept);
    for (int i = 0; i < node->num_edges; i++) {
        printf("  Connected to: %s\n", node->edges[i].node->concept);
    }
}

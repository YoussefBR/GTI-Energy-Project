#include <stddef.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "idea_node.h"
#include "coherence_net.h"

/*
typedef struct node Node; 

// Edge structure
typedef struct {
    Node *node; 
    double weight; 
} Edge;

// Node structure
typedef struct node {
    char *concept;
    Edge *edges; 
    int num_edges; 
    int edge_capacity; 
} Node;

typedef struct coherence_network{
    // Node central_node;
    Node *central_node;
    int file_id[]; // list of related files, will need to number files to keep track of them
} Network;

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


void next_connection(char *concepts[], int num_concepts, int *count, int order[], Node *prev_node, double weight){
    Node *next = create_node(concepts[order[*count]]); // add_node(&prev_node, concepts[order[*count]]);
    connect_nodes(prev_node, next, weight);
    (*count)++;
    if(rand() % 2 > 0) {
        next_connection(concepts, num_concepts, count, order, next, weight * .9);
    }
    // 33% chance of continuing horizontally off of previous node
    while(*count < num_concepts && (rand() % 3) < 1) {
        next_connection(concepts, num_concepts, count, order, prev_node, weight);
    }
    return;
}

// builds random coherence network
Network *build_network(char *concepts[], int num_concepts) {
    Network *network; // this needs to be malloced maybe?
    // randomly mix up order of concepts added to network
    
    int order[num_concepts];// tracks the order that the concepts should be used i
    for(int i = 0; i < num_concepts; i++) {
        order[i] = i;
    }
    for(int i = 0; i < num_concepts; i++) { //  randomly orders concepts to be added to the network
        int switcher = rand() % num_concepts;
        int temp = order[i];
        order[i] = order[switcher];
        order[switcher] = temp;
    }
    // add center
    Node *center; // malloced maybe?
    center = create_node(concepts[order[0]]);
    network->central_node = center;
    // tracking
    int count = 1;
    // randomly add nodes to center
    int cont = 2; // decides whether to continue or not at 80% chance, initialized to continue
    while(count < num_concepts && cont > 0) {
        //Node next = add_node(center, concepts[order[count]]); // not sure if this will work as far as pointers
        Node *next = create_node(concepts[order[count]]);
        connect_nodes(center, next, 1);
        count++;
        // 67% chance to add random node on to last node
        while(count < num_concepts && (rand() % 3) > 0) {
            // count and used will need to be updated throughout different calls of functions so nt sure about pointer stuff there
            next_connection(concepts, num_concepts, &count, order, next, .9);
        }
        // 80% chance to continue
        cont = rand() % 5;
    }
    return network;
}
*/

int main(void) {
    char *concepts[] = {"pizza", "noodles", "pasta", "sauce", "tacos", "cheese", "beef", "lettuce", "beans", "chicken", "bacon", "stocks", "money", "trash", "a", "b", "cat", "dog", "pig", "bug", "ant", "bee", "wasp"};
    //printf("asdlasffl");
    //Node* node = create_node(concepts[0]);
    //printf("%s", node->concept);
    //free_node(node);
    //printf("%d", sp());
    Network *network = build_network(concepts, 23);
    printf("%s\n", network->central_node->concept);
    return 0;
}
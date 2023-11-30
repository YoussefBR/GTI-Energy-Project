#include <stddef.h>
#include <stdio.h>
#include "idea_node.h"



int main() {
    Node *nodeA = create_node("Node A");
    Node *nodeB = create_node("Node B");
    Node *nodeC = create_node("Node C");
    
    if (connect_nodes(nodeA, nodeB, 0.75) == -1) {
        printf("Failed to connect Node A and Node B.\n");
        // Handle error, free nodes
    }
    printf("Connected Node A and Node B.\n");
        if (connect_nodes(nodeA, nodeC, 1) == -1) {
        printf("Failed to connect Node A and Node C.\n");
        // Handle error, free nodes
    }
    printf("Connected Node A and Node C.\n");
    // ... Use the graph
    free_node(nodeC);
    printf("%c", nodeA->edges->node->concept);

    
    // Clean up
    free_node(nodeA);
    free_node(nodeB);
    
    return 0;
}
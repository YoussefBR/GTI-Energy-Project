#include <stddef.h>
#include <stdio.h>
#include "idea_node.h"



int main() {
    Node *nodeA = create_node("Node A");
    Node *nodeB = create_node("Node B");
    Node *nodeC = create_node("Node C");
    Node *nodeD = create_node("Node D");
    
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
    if (connect_nodes(nodeC, nodeD, 2) == -1) {
        printf("Failed to connect Node C and Node D.\n");
        // Handle error, free nodes
    }
    printf("Connected Node C and Node D.\n");
    // ... Use the graph
    // Clean up
    free_network(nodeA);
    print_connected_nodes(nodeC);
    return 0;
}
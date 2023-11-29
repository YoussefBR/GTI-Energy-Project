#include <stddef.h>
#include <stdbool.h>
#include <stdio.h>
#include "idea_node.h"

// struct for potential coherence network
typedef struct coherence_network{
    // Node central_node;
    Node *central_node;
    int file_id[]; // list of related files, will need to number files to keep track of them
} Network;

// struct representing tuple triples
typedef struct triple{
    char *subject;
    char *verb;
    char *object;
} Triple;

// determines if two nodes are positively or negatively related
bool isPositive(char verb[]);
// adds next node and recursively calls at 50% chance, then out at 50% chance
void next_connection(char *concepts[], int num_concepts, int *count, int order[], Node *prev_node, double weight);

int sp();

// builds random coherence network
Network *build_network(char *concepts[], int num_concepts);

// Coherence Network Algorithm: takes list of tuples and builds best coherence network based off of that
//Network best_coherence(Triple file_triples[], int length);

// Coherence Network Scoring function: takes Network network and returns the score
int network_score(Network network, Triple *file_triples);
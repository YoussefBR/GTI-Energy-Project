#include <stddef.h>
#include <stdbool.h>
#include <stdio.h>
#include "idea_node.h"
#include "coherence_net.h"

char *concepts[] = {"pizza", "noodles", "pasta", "sauce", "tacos", "cheese", "beef", "lettuce", "beans", "chicken", "bacon", "stocks", "money", "trash", "a", "b", "cat", "dog", "pig", "bug", "ant", "bee", "wasp"};

int main(void) {
    Network network = build_network(concepts, 23);
    printf("%s\n", network.central_node.concept);
    return 0;
}
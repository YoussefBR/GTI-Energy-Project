
// struct for each individual file
struct file {
    struct node *nodesList;
};

// node for each idea in file
struct node {
    char *concept;
    struct node *connectNodes;
};
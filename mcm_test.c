#include <stdio.h>
#include <limits.h>

#define INF INT_MAX  // Define infinity as the maximum integer value

// Function to initialize the graph with INF where no path is defined
void initialize_graph(int graph[][100], int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            graph[i][j] = INF;  // Set all edges to INF initially
        }
    }
}

// Function to add an edge to the graph (1-based indexing to 0-based)
void add_edge(int graph[][100], int u, int v, int w) {
    graph[u - 1][v - 1] = w;  // Adjust for 1-based index input
}

// Function to find the iteration bound and intermediate vectors
void find_iteration_bound_from_node(int graph[][100], int ref_node, int n) {
    int F[100][100];

    // Initialize DP table: F[0][ref_node] = 0, others are INF
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            F[i][j] = INF;
        }
    }
    F[0][ref_node - 1] = 0;  // Distance from the reference node to itself is 0

    // DP computation: F[m][j] = min(F[m-1][i] + w_ij)
    for (int m = 1; m <= n; m++) {
        for (int j = 0; j < n; j++) {
            // Carry forward the previous value as the starting point
            F[m][j] = F[m - 1][j];
            for (int i = 0; i < n; i++) {
                if (graph[i][j] != INF) {  // Check if there is an edge
                    int candidate = F[m - 1][i] + graph[i][j];
                    if (candidate < F[m][j]) {
                        F[m][j] = candidate;  // Update with the smaller value
                    }
                }
            }
        }
    }

    // Print intermediate vectors
    printf("\nIntermediate Vectors from Reference Node %d:\n", ref_node);
    for (int m = 0; m <= n; m++) {
        printf("m = %d: [", m);
        for (int v = 0; v < n; v++) {
            if (F[m][v] == INF) {
                printf(" inf ");
            } else {
                printf(" %d ", F[m][v]);
            }
        }
        printf("]\n");
    }

    // Compute the iteration bound (smallest cycle mean)
    int iteration_bound = INF;
    for (int v = 0; v < n; v++) {
        if (F[n][v] != INF) {
            for (int m = 0; m < n; m++) {
                if (F[m][v] != INF) {
                    // Calculate the cycle mean
                    int cycle_mean = (F[n][v] - F[m][v]) / (n - m);
                    if (cycle_mean < iteration_bound) {
                        iteration_bound = cycle_mean;
                    }
                }
            }
        }
    }

    printf("\nIteration Bound = %d\n", iteration_bound);
}

int main() {
    int n, e;

    // Input number of nodes and edges
    printf("Enter number of nodes and edges: ");
    scanf("%d %d", &n, &e);

    int graph[100][100];
    
    // Initialize the graph
    initialize_graph(graph, n);

    // Input edges (1-based indexing)
    printf("Enter edges (u v weight) [1-based index]:\n");
    for (int i = 0; i < e; i++) {
        int u, v, w;
        scanf("%d %d %d", &u, &v, &w);
        add_edge(graph, u, v, w);
    }

    // Input reference node
    int ref_node;
    printf("Enter reference node [1-based index]: ");
    scanf("%d", &ref_node);

    // Find iteration bound and intermediate vectors
    find_iteration_bound_from_node(graph, ref_node, n);

    return 0;
}

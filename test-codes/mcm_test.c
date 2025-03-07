#include <stdio.h>
#include <limits.h>

#define INF INT_MAX 

void graph_init(int graph[][100], int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            graph[i][j] = INF;  
        }
    }
}


void add_edge(int graph[][100], int u, int v, int w) {
    graph[u - 1][v - 1] = w;  
}

void iterationBound(int graph[][100], int ref_node, int n) {
    int F[100][100];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            F[i][j] = INF;
        }
    }
    F[0][ref_node - 1] = 0;

    for (int m = 1; m <= n; m++) {
        for (int j = 0; j < n; j++) {
            F[m][j] = F[m - 1][j];

            for (int i = 0; i < n; i++) {
                if (graph[i][j] != INF) {  
                    int candidate = F[m][i] + graph[i][j];          // m-1 -> m

                    if (candidate < F[m][j]) {            // Update if worse m-1 -> m
                        F[m][j] = candidate;  
                    }
                }

                // else {
                //     F[m][j] = INF;
                
                // }
            }
        }
    }

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

    int iteration_bound = INF;
    for (int v = 0; v < n; v++) {
        if (F[n][v] != INF) {
            for (int m = 0; m < n; m++) {
                if (F[m][v] != INF) {
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

    printf("Enter number of nodes and edges: ");
    scanf("%d %d", &n, &e);

    int graph[100][100];
    graph_init(graph, n);

    printf("edge data (SRC DST delay)\n");
    for (int i = 0; i < e; i++) {
        int u, v, w = 0;
        scanf("%d %d %d", &u, &v, &w);
        add_edge(graph, u, v, w);
    }

    // Input reference node
    int ref_node;
    printf("Ref node: ");
    scanf("%d", &ref_node);

    // Find iteration bound and intermediate vectors
    iterationBound(graph, ref_node, n);

    return 0;
}

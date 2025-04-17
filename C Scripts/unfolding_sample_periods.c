#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_INPUT_LEN 100
double parsing(const char* input) {
    char* slash = strchr(input, '/');
    if (slash != NULL) {
        double num = atof(input);
        double den = atof(slash + 1);
        if (den == 0.0) {
            fprintf(stderr, "Error: Division by zero in fraction.\n");
            exit(1);
        }
        return num / den;
    } else {
        return atof(input);
    }
}

int unfolding(double Tc, double Tclk, int max_j) {
    double min_diff = 1e9; 
    int closest_j = -1; 

    for (int j = 1; j <= max_j; ++j) {
        double Tcj = j * Tc;
        double Tclkj = fmax(ceil(Tcj), Tclk);
        double spj = Tclkj / j;

        printf("j = %d\tTcj = %.6f\tTclkj = %.6f\tspj = %.6f\n", j, Tcj, Tclkj, spj);

        if (fabs(spj - Tc) < min_diff) {
            min_diff = fabs(spj - Tc);
            closest_j = j;
        }

        if (fabs(spj - Tc) < 1e-6) {
            printf("\nSP = Tc at j = %d\n", j);
            return j;
        }
    }
    printf("\nNo value of j found where sample period equals Tc.\n");
    printf("Closest j is %d with spj ≈ %.6f\n", closest_j, Tc + (Tc < Tc + min_diff ? min_diff : -min_diff));
    return -1;
}

int main() {
    char input_Tc[MAX_INPUT_LEN];
    char input_Tclk[MAX_INPUT_LEN];

    printf("Iteration boun = ");
    fgets(input_Tc, sizeof(input_Tc), stdin);
    input_Tc[strcspn(input_Tc, "\n")] = 0; 

    printf("Clokc Period =  ");
    fgets(input_Tclk, sizeof(input_Tclk), stdin);
    input_Tclk[strcspn(input_Tclk, "\n")] = 0;

    double Tc = parsing(input_Tc);
    double Tclk = parsing(input_Tclk);

    unfolding(Tc, Tclk, 100);
    return 0;

}
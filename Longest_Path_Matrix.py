import numpy as np

def get_matrix_from_input():

    n = int(input("Enter the size of the matrix (n): "))
    print("Enter the matrix row by row, with space-separated values:")

    matrix = []

    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)

    return np.array(matrix, dtype=int)

def generate_matrices(L1, m):

    n = L1.shape[0]
    matrices = [L1]
    
    for _ in range(m):
        L_prev = matrices[-1]
        L_next = np.full((n, n), -1, dtype=int)
        
        for i in range(n):
            for j in range(n):
                max_val = -1

                for k in range(n):

                    if L1[i, k] != -1 and L_prev[k, j] != -1:
                        temp_val = L1[i, k] + L_prev[k, j]

                        if max_val == -1 or temp_val > max_val:
                            max_val = temp_val

                L_next[i, j] = max_val
        
        matrices.append(L_next)
    
    return matrices  

def compute_iteration_bound(matrices):
    n = matrices[0].shape[0]
    bound_values = []
    
    for t, matrix in enumerate(matrices, start=1):
        for i in range(n):
            if matrix[i, i] != -1:
                value = matrix[i, i] / t
                bound_values.append(value)
                # print(f"L{t+1}[{i},{i}] = {matrix[i, i]}, Divided by {t}: {value}")
    
    iteration_bound = max(bound_values) if bound_values else -1
    print("\nFinal Iteration Bound:", iteration_bound)
    return iteration_bound

def print_matrices(matrices):
    for idx, matrix in enumerate(matrices, start=2):
        print(f"\nMatrix L{idx-1}:")
        for row in matrix:
            print(" ".join(map(str, row)))

if __name__ == "__main__":
    L1 = get_matrix_from_input()
    m = int(input("Enter the number of matrices to generate (m): "))
    
    matrices = generate_matrices(L1, m)
    print_matrices(matrices)
    
    iteration_bound = compute_iteration_bound(matrices)
    print("\nIteration Bound:", iteration_bound)

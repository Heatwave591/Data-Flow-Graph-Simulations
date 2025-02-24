import numpy as np

def generate_matrices_fixed_final(R1, n):
    """
    Generate matrices R2 to Rn ensuring correct updates, particularly for the last row,
    while printing computation steps.
    
    Parameters:
    R1 (numpy.ndarray): Initial n×n matrix
    n (int): Size of the matrix
    
    Returns:
    list: List of matrices [R2, R3, ..., Rn]
    """
    matrices = [R1.copy()]

    for k in range(n):  # Floyd-Warshall iteration over intermediate vertices
        prev_matrix = matrices[-1]
        new_matrix = np.copy(prev_matrix)

        print(f"Computing R{k+2} using k={k+1}:")
        for u in range(n):
            for v in range(n):
                if prev_matrix[u, k] != np.inf and prev_matrix[k, v] != np.inf:
                    new_value = min(
                        prev_matrix[u, v],
                        prev_matrix[u, k] + prev_matrix[k, v]
                    )
                    if new_value != new_matrix[u, v]:
                        print(f"Updating R{k+2}[{u},{v}] from {new_matrix[u, v]} to {new_value}")
                    new_matrix[u, v] = new_value
        
        # Ensure proper calculation propagates naturally for the last row
        for v in range(n):
            if prev_matrix[-1, k] != np.inf and prev_matrix[k, v] != np.inf:
                new_value = min(prev_matrix[-1, v], prev_matrix[-1, k] + prev_matrix[k, v])
                if new_value != new_matrix[-1, v]:
                    print(f"Updating R{k+2}[{n-1},{v}] from {new_matrix[-1, v]} to {new_value}")
                new_matrix[-1, v] = new_value
        
        # Compare Rk and Rk+1
        if np.array_equal(prev_matrix, new_matrix):
            print(f"No updates in R{k+2}, continuing with k={k+1}.")
            k += 1
        
        matrices.append(new_matrix)
        print()

    return matrices[1:n+1]

# Define the input matrix
inf = np.inf
n = 6
R1 = np.array([
    [inf, inf,  3,   2,   2,   inf],
    [1,   inf,  1,   inf, inf, inf],
    [inf, inf,  inf, -1,  inf, inf],
    [inf, inf,  inf, inf, inf, inf],
    [inf, inf, -6,  -2,  inf, inf],
    [0,   0,   0,   0,   0,   inf]
])

# Generate matrices R2 to Rn with final correction
result_matrices_fixed_final = generate_matrices_fixed_final(R1, n)

# Print all matrices
for i, matrix in enumerate(result_matrices_fixed_final, start=2):
    print(f"Matrix R{i}:")
    for row in matrix:
        print("[" + ", ".join(["∞" if val == np.inf else str(int(val)) if val == int(val) else f"{val:.1f}" for val in row]) + "]")
    print()

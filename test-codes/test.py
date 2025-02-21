import numpy as np

def explain_matrix_calculation(L1: np.ndarray):
    """Demonstrates step-by-step matrix calculations with explanations"""
    n = L1.shape[0]
    print("Initial L1 Matrix:")
    print(L1)
    print("\nCalculating L2 Matrix:")
    
    L2 = np.full((n, n), -1)
    for i in range(n):
        for j in range(n):
            max_val = -1
            for k in range(n):
                if L1[i,k] != -1 and L1[k,j] != -1:
                    path_val = L1[i,k] + L1[k,j]
                    print(f"L2[{i},{j}] checking k={k}:")
                    print(f"  L1[{i},{k}] + L1[{k},{j}] = {L1[i,k]} + {L1[k,j]} = {path_val}")
                    max_val = max(max_val, path_val)
            L2[i,j] = max_val
            print(f"Final L2[{i},{j}] = {max_val}\n")
    
    print("Complete L2 Matrix:")
    print(L2)
    
    print("\nCalculating L3 Matrix:")
    L3 = np.full((n, n), -1)
    for i in range(n):
        for j in range(n):
            max_val = -1
            for k in range(n):
                if L1[i,k] != -1 and L2[k,j] != -1:
                    path_val = L1[i,k] + L2[k,j]
                    print(f"L3[{i},{j}] checking k={k}:")
                    print(f"  L1[{i},{k}] + L2[{k},{j}] = {L1[i,k]} + {L2[k,j]} = {path_val}")
                    max_val = max(max_val, path_val)
            L3[i,j] = max_val
            print(f"Final L3[{i},{j}] = {max_val}\n")
    
    print("Complete L3 Matrix:")
    print(L3)

# Example usage
L1 = np.array([[-1, 3],
               [3, -1]])

explain_matrix_calculation(L1)
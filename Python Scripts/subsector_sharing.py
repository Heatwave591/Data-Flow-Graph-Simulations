import numpy as np
import pandas as pd
from itertools import combinations

binary_coeffs = ['0011', '1010', '0111', '1111'] 

max_len = max(len(b) for b in binary_coeffs)
padded_binary = [b.zfill(max_len) for b in binary_coeffs]

# BIN to INT string
A = np.array([[int(bit) for bit in row] for row in padded_binary])

iteration = 1
while True:
    print(f"\nIteration {iteration}\n")
    all_groups = []

# Find sharing groups of rows
    for r in range(2, A.shape[0] + 1):
        for rows in combinations(range(A.shape[0]), r):
            subset = A[list(rows)]
            common_ones = np.sum(np.all(subset == 1, axis=0))
            all_groups.append((rows, common_ones))

    valid_groups = [g for g in all_groups if g[1] >= 2]
    if not valid_groups:
        break

    max_size = max(len(g[0]) for g in valid_groups)
    best_groups = [g[0] for g in valid_groups if len(g[0]) == max_size]

    print("max ones shared by")
    for group in best_groups:
        print(group)
        subset = A[list(group)]
        shared_positions = np.where(np.all(subset == 1, axis=0))[0]
        print(f"Shared ones = {shared_positions.tolist()}")

        Pn = np.bitwise_xor.reduce(A[list(group)], axis=0)
        print(f"Pn = {Pn.tolist()}")

        shared_mask = np.zeros(A.shape[1], dtype=bool)
        shared_mask[shared_positions] = True
        for idx in group:
            A[idx, shared_mask] = 0

        new_col = np.array([1 if i in group else 0 for i in range(A.shape[0])]).reshape(-1, 1)
        A = np.hstack((A, new_col))
        break  

    iteration += 1


print("\nFinal matrix\n")
num_input_bits = max_len
num_outputs = A.shape[1] - num_input_bits
column_names = [f"X{i}" for i in range(num_input_bits)] + [f"P{i+1}" for i in range(num_outputs)]
df = pd.DataFrame(A, columns=column_names)
print(df)
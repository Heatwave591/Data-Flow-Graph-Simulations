import numpy as np
import pandas as pd
from itertools import combinations

binary_coeffs = [
    "11101111",
    "11110001",
    "11100001",
    "10000001",
    "10010001",
    "10010111",
    "00010011",
    "00010001"
    ]

max_len = max(len(b) for b in binary_coeffs)
padded_binary = [b.zfill(max_len) for b in binary_coeffs]
A = np.array([[int(bit) for bit in row] for row in padded_binary])

iteration = 1
while True:
    print(f"\nIteration {iteration}\n")
    all_groups = []

    # Step 1: Find all row groups with ≥2 shared 1s
    for r in range(2, A.shape[0] + 1):
        for rows in combinations(range(A.shape[0]), r):
            subset = A[list(rows)]
            common_ones = np.sum(np.all(subset == 1, axis=0))
            if common_ones >= 2:
                all_groups.append((rows, common_ones))

    if not all_groups:
        break

    # Step 2: Pick the group with the most rows
    max_row_count = max(len(g[0]) for g in all_groups)
    best_groups = [g[0] for g in all_groups if len(g[0]) == max_row_count]

    print("Group with max rows that share ≥2 ones:")
    for group in best_groups:
        print(group)
        subset = A[list(group)]
        shared_positions = np.where(np.all(subset == 1, axis=0))[0]
        print(f"Shared positions: {shared_positions.tolist()}")

        print("Subset used for XOR:")
        print(subset)

        # Compute Pn from XOR
        Pn = np.bitwise_xor.reduce(subset, axis=0)
        print(f"Pn vector: {Pn.tolist()}")

        # Zero out shared 1s in group rows
        shared_mask = np.zeros(A.shape[1], dtype=bool)
        shared_mask[shared_positions] = True
        for idx in group:
            if not np.any(A[idx]):
                continue
            A[idx, shared_mask] = 0

        # ✅ Create new P column with 1s for participating rows
        pn_col = np.zeros((A.shape[0],), dtype=int)
        for idx in group:
            pn_col[idx] = 1
        A = np.hstack((A, pn_col.reshape(-1, 1)))
        break  # process only one group per iteration

    print("Matrix after iteration:")
    print(A)
    iteration += 1

# Final matrix output
print("\nFinal matrix\n")
num_input_bits = max_len
num_outputs = A.shape[1] - num_input_bits
column_names = [f"X{i}" for i in range(num_input_bits)] + [f"P{i+1}" for i in range(num_outputs)]
df = pd.DataFrame(A, columns=column_names)
print(df)
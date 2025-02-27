import numpy as np
import math

def generate_matrices(R1, n, t):

    matrices = [R1.copy()]
    
    if isinstance(t, (int, float)):
        t = np.full(n, t)

    for k in range(n):  
        prev_matrix = matrices[-1]
        new_matrix = np.copy(prev_matrix)

        for u in range(n):
            for v in range(n):
                if prev_matrix[u, k] != np.inf and prev_matrix[k, v] != np.inf:
                    new_value = min(
                        prev_matrix[u, v],
                        prev_matrix[u, k] + prev_matrix[k, v]
                    )
                    new_matrix[u, v] = new_value

        if np.array_equal(prev_matrix, new_matrix):
            k += 1

        matrices.append(new_matrix)
        print()

    return matrices[1:n+1]



inf = np.inf
n = 4
R1 = np.array([
    [inf, inf, 7, 15],
    [7, inf, inf, inf],
    [inf, -2, inf, inf],
    [inf, -2, inf, inf]
])

t = np.array([1, 1, 2, 2])  

result_matrices = generate_matrices(R1, n, t)

S = result_matrices[-1]
print("Matrix S (final matrix):")
for row in S:
    print("[" + ", ".join(["inf" if val == np.inf else str(int(val)) if val == int(val) else f"{val:.1f}" for val in row]) + "]\n ")


tmax = np.max(t)
M = tmax * n
print(f"tmax = {tmax}")
print(f"M = tmax * n = {tmax} * {n} = {M}")
print()

W = np.zeros((n, n))
D = np.zeros((n, n))

for u in range(n):
    for v in range(n):
        if u == v:
            W[u, v] = 0
            D[u, v] = t[u]
        else:
            if S[u, v] == np.inf:
                W[u, v] = np.inf
                D[u, v] = np.inf
            else:
                W[u, v] = math.ceil(S[u, v] / M)
                D[u, v] = (M * W[u, v] - S[u, v] + t[v])

print("Matrix W:")
for row in W:
    print("[" + ", ".join(["inf" if val == np.inf else str(int(val)) if val == int(val) else f"{val:.1f}" for val in row]) + "]")
print()

print("Matrix D:")
for row in D:
    print("[" + ", ".join(["inf" if val == np.inf else str(int(val)) if val == int(val) else f"{val:.1f}" for val in row]) + "]")
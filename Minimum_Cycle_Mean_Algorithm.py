from math import inf

def create_weight_matrix(u, edges):

    # Initialize all weights to infinity (including diagonal)
    W = [[inf] * u for _ in range(u)]
    
    # Fill in known edge weights
    for i, j, weight in edges:
        W[i-1][j-1] = weight
    
    return W

def compute_iteration_bound(F_vectors, u):

    # init Fu
    Fu = F_vectors[u]  
    min_max_ratio = inf
    
    # iteration bound math
    for m in range(u):
        Fm = F_vectors[m]
        max_ratio = -inf
        
        for i in range(u):
            if Fu[i] == inf or Fm[i] == inf:
                continue
                
            ratio = (Fu[i] - Fm[i])/(u-m)
            max_ratio = max(max_ratio, ratio)
        
        if max_ratio != -inf:
            min_max_ratio = min(min_max_ratio, max_ratio)
    return -min_max_ratio if min_max_ratio != inf else None

def compute_path_vectors(u, v, edges, r):

    # Create weight matrix W
    W = create_weight_matrix(u, edges)
    F_vectors = []
    F0 = [inf] * u

    #init reference node
    F0[r-1] = 0                             
    F_vectors.append(F0)
    
    # Fm math
    for m in range(1, u + 1):
        Fm = [inf] * u
        for j in range(u):
            min_distance = inf
            for i in range(u):
                if F_vectors[m-1][i] != inf and W[i][j] != inf:
                    distance = F_vectors[m-1][i] + W[i][j]
                    min_distance = min(min_distance, distance)
            Fm[j] = min_distance
        
        F_vectors.append(Fm)
    
    return F_vectors

def print_vectors(F_vectors):
    for m, vector in enumerate(F_vectors):
        formatted_vector = [str(x) if x != inf else '∞' for x in vector]
        print(f"F{m} = [{', '.join(formatted_vector)}]")

def print_weight_matrix(W):
    print("Weight Matrix W:")
    for row in W:
        formatted_row = [str(x) if x != inf else '∞' for x in row]
        print('[' + ', '.join(formatted_row) + ']')

def main():

    u = 3  # nodes 
    v = 4  # links
    edges = [
        (1, 2, 0),
        (2, 3, 0),
        (3, 1, -5),
        (2, 1, -5),
        (1, 1, -4)
    ]
    r = 1
    
    W = create_weight_matrix(u, edges)
    print_weight_matrix(W)
    print()
    
    F_vectors = compute_path_vectors(u, v, edges, r)
    print_vectors(F_vectors)
    print()
    

    T = compute_iteration_bound(F_vectors, u)
    if T is not None:
        print(f"Iteration bound T = {T}")

    else:
        print("Could not compute iteration bound (no valid ratios found)")

if __name__ == "__main__":
    main()
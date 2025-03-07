from math import inf
from itertools import combinations
from collections import defaultdict

def create_adjacency_matrix(u, edges):
    adj = [[0] * u for _ in range(u)]
    for i, j, _ in edges:
        adj[i-1][j-1] = 1
    return adj

def get_connected_components(adj_matrix, u):
    adj_list = defaultdict(list)
    for i in range(u):
        for j in range(u):
            if adj_matrix[i][j]:
                adj_list[i].append(j)
    
    def dfs(node, visited, component):
        visited[node] = True
        component.append(node + 1)  
        for next_node in adj_list[node]:
            if not visited[next_node]:
                dfs(next_node, visited, component)
    
    visited = [False] * u
    components = []
    
    for node in range(u):
        if not visited[node]:
            component = []
            dfs(node, visited, component)
            components.append(sorted(component))
    
    return components

def is_valid_split(graph, u, removed_edges):
    adj = [[0] * u for _ in range(u)]
    for i in range(u):
        for j in range(u):
            if graph[i][j] and (i+1, j+1) not in removed_edges:
                adj[i][j] = 1
    
    components = get_connected_components(adj, u)
    # Only return True if we get 2 or 3 components
    return 2 <= len(components) <= 3, adj, components

def is_feedforward(edges_subset):
    nodes_in = set()
    nodes_out = set()
    
    for edge in edges_subset:
        nodes_out.add(edge[0])
        nodes_in.add(edge[1])
    
    return len(nodes_in.intersection(nodes_out)) == 0

def get_subgraph_edges(adj_matrix, component):
    edges = []
    for i in component:
        for j in component:
            if adj_matrix[i-1][j-1]:  
                edges.append((i, j))
    return edges

def find_feedforward_cutsets(u, edges):
    adj_matrix = create_adjacency_matrix(u, edges)
    edge_tuples = [(i+1, j+1) for i in range(u) for j in range(u) if adj_matrix[i][j]]
    cutsets = []
    subgraphs = []
    
    for size in range(1, len(edge_tuples) + 1):
        for edge_combo in combinations(edge_tuples, size):
            is_valid, remaining_adj, components = is_valid_split(adj_matrix, u, edge_combo)
            
            if is_valid:
                remaining_edges = [(i, j) for i, j in edge_tuples if (i, j) not in edge_combo]
                if is_feedforward(remaining_edges):
                    cutsets.append(list(edge_combo))
                    subgraph_data = []
                    for component in components:
                        edges = get_subgraph_edges(remaining_adj, component)
                        subgraph_data.append({
                            'nodes': component,
                            'edges': edges
                        })
                    subgraphs.append(subgraph_data)
    
    return cutsets, subgraphs

def print_subgraph(subgraph, index):
    print(f"\nSubgraph {index}:")
    print(f"Nodes: {subgraph['nodes']}")
    print(f"Edges: {subgraph['edges']}")

def main():
    u = 3  # nodes 
    v = 4  # links
    edges = [
        (1, 2, 0),
        (2, 3, 0),
        (3, 4, 0),
        (3, 1, -5),
        (2, 1, -4),
        (4, 1, -5)
    ]
    
    print("Original graph edges:", edges)
    print("\nFinding feed forward cutsets that create 2 or 3 subgraphs...")
    
    cutsets, subgraphs = find_feedforward_cutsets(u, edges)
    
    if cutsets:
        print("\nFound feed forward cutsets and their resulting subgraphs:")
        for i, (cutset, subgraph_set) in enumerate(zip(cutsets, subgraphs), 1):
            print(f"\n{'='*50}")
            print(f"Cutset {i}:")
            print("Edges to remove:", cutset)
            print(f"Number of resulting subgraphs: {len(subgraph_set)}")
            print("\nResulting subgraphs after removing cutset:")
            for j, subgraph in enumerate(subgraph_set, 1):
                print_subgraph(subgraph, j)
    else:
        print("\nNo valid feed forward cutsets found that create 2 or 3 subgraphs.")

if __name__ == "__main__":
    main()
    
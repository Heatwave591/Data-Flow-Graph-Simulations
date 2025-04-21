class Node:
    def __init__(self, name, label, p):
        self.name = name
        self.label = label
        self.p = p

class DFGraph:
    def __init__(self, folding_factor):
        self.nodes = {}
        self.edges = []  # (source, dest, W)
        self.N = folding_factor

    def add_node(self, name, label, p):
        self.nodes[name] = Node(name, label, p)

    def add_edge(self, source, dest, W):
        self.edges.append((source, dest, W))

    def compute_DF(self):
        print(f"{'Source':<6} → {'Dest':<6} | {'DF':>4}")
        print("-" * 30)
        for source, dest, W in self.edges:
            u_node = self.nodes[source]
            v_node = self.nodes[dest]
            DF = (self.N * W) + v_node.label - u_node.label - u_node.p
            print(f"{source:<6} → {dest:<6} | {DF:>4}")

# ------------- Example ------------- #
if __name__ == "__main__":
    N = 4  # <-- Folding factor here!
    g = DFGraph(N)

    g.add_node("A1", 2, 1)
    g.add_node("A2", 3, 1)
    g.add_node("A3", 4, 1)
    g.add_node("A4", 0, 1)

    g.add_node("A5", 2, 1)
    g.add_node("A6", 1, 1)
    g.add_node("A7", 4, 1)
    g.add_node("A8", 3, 1)

    g.add_node("M1", 1, 2)
    g.add_node("M2", 0, 2)
    g.add_node("M3", 2, 2)
    g.add_node("M4", 0, 2)
    g.add_node("M5", 2, 2)

    g.add_node("M6", 3, 2)
    g.add_node("M7", 4, 2)
    g.add_node("M8", 3, 2)
    g.add_node("M9", 4, 2)

    # Add edges: (source, dest, W = number of delays)
    g.add_edge("A1", "2", 1)
    g.add_edge("A1", "5", 1)
    g.add_edge("A1", "6", 1)
    g.add_edge("A1", "7", 1)
    g.add_edge("A", "8", 2)
    g.add_edge("3", "1", 0)
    g.add_edge("5", "3", 0)
    g.add_edge("6", "4", 1)
    g.add_edge("7", "3", 1)
    g.add_edge("8", "4", 1)
    g.add_edge("4", "1", 0)



    g.compute_DF()
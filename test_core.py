import sys
import os
sys.path.append(os.getcwd())

try:
    import neuronet
    print("Module imported successfully.")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

def test_core():
    g = neuronet.NeuroNet()
    g.load_data("test_graph.txt")
    
    print(f"Nodes: {g.get_num_nodes()}")
    print(f"Edges: {g.get_num_edges()}")
    
    max_deg = g.get_max_degree_node()
    print(f"Max Degree Node: {max_deg}")
    
    # Check neighbors of 0
    neighbors = g.get_neighbors(0)
    print(f"Neighbors of 0: {neighbors}")
    
    # BFS from 0 depth 2
    edges = g.bfs(0, 2)
    print(f"BFS Edges (Start 0, Depth 2): {edges}")
    
    # Expected: 
    # Nodes: 8 (0 to 7)
    # Edges: 7
    # Max Degree: 0, 1, or 2 (all have out-degree 2). Implementation picks first one probably?
    # Neighbors of 0: [1, 2]
    # BFS Edges: (0,1), (0,2), (1,3), (1,4), (2,5), (2,6)

if __name__ == "__main__":
    test_core()

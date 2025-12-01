import tkinter as tk
from tkinter import filedialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import sys
import os

# Ensure we can import the compiled module from the current directory
sys.path.append(os.getcwd())

try:
    import neuronet
except ImportError:
    messagebox.showerror("Error", "Could not import 'neuronet' module. Please compile it first using 'python setup.py build_ext --inplace'.")
    sys.exit(1)

class NeuroNetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet: Massive Graph Analysis")
        self.root.geometry("1000x800")

        self.graph_engine = None
        self.loaded = False

        self._init_ui()

    def _init_ui(self):
        # Colors
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        accent_color = "#4a90e2"
        panel_color = "#3c3f41"
        active_color = "#357abd"
        
        self.root.configure(bg=bg_color)
        
        # Main Layout: Sidebar (Left) + Content (Right)
        main_container = tk.Frame(self.root, bg=bg_color)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = tk.Frame(main_container, bg=panel_color, width=250, padx=20, pady=20)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False) # Enforce width
        
        # Sidebar Content
        tk.Label(sidebar, text="NeuroNet", bg=panel_color, fg=accent_color, font=("Helvetica", 18, "bold")).pack(pady=(0, 20))
        
        # Dataset Section
        tk.Label(sidebar, text="Dataset", bg=panel_color, fg=fg_color, font=("Helvetica", 12, "bold")).pack(anchor="w")
        self.btn_load = tk.Button(sidebar, text="Load Edge List", command=self.load_dataset, bg=accent_color, fg=fg_color, activebackground=active_color, activeforeground=fg_color, relief="flat", padx=10, pady=5, borderwidth=0)
        self.btn_load.pack(fill=tk.X, pady=(5, 15))
        
        # Analysis Section
        tk.Label(sidebar, text="Analysis", bg=panel_color, fg=fg_color, font=("Helvetica", 12, "bold")).pack(anchor="w")
        
        tk.Label(sidebar, text="Start Node ID:", bg=panel_color, fg="#aaaaaa").pack(anchor="w", pady=(5, 0))
        self.entry_start = tk.Entry(sidebar, bg="#4e5254", fg=fg_color, insertbackground=fg_color, relief="flat")
        self.entry_start.pack(fill=tk.X, pady=2)
        
        tk.Label(sidebar, text="Max Depth:", bg=panel_color, fg="#aaaaaa").pack(anchor="w", pady=(5, 0))
        self.entry_depth = tk.Entry(sidebar, bg="#4e5254", fg=fg_color, insertbackground=fg_color, relief="flat")
        self.entry_depth.insert(0, "2")
        self.entry_depth.pack(fill=tk.X, pady=2)
        
        self.btn_bfs = tk.Button(sidebar, text="Run BFS", command=self.run_bfs, state=tk.DISABLED, bg="#555555", fg=fg_color, activebackground=active_color, activeforeground=fg_color, relief="flat", padx=10, pady=5, borderwidth=0)
        self.btn_bfs.pack(fill=tk.X, pady=(15, 5))
        
        # Stats in Sidebar
        tk.Label(sidebar, text="Statistics", bg=panel_color, fg=fg_color, font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(20, 5))
        self.lbl_stats = tk.Label(sidebar, text="No data loaded", bg=panel_color, fg="#aaaaaa", justify=tk.LEFT, wraplength=210)
        self.lbl_stats.pack(anchor="w")

        # Main Content Area
        content_area = tk.Frame(main_container, bg=bg_color)
        content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Status Bar (Top of content)
        self.lbl_status = tk.Label(content_area, text="Ready", bg=bg_color, fg="#aaaaaa", font=("Helvetica", 10, "italic"))
        self.lbl_status.pack(anchor="e", pady=(0, 10))
        
        # Canvas
        self.figure = plt.Figure(figsize=(8, 6), dpi=100, facecolor=bg_color)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(bg_color)
        
        # Style plot axes
        self.ax.spines['bottom'].set_color(fg_color)
        self.ax.spines['top'].set_color(fg_color) 
        self.ax.spines['right'].set_color(fg_color)
        self.ax.spines['left'].set_color(fg_color)
        self.ax.tick_params(axis='x', colors=fg_color)
        self.ax.tick_params(axis='y', colors=fg_color)
        self.ax.yaxis.label.set_color(fg_color)
        self.ax.xaxis.label.set_color(fg_color)
        self.ax.title.set_color(fg_color)

        self.canvas = FigureCanvasTkAgg(self.figure, content_area)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.get_tk_widget().configure(bg=bg_color, highlightthickness=0)

    def load_dataset(self):
        filename = filedialog.askopenfilename(title="Select Edge List File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not filename:
            return

        self.lbl_status.config(text="Loading data... Please wait.")
        self.root.update()

        try:
            start_time = time.time()
            self.graph_engine = neuronet.NeuroNet()
            self.graph_engine.load_data(filename)
            elapsed = time.time() - start_time

            num_nodes = self.graph_engine.get_num_nodes()
            num_edges = self.graph_engine.get_num_edges()
            
            mem_est = (num_nodes * 4 + num_edges * 4) / (1024 * 1024) # MB
            max_degree_node = self.graph_engine.get_max_degree_node()

            stats_text = f"Nodes: {num_nodes:,}\nEdges: {num_edges:,}\nTime: {elapsed:.4f}s\nEst. Mem: {mem_est:.2f} MB\nMax Degree Node: {max_degree_node}"
            self.lbl_stats.config(text=stats_text)
            self.lbl_status.config(text="Dataset Loaded Successfully")
            
            self.loaded = True
            self.btn_bfs.config(state=tk.NORMAL, bg="#4a90e2") # Enable with accent color
            
            self.entry_start.delete(0, tk.END)
            self.entry_start.insert(0, str(max_degree_node))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dataset: {e}")
            self.lbl_status.config(text="Error loading data")

    def run_bfs(self):
        if not self.loaded or not self.graph_engine:
            return

        try:
            start_node = int(self.entry_start.get())
            depth = int(self.entry_depth.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input for Start Node or Depth")
            return

        self.lbl_status.config(text="Running BFS...")
        self.root.update()

        try:
            start_time = time.time()
            edges = self.graph_engine.bfs(start_node, depth)
            elapsed = time.time() - start_time
            
            self.lbl_status.config(text=f"BFS Done. Found {len(edges)} edges in {elapsed:.4f}s. Drawing...")
            self.root.update()

            self.draw_subgraph(edges, start_node)
            
        except Exception as e:
            messagebox.showerror("Error", f"BFS Failed: {e}")
            self.lbl_status.config(text="Error in BFS")

    def draw_subgraph(self, edges, start_node):
        self.ax.clear()
        
        if not edges:
            self.ax.text(0.5, 0.5, "No edges found or start node has no neighbors.", ha='center', color='white')
            self.canvas.draw()
            return

        G = nx.Graph()
        G.add_edges_from(edges)

        if G.number_of_nodes() > 1000:
            self.ax.text(0.5, 0.5, f"Subgraph too large to visualize ({G.number_of_nodes()} nodes).", ha='center', color='white')
            self.canvas.draw()
            return

        pos = nx.spring_layout(G, seed=42)
        
        node_colors = ['#ff6b6b' if node == start_node else '#4ecdc4' for node in G.nodes()]
        
        nx.draw(G, pos, ax=self.ax, with_labels=True, node_size=300, node_color=node_colors, font_size=8, edge_color='#aaaaaa', font_color='white')
        self.ax.set_title(f"BFS Result (Start: {start_node})", color='white')
        
        self.canvas.draw()
        self.lbl_status.config(text="Visualization Complete")

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroNetApp(root)
    root.mainloop()

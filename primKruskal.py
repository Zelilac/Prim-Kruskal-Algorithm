import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

class MinimumSpanningTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prim and Kruskal Algorithms")

        self.graph_data = [
            ('A', 'B', 4),
            ('A', 'H', 8),
            ('B', 'H', 11),
            ('B', 'C', 8),
            ('C', 'I', 2),
            ('C', 'F', 4),
            ('H', 'G', 1),
            ('I', 'G', 6),
            ('I', 'F', 7),
            ('G', 'F', 2),
            ('C', 'D', 7),
            ('D', 'F', 14),
            ('D', 'E', 9),
            ('E', 'F', 10),
            # Tambahkan simpul dan sisi tambahan di sini
        ]

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white')
        self.canvas.pack()

        show_graph_button = tk.Button(self.root, text="Show Graph", command=self.show_graph)
        show_graph_button.pack()

        run_prim_button = tk.Button(self.root, text="Run Prim Algorithm", command=self.run_prim_algorithm)
        run_prim_button.pack()

        run_kruskal_button = tk.Button(self.root, text="Run Kruskal Algorithm", command=self.run_kruskal_algorithm)
        run_kruskal_button.pack()

        self.output_box = tk.Text(self.root, wrap=tk.WORD, width=80, height=10)
        self.output_box.pack()

    def draw_graph(self, graph):
        self.canvas.delete("all")  # Hapus gambar sebelumnya dari canvas
        G = nx.Graph()
        G.add_weighted_edges_from(graph)
        pos = nx.spring_layout(G, seed=42)  # Tetapkan posisi graf menggunakan spring_layout

        # Normalisasi posisi node agar berada di tengah canvas
        x_values, y_values = zip(*pos.values())
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)
        x_range = x_max - x_min
        y_range = y_max - y_min
        for node in pos:
            pos[node] = ((pos[node][0] - x_min) / x_range, (pos[node][1] - y_min) / y_range)

        # Gambar garis dan teks untuk node dan edge
        for u, v, weight in graph:
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            self.canvas.create_line(x1 * 600 + 100, y1 * 400 + 100, x2 * 600 + 100, y2 * 400 + 100)
            self.canvas.create_text((x1 * 600 + x2 * 600) / 2 + 100, (y1 * 400 + y2 * 400) / 2 + 100, text=str(weight))

        # Gambar node
        node_size = 50
        for node, (x, y) in pos.items():
            self.canvas.create_oval(x * 600 + 100 - node_size / 2, y * 400 + 100 - node_size / 2,
                                    x * 600 + 100 + node_size / 2, y * 400 + 100 + node_size / 2,
                                    fill='skyblue')
            self.canvas.create_text(x * 600 + 100, y * 400 + 100, text=node, font=("Arial", 12, "bold"))

    def show_graph(self):
        try:
            graph = [(x, y, weight) for (x, y, weight) in self.graph_data]
            self.draw_graph(graph)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_prim_algorithm(self):
        try:
            mst = self.calculate_mst("prim")
            if mst:
                mst_edges = [(u, v, data['weight']) for u, v, data in mst.edges(data=True)]
                self.display_output("Minimum Spanning Tree (Prim Algorithm):\n{}".format(mst_edges))
            else:
                self.display_output("Minimum Spanning Tree (Prim Algorithm): Tidak ada MST.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_kruskal_algorithm(self):
        try:
            mst = self.calculate_mst("kruskal")
            if mst:
                mst_edges = [(u, v, data['weight']) for u, v, data in mst.edges(data=True)]
                self.display_output("Minimum Spanning Tree (Kruskal Algorithm):\n{}".format(mst_edges))
            else:
                self.display_output("Minimum Spanning Tree (Kruskal Algorithm): Tidak ada MST.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calculate_mst(self, algorithm):
        G = nx.Graph()
        G.add_weighted_edges_from(self.graph_data)
        if algorithm == "prim":
            mst = nx.minimum_spanning_tree(G)
        elif algorithm == "kruskal":
            mst = nx.minimum_spanning_tree(G, algorithm='kruskal')
        else:
            raise ValueError("Invalid algorithm specified.")

        if nx.is_tree(mst):
            return mst
        else:
            return None

    def display_output(self, output_text):
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, output_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = MinimumSpanningTreeApp(root)
    root.mainloop()

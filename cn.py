import tkinter as tk
import math

class NetworkSim:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Network Simulator")
        self.root.geometry("800x600")

        self.nodes = []
        self.links = []
        self.topology = ""

        self.setup_ui()

    def setup_ui(self):
        control = tk.Frame(self.root, bg="#ddd", width=200)
        control.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(control, text="Topologies", font=("Arial", 13, "bold"), bg="#ddd").pack(pady=10)

        tk.Button(control, text="Star", width=14, command=self.star_topology).pack(pady=4)
        tk.Button(control, text="Ring", width=14, command=self.ring_topology).pack(pady=4)
        tk.Button(control, text="Mesh", width=14, command=self.mesh_topology).pack(pady=4)
        tk.Button(control, text="Bus", width=14, command=self.bus_topology).pack(pady=4)

        tk.Button(control, text="Clear", bg="#f9a825", width=14, command=self.clear_canvas).pack(pady=8)

        self.info = tk.Text(control, width=22, height=12)
        self.info.pack(pady=10)
        self.info.insert("1.0", "Select a topology.")

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def star_topology(self):
        self.clear_canvas()
        self.topology = "Star"

        center = self.add_node(400, 300, "Hub")
        positions = [(300, 200), (500, 200), (300, 400), (500, 400)]
        for i, pos in enumerate(positions):
            n = self.add_node(*pos, f"N{i+1}")
            self.connect(center, n)

        self.show_info("Star topology.\nAll nodes connect to central hub.")

    def ring_topology(self):
        self.clear_canvas()
        self.topology = "Ring"

        nodes = []
        for i in range(6):
            ang = 2 * math.pi * i / 6
            x, y = 400 + 150 * math.cos(ang), 300 + 150 * math.sin(ang)
            nodes.append(self.add_node(x, y, f"N{i+1}"))

        for i in range(6):
            self.connect(nodes[i], nodes[(i + 1) % 6])

        self.show_info("Ring topology.\nEach node linked to 2 neighbors.")

    def mesh_topology(self):
        self.clear_canvas()
        self.topology = "Mesh"

        pos = [(300, 200), (500, 200), (300, 400), (500, 400)]
        nodes = [self.add_node(x, y, f"M{i+1}") for i, (x, y) in enumerate(pos)]

        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                self.connect(nodes[i], nodes[j])

        self.show_info("Mesh topology.\nEach node connects to all others.")

    def bus_topology(self):
        self.clear_canvas()
        self.topology = "Bus"

        self.canvas.create_line(150, 300, 650, 300, width=4, fill="blue")

        for i in range(5):
            x = 200 + i * 100
            n = self.add_node(x, 200, f"B{i+1}")
            self.canvas.create_line(x, 200, x, 300, dash=(3, 2))

        self.show_info("Bus topology.\nAll share one backbone cable.")

    def add_node(self, x, y, label):
        node_circle = self.canvas.create_oval(x-18, y-18, x+18, y+18, fill="#90caf9", outline="#000", width=2)
        node_text = self.canvas.create_text(x, y, text=label, font=("Arial", 9))

        data = {'x': x, 'y': y, 'circle': node_circle, 'text': node_text, 'label': label, 'ok': True}
        self.nodes.append(data)

        self.canvas.tag_bind(node_circle, "<Button-1>", lambda e, n=data: self.toggle_node(n))
        self.canvas.tag_bind(node_text, "<Button-1>", lambda e, n=data: self.toggle_node(n))

        return data

    def connect(self, a, b):
        line = self.canvas.create_line(a['x'], a['y'], b['x'], b['y'], width=2)
        self.links.append({'line': line, 'a': a, 'b': b})

    def toggle_node(self, node):
        if node['ok']:
            self.canvas.itemconfig(node['circle'], fill="#ef5350")
            node['ok'] = False
            for link in self.links:
                if link['a'] == node or link['b'] == node:
                    self.canvas.itemconfig(link['line'], fill="red", dash=(3, 2))
        else:
            self.canvas.itemconfig(node['circle'], fill="#90caf9")
            node['ok'] = True
            for link in self.links:
                if link['a'] == node or link['b'] == node:
                    self.canvas.itemconfig(link['line'], fill="black", dash="")

        self.update_info()

    def update_info(self):
        total = len(self.nodes)
        active = sum(n['ok'] for n in self.nodes)
        down = total - active
        reliability = (active / total * 100) if total else 0

        txt = f"{self.topology} Topology\n\n"
        txt += f"Nodes: {total}\nActive: {active}\nDown: {down}\n"
        txt += f"Reliability: {reliability:.1f}%\n"
        txt += "\nClick nodes to toggle."

        self.show_info(txt)

    def show_info(self, msg):
        self.info.delete("1.0", tk.END)
        self.info.insert("1.0", msg)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.nodes.clear()
        self.links.clear()
        self.topology = ""
        self.show_info("Cleared. Choose a topology.")

if __name__ == "__main__":
    print("Launching network simulator...")
    app = NetworkSim()
    app.root.mainloop()

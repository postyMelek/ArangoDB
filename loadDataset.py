import networkx as nx

# Membuat graf terarah (directed graph)
G = nx.DiGraph()

# Baca file .txt
with open("amazon0302.txt", "r") as file:
    for line in file:
        if line.startswith("#"):  # Abaikan baris komentar
            continue
        source, target = map(int, line.strip().split())  # Pisahkan node asal dan tujuan
        G.add_edge(source, target)  # Tambahkan edge ke graf

print(f"Total Nodes: {G.number_of_nodes()}")
print(f"Total Edges: {G.number_of_edges()}")
# import networkx as nx
# from arango import ArangoClient
# from dotenv import load_dotenv
# import os
# from networkx.algorithms.community import greedy_modularity_communities

# load_dotenv()

# ARANGO_HOST = os.getenv("ARANGO_HOST")
# ARANGO_USERNAME = os.getenv("ARANGO_USERNAME")
# ARANGO_PASSWORD = os.getenv("ARANGO_PASSWORD")
# ARANGO_DB_NAME = os.getenv("ARANGO_DB_NAME")

# client = ArangoClient(hosts=ARANGO_HOST)
# db = client.db(ARANGO_DB_NAME, username=ARANGO_USERNAME, password=ARANGO_PASSWORD)

# def load_graph_from_arango():
#     G = nx.DiGraph()
#     for p in db.aql.execute("FOR p IN products RETURN p"):
#         G.add_node(p["_key"])
#     for e in db.aql.execute("FOR e IN co_purchases RETURN e"):
#         from_node = e["_from"].split("/")[-1]
#         to_node = e["_to"].split("/")[-1]
#         G.add_edge(from_node, to_node)
#     return G

# def get_top_influencers(G, top_n=5):
#     pagerank_scores = nx.pagerank(G)
#     sorted_scores = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)
#     return sorted_scores[:top_n]

# def recommend_products(G, product_id, top_n=5):
#     neighbors = list(G.successors(product_id))[:top_n]
#     return neighbors

# def detect_anomaly(G, threshold=0.2):
#     pagerank_scores = nx.pagerank(G)
#     mean_score = sum(pagerank_scores.values()) / len(pagerank_scores)
#     anomalies = [node for node, score in pagerank_scores.items() if abs(score - mean_score) > threshold]
#     return anomalies
# def load_graph_from_arango():
#     G = nx.DiGraph()
#     for p in db.aql.execute("FOR p IN products RETURN p"):
#         G.add_node(p["_key"])
#     for e in db.aql.execute("FOR e IN co_purchases RETURN e"):
#         from_node = e["_from"].split("/")[-1]
#         to_node = e["_to"].split("/")[-1]
#         G.add_edge(from_node, to_node)
#     return G

# def get_subgraph_context(G, product_id, radius=2):
#     subgraph = nx.ego_graph(G, product_id, radius=radius, center=True, undirected=False)
#     nodes = list(subgraph.nodes())
#     edges = list(subgraph.edges())
    
#     context = {
#         "product_id": product_id,
#         "related_products": nodes,
#         "relationships": edges
#     }
#     return context


# def get_subgraph(G, product_id, radius=2):
#     return nx.ego_graph(G, product_id, radius=radius)

# def get_communities(G):
#     return list(greedy_modularity_communities(G))

# def get_top_influencers(G, top_n=5):
#     pagerank = nx.pagerank(G)
#     return sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:top_n]
import networkx as nx
from arango import ArangoClient
from dotenv import load_dotenv
import os
from networkx.algorithms.community import greedy_modularity_communities

load_dotenv()

ARANGO_HOST = os.getenv("ARANGO_HOST")
ARANGO_USERNAME = os.getenv("ARANGO_USERNAME")
ARANGO_PASSWORD = os.getenv("ARANGO_PASSWORD")
ARANGO_DB_NAME = os.getenv("ARANGO_DB_NAME")

client = ArangoClient(hosts=ARANGO_HOST)
db = client.db(ARANGO_DB_NAME, username=ARANGO_USERNAME, password=ARANGO_PASSWORD)

def load_subgraph():
    """Load Subgraph dari ArangoDB (Optimized for Speed)"""
    G = nx.DiGraph()

    query_nodes = db.aql.execute("FOR p IN products LIMIT 300 RETURN p")
    for p in query_nodes:
        G.add_node(p["_key"])

    query_edges = db.aql.execute("FOR e IN co_purchases LIMIT 1000 RETURN e")
    for e in query_edges:
        from_node = e["_from"].split("/")[-1]
        to_node = e["_to"].split("/")[-1]
        G.add_edge(from_node, to_node)

    return G

def get_top_influencers(G, top_n=5):
    """Menghitung PageRank buat cari influencer"""
    pagerank_scores = nx.pagerank(G)
    sorted_scores = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[:top_n]

def get_subgraph(G, product_id, radius=2):
    """Ambil subgraph/ego graph dari node tertentu"""
    return nx.ego_graph(G, product_id, radius=radius)

def get_communities(G):
    """Deteksi komunitas di graph"""
    return list(greedy_modularity_communities(G))

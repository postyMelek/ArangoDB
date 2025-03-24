from langchain.tools import Tool
from graph_analysis import (
    load_graph_from_arango,
    get_top_influencers,
    recommend_products,
    detect_anomaly
)
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from collections import Counter

G = load_graph_from_arango()

def co_purchase_query_tool(query: str) -> str:
    try:
        product_id = query.split()[-1]
        recs = recommend_products(G, product_id, top_n=5)
        return (f"Pelanggan yang membeli produk **{product_id}** sering juga membeli produk berikut: "
                f"{', '.join(recs)}. Rekomendasi bundling produk ini untuk meningkatkan penjualan cross-sell.")
    except Exception as e:
        return f"Gagal menjalankan co-purchase analysis: {str(e)}"

def influencer_tool(query: str) -> str:
    influencers = get_top_influencers(G, top_n=5)
    response = "**Top 5 Produk Influencer di jaringan co-purchase:**\n\n"
    for prod_id, score in influencers:
        response += f"- Produk {prod_id} dengan PageRank {score:.4f}\n"
    response += "\n➡️ Produk ini memiliki pengaruh tinggi dalam network dan disarankan sebagai anchor promo."
    return response

def anomaly_tool(query: str) -> str:
    anomalies = detect_anomaly(G)
    return (f"Produk berikut terdeteksi **anomali** dalam jaringan pembelian:\n"
            f"{', '.join(anomalies[:5])}\n\n➡️ Perlu investigasi lebih lanjut, "
            f"kemungkinan adanya lonjakan atau penurunan pembelian yang tidak biasa.")

def strategic_advisor_tool(query: str) -> str:
    # Parsing product id (contoh dummy)
    product_ids = [id.strip() for id in query.split() if id.isdigit()][:2]

    if len(product_ids) < 2:
        return "Masukkan minimal 2 produk untuk analisis strategi!"

    bundles = []
    next_products = []
    for pid in product_ids:
        next_products.extend(list(G.successors(pid)))

    counts = Counter(next_products)
    recommended_bundles = counts.most_common(3)

    communities = list(greedy_modularity_communities(G))

    # Check spender
    def check_high_spender(products, communities):
        for idx, community in enumerate(communities):
            if all(pid in community for pid in products):
                depths = []
                for pid in community:
                    lengths = nx.single_source_shortest_path_length(G, pid)
                    depths.append(max(lengths.values()) if lengths else 0)
                avg_depth = sum(depths) / len(depths)
                return True if avg_depth > 5 else False, idx, avg_depth
        return False, None, 0

    spender, community_idx, avg_depth = check_high_spender(product_ids, communities)

    # Build descriptive response
    response = f"📦 Pelanggan membeli produk {product_ids[0]} dan {product_ids[1]}.\n\n"

    if recommended_bundles:
        response += "**Rekomendasi Bundling Produk:**\n"
        for bundle in recommended_bundles:
            response += f"- Produk {bundle[0]} (muncul {bundle[1]} kali)\n"
        response += "\n➡️ Disarankan tawarkan bundling dengan diskon 10%-15%.\n"

    response += f"\n👥 Masuk dalam komunitas produk: {community_idx} dengan rata-rata depth {avg_depth}."

    if spender:
        response += "\n💰 Pelanggan ini **High Spender**! Dorong upsell produk premium."
    else:
        response += "\n🧐 Pelanggan ini termasuk **mid spender**. Berikan promosi dasar dan monitoring lanjutan."

    return response

tools = [
    Tool(name="Co-Purchase Tool", func=co_purchase_query_tool, description="Cek produk yang sering dibeli bersamaan."),
    Tool(name="Influencer Tool", func=influencer_tool, description="Cek influencer produk di jaringan graf."),
    Tool(name="Anomaly Detection Tool", func=anomaly_tool, description="Cek produk anomali."),
    Tool(name="Strategic Advisor Tool", func=strategic_advisor_tool, description="Beri rekomendasi strategi marketing berdasarkan pembelian produk user.")
]

import streamlit as st
import pandas as pd
import networkx as nx
from graph_analysis import load_graph_from_arango
from networkx.algorithms.community import greedy_modularity_communities

st.set_page_config(page_title="👥 Customer Segmentation & Spender Analysis", layout="wide")

st.title("👥 Customer Segmentation & Spender Targeting")

# ===========================================
# 🔄 LOAD GRAPH DATA
# ===========================================
with st.spinner("Memuat graph dari ArangoDB..."):
    G = load_graph_from_arango()

st.success(f"✅ Graph berhasil dimuat! Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

# ===========================================
# 🔧 SEGMENTASI KOMUNITAS (Produk = Segmentasi Customer)
# ===========================================
st.subheader("📊 Segmentasi Komunitas Produk (Proxy Customer Group)")

communities = list(greedy_modularity_communities(G))
num_communities = len(communities)

st.info(f"📌 Ditemukan {num_communities} komunitas produk!")

# Tampilkan komunitas tertentu
selected_community_idx = st.selectbox("Pilih Komunitas Index", list(range(num_communities)))

selected_community = list(communities[selected_community_idx])
st.write(f"Produk dalam Komunitas {selected_community_idx}:")
st.table(pd.DataFrame({"Product ID": selected_community[:20]}))

# ===========================================
# 🎯 TARGET HIGH SPENDER BASED ON CHAIN DEPTH
# ===========================================
st.subheader("💰 High Spender Produk (Berdasarkan Rantai Pembelian Panjang)")

# Cari node dengan longest path traversal ➡️ asumsikan user suka beli berantai
longest_paths = {}
for node in selected_community[:50]:  # Limit biar gak berat
    lengths = nx.single_source_shortest_path_length(G, node)
    max_depth = max(lengths.values()) if lengths else 0
    longest_paths[node] = max_depth

# Urutkan berdasarkan kedalaman traversal
sorted_spenders = sorted(longest_paths.items(), key=lambda x: x[1], reverse=True)

top_spender_df = pd.DataFrame(sorted_spenders, columns=["Product ID", "Max Purchase Depth"])
st.table(top_spender_df.head(10))

st.success("✅ High Spender Produk ditemukan berdasarkan kedalaman traversal pembelian.")

# ===========================================
# 📈 VISUALISASI JARINGAN SEGMENTASI
# ===========================================
st.subheader("📈 Visualisasi Komunitas Produk (Proxy Customer Segment)")

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
subgraph = G.subgraph(selected_community[:50])  # limit 50 node
pos = nx.spring_layout(subgraph, seed=42)
nx.draw(subgraph, pos, with_labels=True, node_color='skyblue', node_size=800, edge_color='gray')
plt.title(f"Komunitas Produk {selected_community_idx}")
st.pyplot(plt)

# ===========================================
# 📝 INSIGHT DAN REKOMENDASI
# ===========================================
st.subheader("📝 Insight & Rekomendasi Strategi Marketing")

if sorted_spenders:
    top_product = sorted_spenders[0][0]
    max_depth = sorted_spenders[0][1]

    st.markdown(f"""
    - 🎯 Produk **{top_product}** memiliki kedalaman pembelian **{max_depth}**, artinya kemungkinan besar pembeli produk ini adalah **high spender**.
    - 🚀 Rekomendasi: **Target diskon atau bundling premium** untuk komunitas produk ini.
    - 📦 Bundling dengan produk lain di komunitas {selected_community_idx}.
    """)
else:
    st.warning("⚠️ Tidak ada data spender yang valid ditemukan.")

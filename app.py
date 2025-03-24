import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import requests
from dotenv import load_dotenv
import os

# Load environment variable dari .env
load_dotenv()

# DISCORD webhook URL
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Import modul internal
from graph_analysis import (
    load_graph_from_arango,
    get_top_influencers,
    recommend_products,
    detect_anomaly
)
from ai_insights import generate_business_insight
from agent_core import create_hybrid_agent, hybrid_query_agent, feedback_loop

# ===========================================
# 🚀 CONFIG & INITIALIZATION
# ===========================================
st.set_page_config(page_title="Marketing Dashboard - Agentic App", layout="wide")
st.title("📈 Agentic Marketing Strategy Dashboard")

# ===========================================
# 🔧 SIDEBAR CONTROLS
# ===========================================
product_id = st.sidebar.text_input("Masukkan Product ID", "1")
top_n_recs = st.sidebar.slider("Jumlah Rekomendasi", 1, 10, 5)

# ===========================================
# 🔄 LOAD GRAPH DATA
# ===========================================
with st.spinner("Memuat graph dari ArangoDB..."):
    G = load_graph_from_arango()

st.success(f"✅ Graph berhasil dimuat! Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

# ===========================================
# 🔥 INISIALISASI AGENT (HARUS SETELAH GRAPH DIMUAT!)
# ===========================================
agent = create_hybrid_agent(G)

# ===========================================
# 🤖 LangChain Hybrid Query Agent
# ===========================================
st.sidebar.subheader("🤖 LangChain Hybrid Query Agent")

user_query = st.sidebar.text_input("Tanyakan sesuatu ke Agent:", "Siapa influencer terbaik?")

if st.sidebar.button("Run Hybrid Agent with Gemini"):
    result = agent.run(user_query)
    st.sidebar.success("✅ Agent Response:")
    st.sidebar.info(result)

# ===========================================
# 🗣️ FEEDBACK LOOP SIMULASI
# ===========================================
st.subheader("🗣️ Feedback Kamu")

feedback_col1, feedback_col2 = st.columns(2)

with feedback_col1:
    if st.button("👍 Suka Rekomendasi Ini"):
        feedback_loop(product_id, "like")
        st.success("Feedback disimpan! Agent akan belajar.")

with feedback_col2:
    if st.button("👎 Tidak Suka Rekomendasi Ini"):
        feedback_loop(product_id, "dislike")
        st.warning("Feedback disimpan. Agent akan memperbaiki rekomendasi.")

# ===========================================
# 🔝 TOP INFLUENCER PRODUCTS
# ===========================================
st.subheader("🔥 Top Influencer Produk")
influencers = get_top_influencers(G)
st.table(influencers)

# ===========================================
# 👥 INFLUENCER GRAPH VISUALIZATION
# ===========================================
st.subheader("👥 Visualisasi Influencer Graph")

plt.figure(figsize=(10, 8))
H = G.subgraph([node for node in influencers["Product ID"]])
pos = nx.spring_layout(H, seed=42)

nx.draw(H, pos, with_labels=True, node_size=500, node_color='lightgreen')
plt.title("Influencer Graph - Produk Kunci dalam Jaringan Co-Purchase")
st.pyplot(plt)

with st.expander("Penjelasan Influencer Graph"):
    st.markdown("""
    - Titik node menunjukkan produk.
    - Panah edge menunjukkan hubungan co-purchase (produk A ➡️ produk B).
    - Produk di pusat graf adalah key influencer yang mampu menarik pembelian produk lainnya.
    - Cluster terpisah menunjukkan segmentasi user atau komunitas pembeli berbeda.
    """)

# ===========================================
# 🎯 REKOMENDASI PRODUK
# ===========================================
st.subheader(f"🎯 Rekomendasi Produk untuk {product_id}")

recommendations = recommend_products(G, product_id, top_n=top_n_recs)
st.table(recommendations)

with st.expander("Penjelasan Rekomendasi Produk"):
    st.markdown("""
    Produk-produk yang disarankan karena sering dibeli bersama dengan produk utama.  
    Rekomendasi berdasarkan analisis directed graph Amazon Co-Purchase.
    """)

# ===========================================
# 🧠 BUSINESS INSIGHT (GEMINI AI)
# ===========================================
st.subheader("🧠 Insight Bisnis oleh Gemini AI")

insight = generate_business_insight(product_id, recommendations)
st.success(insight)

# ===========================================
# 🚨 ANOMALY DETECTION & DISCORD ALERT
# ===========================================
st.sidebar.subheader("🚨 Smart Alerts / Anomaly Detection")

anomalies = detect_anomaly(G)

if anomalies:
    alert_message = f"⚠️ Anomali terdeteksi di Produk: {', '.join(anomalies[:5])}"

    action_plan = generate_action_plan(anomalies[:5])

    discord_message = f"{alert_message}\n\n🚀 **Recommended Action Plan:**\n{action_plan}"

    st.sidebar.warning(alert_message)
    st.sidebar.info(f"🚀 Action Plan:\n{action_plan}")

    status = send_discord_alert(discord_message)
    if status == 204:
        st.sidebar.success("✅ Alert dan Action Plan dikirim ke Discord!")
    else:
        st.sidebar.error("❌ Gagal mengirim alert ke Discord.")
else:
    st.sidebar.success("✅ Tidak ada anomali saat ini!")

# ===========================================
# 🚫 NEGATIVE RECOMMENDATIONS (Produk Dihindari)
# ===========================================
st.subheader("⚠️ Produk yang Disarankan Untuk Dihindari")

def avoid_products(G, pagerank_threshold=0.005):
    pagerank_scores = nx.pagerank(G)
    avoid = [node for node, score in pagerank_scores.items() if score < pagerank_threshold]
    return avoid

low_influence_products = avoid_products(G, pagerank_threshold=0.005)

st.table(pd.DataFrame({
    "Product ID": low_influence_products[:10],
    "Reason": ["Low Influence / Low Centrality"] * len(low_influence_products[:10])
}))

with st.expander("Penjelasan Produk Dihindari"):
    st.markdown("""
    Produk dengan pengaruh rendah (Low PageRank),  
    tidak efektif dalam cross-sell / upsell dan berpotensi menyebabkan churn pelanggan.
    """)

# ===========================================
# 🚀 ACTION PLAN SUMMARY
# ===========================================
st.subheader("🚀 Action Plan Final")

action_plan_final = generate_action_plan_final(product_id, recommendations, low_influence_products)

st.markdown(f"""
**Call to Action:**
{action_plan_final}
""")

discord_message_final = f"🚀 **Final Action Plan Summary**\n\n{action_plan_final}"

status = send_discord_alert(discord_message_final)

if status == 204:
    st.success("✅ Action Plan dikirim ke Discord!")
else:
    st.error("❌ Gagal mengirim Action Plan ke Discord!")

# ===========================================
# 💡 UTILITY FUNCTIONS
# ===========================================
def send_discord_alert(message):
    """Kirim notifikasi ke Discord via Webhook"""
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    return response.status_code

def generate_action_plan(anomalies):
    plans = []
    for product_id in anomalies:
        plans.append(f"- 🚨 Diskon 20% untuk produk {product_id}")
        plans.append(f"- 🚀 Push campaign cross-sell untuk produk {product_id} minggu ini")
        plans.append(f"- 🔎 QC Review produk {product_id} untuk perbaikan kualitas")
    return "\n".join(plans)

def generate_action_plan_final(product_id, recommendations, low_influence_products):
    plans = []
    plans.append(f"- 🎯 Diskon 10% untuk produk {product_id}.")
    if len(recommendations) > 0:
        bundle_products = ", ".join(recommendations["Product ID"])
        plans.append(f"- 📦 Bundling produk {product_id} dengan {bundle_products}.")
    if len(low_influence_products) > 0:
        review_products = ", ".join(low_influence_products[:5])
        plans.append(f"- 🔍 Review produk {review_products} untuk potensi churn atau perbaikan kualitas.")
    return "\n".join(plans)

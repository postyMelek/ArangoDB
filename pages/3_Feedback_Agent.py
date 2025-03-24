import streamlit as st
from agent_core import feedback_loop
from graph_analysis import load_graph_from_arango, recommend_products
from ai_insights import generate_business_insight
from utils import send_discord_alert

# Set page config
st.set_page_config(page_title="🗣️ Feedback Learning Agent", layout="wide")

st.title("🗣️ Feedback Learning Agent")

# ===========================================
# 🔄 LOAD GRAPH DATA
# ===========================================
with st.spinner("Memuat graph dari ArangoDB..."):
    G = load_graph_from_arango()

st.success(f"✅ Graph berhasil dimuat! Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

# ===========================================
# 🔧 SIDEBAR CONTROLS (PRODUCT SELECTION)
# ===========================================
product_id = st.sidebar.text_input("Masukkan Product ID", "1")
top_n_recs = st.sidebar.slider("Jumlah Rekomendasi", 1, 10, 5)

# ===========================================
# 🎯 REKOMENDASI PRODUK BERDASARKAN SELEKSI
# ===========================================
st.subheader(f"🎯 Rekomendasi Produk untuk {product_id}")

recommendations = recommend_products(G, product_id, top_n=top_n_recs)
st.table(recommendations)

# ===========================================
# 🧠 INSIGHT DARI GEMINI
# ===========================================
insight = generate_business_insight(product_id, recommendations)
st.info(f"🧠 Insight Gemini:\n\n{insight}")

# ===========================================
# 🗣️ FEEDBACK LOOP BUTTONS
# ===========================================
st.subheader("Berikan Feedback ke Agent")

feedback_col1, feedback_col2 = st.columns(2)

with feedback_col1:
    if st.button("👍 Suka Rekomendasi Ini"):
        feedback_loop(product_id, "like")
        st.success("Feedback diterima! Agent akan belajar dari input ini.")

with feedback_col2:
    if st.button("👎 Tidak Suka Rekomendasi Ini"):
        feedback_loop(product_id, "dislike")
        st.warning("Feedback diterima. Agent akan evaluasi ulang rekomendasi.")

# ===========================================
# 🚀 ACTION PLAN DARI FEEDBACK
# ===========================================
st.subheader("🚀 Action Plan Berdasarkan Feedback")

# Ini cuma simulasi action plan dari feedback, bisa diimprove pakai RL nanti
action_plan = f"""
📦 Produk utama: {product_id}  
🎯 Diskon 10% di minggu depan  
📈 Promosikan ke user cluster loyal berdasarkan feedback positif  
"""

st.markdown(action_plan)

# Kirim ke Discord
if st.button("Kirim Action Plan ke Discord"):
    status = send_discord_alert(f"🚀 Feedback Action Plan:\n\n{action_plan}")
    if status == 204:
        st.success("✅ Action Plan berhasil dikirim ke Discord!")
    else:
        st.error("❌ Gagal mengirim Action Plan ke Discord!")

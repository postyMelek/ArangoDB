import streamlit as st
from graph_analysis import load_graph_from_arango, recommend_products
from ai_insights import generate_business_insight
from utils import send_discord_alert

st.set_page_config(page_title="🎯 Recommender Agent")

st.title("🎯 Product Recommender Agent")

with st.spinner("Memuat graph..."):
    G = load_graph_from_arango()

product_id = st.text_input("Masukkan Product ID", "1")
top_n = st.slider("Jumlah Rekomendasi", 1, 10, 5)

if st.button("Generate Recommendation"):
    recommendations = recommend_products(G, product_id, top_n)
    st.table(recommendations)

    insight = generate_business_insight(product_id, recommendations)
    st.info(f"🧠 Gemini Insight:\n\n{insight}")

    action_plan = f"Bundling produk {product_id} dengan {', '.join(recommendations['Product ID'])}"
    discord_message = f"🚀 Rekomendasi Produk Baru:\n\n{action_plan}"

    send_discord_alert(discord_message)
    st.success("✅ Rekomendasi dikirim ke Discord!")

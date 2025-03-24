import streamlit as st
from graph_analysis import load_graph_from_arango, detect_anomaly
from utils import send_discord_alert, generate_action_plan

st.title("🚨 Anomaly Detection Agent")

with st.spinner("Memuat graph..."):
    G = load_graph_from_arango()

st.success("Graph loaded!")

if st.button("Deteksi Anomali"):
    anomalies = detect_anomaly(G)

    if anomalies:
        st.warning(f"⚠️ Anomali di Produk: {anomalies[:5]}")

        action_plan = generate_action_plan(anomalies[:5])
        st.info(f"🚀 Recommended Action Plan:\n\n{action_plan}")

        send_discord_alert(action_plan)
        st.success("✅ Action Plan dikirim ke Discord!")
    else:
        st.success("✅ Tidak ada anomali ditemukan.")

import requests
import os

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_alert(message):
    """Kirim notifikasi ke Discord via Webhook"""
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    return response.status_code

def generate_action_plan(anomalies):
    plans = []
    for product_id in anomalies:
        plans.append(f"- 🚨 Diskon 20% untuk produk {product_id}")
        plans.append(f"- 🚀 Push campaign cross-sell untuk produk {product_id}")
        plans.append(f"- 🔎 QC Review produk {product_id}")
    return "\n".join(plans)

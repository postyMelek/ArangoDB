import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

def generate_business_insight(product_id, recommendations):
    rec_list = ", ".join(recommendations["Product ID"])
    prompt = f"Produk {product_id} sering dibeli bersama produk berikut: {rec_list}. Apa strategi pemasaran terbaik?"
    response = model.generate_content(prompt)
    return response.text

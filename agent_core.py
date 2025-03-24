# import networkx as nx
# from graph_analysis import (
#     get_top_influencers,
#     recommend_products,
#     detect_anomaly
# )
# from langchain.agents import initialize_agent, AgentType,  tool
# from langchain.tools import Tool
# from gemini_langchain import GeminiLLM
# from graph_analysis import get_top_influencers, get_subgraph, get_communities, load_graph_from_arango



# from ai_insights import generate_business_insight

# # Feedback memory (basic RL simulation)
# feedback_memory = {}
# # Inisialisasi Gemini LangChain LLM
# llm = GeminiLLM()

# def create_hybrid_agent(G):
#     llm = GeminiLLM()

#     tools = [
#         Tool(
#             name="Influencer Tool",
#             func=lambda q: str(get_top_influencers(G, 5)),
#             description="Dapatkan daftar influencer produk."
#         ),
#         Tool(
#             name="Recommender Tool",
#             func=lambda q: str(recommend_products(G, "1", top_n=5)),
#             description="Dapatkan rekomendasi frequently bought together."
#         ),
#     ]

#     return initialize_agent(
#         tools=tools,
#         llm=llm,
#         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         verbose=True
#     )

# def hybrid_query_agent(user_query, G):
#     """
#     Hybrid agent untuk otomatis memilih strategi query dan reasoning.
#     """
#     response = ""

#     # Simple decision tree - bisa upgrade pakai LangChain agent!
#     if "influencer" in user_query.lower():
#         influencers = get_top_influencers(G)
#         response += "Top Influencer Produk:\n"
#         response += str(influencers.head(5))

#         insight = generate_business_insight("Influencers", influencers)
#         response += f"\n\nStrategi Marketing oleh Gemini:\n{insight}"

#     elif "rekomendasi" in user_query.lower():
#         product_id = extract_product_id(user_query)
#         recommendations = recommend_products(G, product_id, top_n=5)
#         response += f"Rekomendasi Produk untuk Produk {product_id}:\n"
#         response += str(recommendations)

#     elif "anomali" in user_query.lower():
#         anomalies = detect_anomaly(G)
#         if anomalies:
#             response += f"Anomali Ditemukan di Produk: {anomalies[:5]}"
#         else:
#             response += "Tidak ada anomali ditemukan."

#     else:
#         # Default ke Gemini AI reasoning
#         response += "Gemini Insight:\n"
#         insight = generate_business_insight("Generic Query", [])
#         response += insight

#     return response

# def extract_product_id(query):
#     """
#     Dummy Extractor → bisa pakai NLP atau Regex yang lebih canggih.
#     """
#     return query.strip().split()[-1]

# def feedback_loop(product_id, feedback):
#     """
#     Simulasi feedback loop → memperbarui prioritas rekomendasi.
#     """
#     if product_id not in feedback_memory:
#         feedback_memory[product_id] = {"likes": 0, "dislikes": 0}

#     if feedback == "like":
#         feedback_memory[product_id]["likes"] += 1
#     else:
#         feedback_memory[product_id]["dislikes"] += 1

#     print(f"[Feedback Memory] {product_id} -> {feedback_memory[product_id]}")
# # Tools
# def get_influencers_tool(query):
#     # Buat output rapi
#     top = get_top_influencers(G, top_n=5)
#     return f"Top Influencer Produk:\n{top}"

# def get_recommendation_tool(query):
#     return f"Rekomendasi Produk:\n{recommend_products(G, '1', top_n=5)}"
# def create_planner_agent():
#     llm = GeminiLLM()  # asumsi wrapper Gemini LLM udah jalan
#     agent = initialize_agent(
#         tools=tools,
#         llm=llm,
#         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         verbose=True
#     )
#     return agent
# tools = [
#     Tool(
#         name="Influencer Tool",
#         func=get_influencers_tool,
#         description="Gunakan ini untuk mendapatkan daftar influencer produk."
#     ),
#     Tool(
#         name="Recommender Tool",
#         func=get_recommendation_tool,
#         description="Gunakan ini untuk mendapatkan rekomendasi produk frequently bought together."
#     ),
# ]

# # Inisialisasi LangChain Agent dengan Gemini
# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )


# @tool
# def influencer_tool(query: str):
#     """Dapatkan daftar top influencer dari graph menggunakan PageRank."""
#     influencers = get_top_influencers(G, 5)
#     return f"Top influencers: {influencers}"

# @tool
# def subgraph_tool(query: str):
#     """Ambil subgraph dari produk tertentu berdasarkan query."""
#     product_id = query.split()[-1]
#     subG = get_subgraph(G, product_id)
#     return f"Subgraph nodes: {list(subG.nodes())}, edges: {list(subG.edges())}"

# @tool
# def community_tool(query: str):
#     """Deteksi komunitas dalam graph menggunakan algoritma modularitas."""
#     communities = get_communities(G)
#     return f"Detected {len(communities)} communities."

# tools = [
#     Tool(name="Influencer Tool", func=influencer_tool, description="Get top influencer products."),
#     Tool(name="Subgraph Tool", func=subgraph_tool, description="Retrieve product subgraph."),
#     Tool(name="Community Tool", func=community_tool, description="Detect product communities.")
# ]


from langchain.agents import initialize_agent, AgentType, tool
from langchain.tools import Tool
from gemini_langchain import GeminiLLM
from graph_analysis import get_top_influencers, get_subgraph, get_communities

@tool
def influencer_tool(query: str):
    """Top influencer produk dari graph."""
    influencers = get_top_influencers(load_subgraph(), 5)
    return f"Influencers: {influencers}"

@tool
def subgraph_tool(query: str):
    """Ambil subgraph dari produk tertentu."""
    subG = get_subgraph(load_subgraph(), query.strip().split()[-1])
    return f"Nodes: {list(subG.nodes())}"

tools = [
    Tool(name="Influencer Tool", func=influencer_tool, description="Get influencers."),
    Tool(name="Subgraph Tool", func=subgraph_tool, description="Get subgraph.")
]

def create_planner_agent():
    llm = GeminiLLM()
    return initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

# import streamlit as st
# from graph_analysis import load_graph_from_arango, get_top_influencers
# from graph_visualization import (
#     visualize_graph_pyvis,
#     visualize_influencer_graph,
#     visualize_subgraph,
#     visualize_community_graph
# )
# from agent_core import create_planner_agent

# st.set_page_config(page_title="🤖 Agentic Dashboard", layout="wide")

# st.title("🤖 Agentic App - GraphRAG + LangGraph + Feedback Loop")

# @st.cache_resource(show_spinner=True)
# def cached_load_graph():
#     return load_graph_from_arango()

# @st.cache_resource(show_spinner=True)
# def cached_create_agent():
#     return create_planner_agent()

# G = cached_load_graph()
# agent = cached_create_agent()

# # Visualization Controls
# st.header("📈 Graph Visualization")
# view_option = st.radio("Pilih graph view:", ["Influencer Graph", "Subgraph", "Community Graph"])

# if st.button("🔄 Tampilkan Graph"):
#     if view_option == "Influencer Graph":
#         influencers = get_top_influencers(G)
#         visualize_influencer_graph(G, influencers)
#     elif view_option == "Subgraph":
#         product_id = st.text_input("Masukkan Product ID", "1")
#         visualize_subgraph(G, product_id)
#     elif view_option == "Community Graph":
#         visualize_community_graph(G)

# # LangChain Planner Chat
# st.header("🤖 LangChain Planner Agent Chat")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     st.chat_message(message["role"]).write(message["content"])

# query = st.chat_input("Masukkan pertanyaan ke Agent...")

# if query:
#     st.chat_message("user").write(query)
#     with st.spinner("Agent lagi mikir..."):
#         response = agent.run(query)

#     st.chat_message("assistant").write(response)

#     st.session_state.messages.append({"role": "user", "content": query})
#     st.session_state.messages.append({"role": "assistant", "content": response})

import streamlit as st
from graph_analysis import load_subgraph, get_top_influencers
from graph_visualization import visualize_graph_cytoscape
from agent_core import create_planner_agent


st.set_page_config(page_title="🚀 Agentic GraphRAG App", layout="wide")
st.title("🚀 GraphRAG + LangGraph + ArangoDB")

@st.cache_resource
def cached_graph():
    return load_subgraph()

@st.cache_resource
def cached_agent():
    return create_planner_agent()

G = cached_graph()
agent = cached_agent()

# Visualization Section
st.header("📈 Graph Visualization")
if st.button("Tampilkan Influencer Graph"):
    influencers = get_top_influencers(G, 5)
    sub_nodes = [node for node, _ in influencers]
    subG = G.subgraph(sub_nodes)
    visualize_graph_cytoscape(subG)

# Chat Agent Section
st.header("🤖 Planner Agent Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

query = st.chat_input("Tanya Agent...")

if query:
    st.chat_message("user").write(query)
    with st.spinner("Agent mikir..."):
        response = agent.run(query)

    st.chat_message("assistant").write(response)

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": response})

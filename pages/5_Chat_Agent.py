import streamlit as st
from graphrag_agent import graph_rag_pipeline

st.set_page_config(page_title="🤖 GraphRAG Chat Agent", layout="wide")

st.title("🤖 GraphRAG-powered Marketing Strategy Chat Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).write(content)

user_query = st.chat_input("Masukkan pertanyaan kamu...")

if user_query:
    st.chat_message("user").write(user_query)
    
    # Extract product ID dari user query (simple parser)
    product_id = ''.join(filter(str.isdigit, user_query)) or "1"
    
    with st.spinner("🔍 GraphRAG Agent lagi mikir..."):
        response = graph_rag_pipeline(user_query, product_id)
    
    st.chat_message("assistant").write(response)
    
    # Save history
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.session_state.messages.append({"role": "assistant", "content": response})

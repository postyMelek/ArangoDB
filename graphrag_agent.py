from gemini_langchain import GeminiLLM
from graph_analysis import load_graph_from_arango, get_subgraph_context

G = load_graph_from_arango()

def graph_rag_pipeline(user_query: str, product_id: str):
    # Step 1: Retrieve Subgraph Context
    subgraph_context = get_subgraph_context(G, product_id, radius=2)
    
    # Step 2: Compose Context for LLM
    context_prompt = f"""
    Produk utama yang dianalisis: {subgraph_context['product_id']}
    
    Produk terkait dalam radius 2 hop: {subgraph_context['related_products']}
    
    Hubungan co-purchase antar produk tersebut: {subgraph_context['relationships']}
    
    ➡️ Berikan analisis strategi pemasaran, rekomendasi bundling, 
    potensi high spender, dan peluang campaign yang relevan berbasis data tersebut.
    """
    
    # Step 3: LLM Reasoning & Generation
    llm = GeminiLLM()
    response = llm._call(context_prompt)
    
    return response

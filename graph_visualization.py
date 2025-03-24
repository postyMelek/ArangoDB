import networkx as nx
from pyvis.network import Network
import streamlit as st
from networkx.algorithms.community import greedy_modularity_communities


import streamlit as st
import streamlit_cytoscapejs as st_cyto

def visualize_graph_cytoscape(G, layout='cose'):
    nodes = [{"data": {"id": node, "label": node}} for node in G.nodes()]
    edges = [{"data": {"source": u, "target": v}} for u, v in G.edges()]

    st_cyto.st_cytoscapejs(
        elements=nodes + edges,
        layout={"name": layout},
        style={'width': '100%', 'height': '600px'},
    )

def visualize_graph_pyvis(G, title="Graph Visualization"):
    net = Network(height='600px', width='100%', bgcolor='#222222', font_color='white')

    for node in G.nodes():
        net.add_node(node, label=str(node))

    for source, target in G.edges():
        net.add_edge(source, target)

    net.save_graph('graph.html')
    with open('graph.html', 'r', encoding='utf-8') as HtmlFile:
        components = HtmlFile.read()
        st.components.v1.html(components, height=650)

def visualize_influencer_graph(G, influencers):
    net = Network(height='600px', width='100%', bgcolor='#222222', font_color='white')

    influencer_ids = [node for node, _ in influencers]

    for node in G.nodes():
        color = 'red' if node in influencer_ids else 'gray'
        size = 30 if node in influencer_ids else 10
        net.add_node(node, label=str(node), color=color, size=size)

    for edge in G.edges():
        net.add_edge(edge[0], edge[1])

    net.save_graph('graph.html')
    with open('graph.html', 'r', encoding='utf-8') as HtmlFile:
        components = HtmlFile.read()
        st.components.v1.html(components, height=650)

def visualize_subgraph(G, product_id, radius=2):
    subG = nx.ego_graph(G, product_id, radius=radius)
    net = Network(height='600px', width='100%', bgcolor='#222222', font_color='white')

    for node in subG.nodes():
        color = 'red' if node == product_id else 'blue'
        net.add_node(node, label=str(node), color=color)

    for edge in subG.edges():
        net.add_edge(edge[0], edge[1])

    net.save_graph('graph.html')
    with open('graph.html', 'r', encoding='utf-8') as HtmlFile:
        components = HtmlFile.read()
        st.components.v1.html(components, height=650)

def visualize_community_graph(G):
    communities = greedy_modularity_communities(G)
    net = Network(height='600px', width='100%', bgcolor='#222222', font_color='white')

    color_palette = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']

    for idx, community in enumerate(communities):
        color = color_palette[idx % len(color_palette)]
        for node in community:
            net.add_node(node, label=str(node), color=color)

    for edge in G.edges():
        net.add_edge(edge[0], edge[1])

    net.save_graph('graph.html')
    with open('graph.html', 'r', encoding='utf-8') as HtmlFile:
        components = HtmlFile.read()
        st.components.v1.html(components, height=650)

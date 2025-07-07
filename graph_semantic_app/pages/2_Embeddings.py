import streamlit as st
from utils.azure_openai import AzureEmbedding
from utils.graph_db import GraphDB
from utils.embedding_utils import cosine_similarity
from utils.graph_visualizer import visualize_graph

st.title('Embeddings y Grafo Semántico')

azure_embed = AzureEmbedding()
gdb = GraphDB()

text_input = st.text_area('Ingresa texto para generar embeddings (una línea por fragmento):')

if st.button('Generar y almacenar') and text_input:
    fragments = [t.strip() for t in text_input.split('\n') if t.strip()]
    for fragment in fragments:
        emb = azure_embed.get_embedding(fragment)
        gdb.insert_text_with_embedding(fragment, emb)
    st.success('Embeddings generados e insertados en la base de datos.')

query = st.text_input('Consulta o concepto para búsqueda semántica:')

if st.button('Buscar') and query:
    q_emb = azure_embed.get_embedding(query)
    results = gdb.search_similar_embeddings(q_emb)
    st.subheader('Resultados:')
    for res in results:
        st.write(f"Texto: {res['text']} - Distancia: {res['distance']:.4f}")
    subgraph = gdb.get_subgraph(results[0]['id']) if results else None
    if subgraph:
        st.subheader('Subgrafo relacionado:')
        html = visualize_graph(subgraph)
        st.components.v1.html(html, height=500, scrolling=True)

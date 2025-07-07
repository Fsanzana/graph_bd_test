import streamlit as st
from utils.azure_openai import AzureChatGPT

st.title('Chat con Azure GPT')

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

azure_gpt = AzureChatGPT()

user_input = st.text_input('Escribe tu mensaje:')

if st.button('Enviar') and user_input:
    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
    response = azure_gpt.chat(st.session_state.chat_history)
    st.session_state.chat_history.append({'role': 'assistant', 'content': response})

for msg in st.session_state.chat_history:
    st.write(f"**{msg['role']}**: {msg['content']}")

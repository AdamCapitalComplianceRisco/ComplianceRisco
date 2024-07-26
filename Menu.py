import streamlit as st
import Rolagem

st.set_page_config(page_title="Menu Principal", page_icon="🎫", layout="wide")

# Barra lateral para navegação
st.sidebar.title("Menu de Navegação")
page = st.sidebar.selectbox("Escolha uma página", ["Rolagem"])

# Carregar o script correspondente
if page == "Rolagem":
    Rolagem.show()

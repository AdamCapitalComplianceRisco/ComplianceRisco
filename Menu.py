import streamlit as st
import page1
import page2
import page3

st.set_page_config(page_title="App with Sidebar Navigation", page_icon="🎫", layout="wide")

# Barra lateral para navegação
st.sidebar.title("Navegação")
page = st.sidebar.selectbox("Escolha uma página", ["Rolagem", "PNL", "Controle de Margem"])

# Carregar o script correspondente
if page == "Rolagem":
    page1.show()
elif page == "PNL":
    page2.show()
elif page == "Controle de Margem":
    page3.show()

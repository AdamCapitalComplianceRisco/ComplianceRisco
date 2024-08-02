import pandas as pd
import streamlit as st
import requests
import tempfile

# URL do arquivo TXT
url = 'https://link-para-o-arquivo.com/AllTradingDesksVaRStress26Jul2024.txt'

# Baixar o arquivo
response = requests.get(url)
with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
    temp_file.write(response.content)
    temp_file_path = temp_file.name

# Ler o arquivo TXT para DataFrame
try:
    df = pd.read_csv(temp_file_path, delimiter='\t')
    if 'ProductClass' in df.columns:
        df_selected = df[['ProductClass']].copy()
        df_selected["Primeiro Aviso"] = ""
        df_selected["Último Trade"] = ""
        df_selected["Dias Úteis Para Liquidação"] = ""
        df_selected["Entrega Física"] = ""
    else:
        df_selected = pd.DataFrame(columns=['ProductClass', 'Primeiro Aviso', 'Último Trade', 'Dias Úteis Para Liquidação', 'Entrega Física'])
        st.error("Coluna 'ProductClass' não encontrada no arquivo TXT.")
except Exception as e:
    df_selected = pd.DataFrame(columns=['ProductClass', 'Primeiro Aviso', 'Último Trade', 'Dias Úteis Para Liquidação', 'Entrega Física'])
    st.error(f"Ocorreu um erro ao ler o arquivo TXT: {e}")

# Configurar a página do Streamlit
st.set_page_config(page_title="Rolagem", page_icon="🎫")

# Mostrar título e descrição
st.title("Rolagem")
st.write("Aqui será possível verificar as rolagens dos Ativos (Last Date Tradeble)")

# Exibir DataFrame no Streamlit
st.dataframe(df_selected, use_container_width=True, hide_index=True)

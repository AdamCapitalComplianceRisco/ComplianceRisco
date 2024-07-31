import streamlit as st
import pandas as pd

# Definir o DataFrame localmente (substitua isto pelo DataFrame real criado)
df = pd.DataFrame({
    'ProductClass': ['Cash', 'Cash', 'Cash', 'Cash', 'Cash', 'Currencies NDF', 'HUF/USD Futures - ICE', 'USD/CNH Futures - SGX', 'USD/CNH Futures - SGX', 'USD/CNH Futures - SGX'],
    'Primeiro Aviso': ['']*10,
    'Último Trade': ['']*10,
    'Dias Úteis Para Liquidação': ['']*10,
    'Entrega Física': ['']*10
})

# Configurar a página do Streamlit
st.set_page_config(page_title="Rolagem", page_icon="🎫")

# Mostrar título e descrição
st.title("Rolagem")
st.write("Aqui será possível verificar as rolagens dos Ativos (Last Date Tradeble)")

# Exibir o DataFrame no Streamlit
st.dataframe(df, use_container_width=True, hide_index=True)

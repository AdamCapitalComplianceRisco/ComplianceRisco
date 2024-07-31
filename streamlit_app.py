import streamlit as st
import pandas as pd

# Defina o caminho do arquivo TXT
file_path = r'Z:\Riscos\Planilhas\Atuais\Power BI\Bases Carteiras\AllTradingDesksVaRStress26Jul2024.txt'

# Tente ler o arquivo e criar o DataFrame
try:
    # Carregar o arquivo TXT
    df = pd.read_csv(file_path, delimiter='\t')  # Ajuste o delimitador conforme necessário

    # Verifique se a coluna 'ProductClass' está presente e crie o DataFrame com dados reais
    if 'ProductClass' in df.columns:
        # Crie um novo DataFrame com a coluna 'ProductClass' e adicione colunas fictícias
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

# Exibir o DataFrame no Streamlit
st.dataframe(df_selected, use_container_width=True, hide_index=True)

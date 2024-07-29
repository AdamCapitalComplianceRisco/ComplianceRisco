import pandas as pd
import streamlit as st
import os

# Configure the page
st.set_page_config(page_title="Rolagem", page_icon="🎫")

# Apply CSS styles from a file
with open("styles.css") as f:
    css_styles = f.read()
st.markdown(f"<style>{css_styles}</style>", unsafe_allow_html=True)

# Show app title and description.
st.title("Rolagem")
st.write(
    """
    Aqui será possível verificar as rolagens dos Ativos(Last Date Tradeble)
    """
)

# Define the path for the specific TXT file
file_path = r'Z:\Riscos\Planilhas\Atuais\Power BI\Bases Carteiras\AllTradingDesksVaRStress26Jul2024.txt'

# Check if the file exists
if os.path.exists(file_path):
    try:
        # Load the data from the specific TXT file
        txt_data = pd.read_csv(file_path, delimiter='\t')  # Adjust the delimiter as needed

        # Check if 'ProductClass' column exists
        if 'ProductClass' in txt_data.columns:
            # Select the necessary column
            selected_data = txt_data[['ProductClass']].copy()

            # Add new columns with empty values
            selected_data["Primeiro Aviso"] = ""  # Add the appropriate value here
            selected_data["Último Trade"] = ""  # Add the appropriate value here
            selected_data["Dias Úteis Para Liquidação"] = ""  # Add the appropriate value here
            selected_data["Entrega Física"] = ""  # Add the appropriate value here

            # Display the selected data in a table on Streamlit
            st.dataframe(selected_data, use_container_width=True, hide_index=True)
        else:
            st.error("Coluna 'ProductClass' não encontrada no arquivo TXT.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao ler o arquivo TXT: {e}")
else:
    st.error(f"O arquivo não foi encontrado no caminho: {file_path}")

# Continue with the rest of the Streamlit app code...

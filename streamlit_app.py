import os
import glob
import pandas as pd
import streamlit as st

# Define o caminho do diretório dos CSVs
csv_directory = r'Z:\Riscos\Planilhas\Atuais\Power BI\Bases Carteiras'

# Função para obter o arquivo CSV mais recente
def get_latest_csv_file(directory):
    list_of_files = glob.glob(os.path.join(directory, "*.csv"))
    print(f"Arquivos encontrados: {list_of_files}")  # Adicione esta linha para depuração
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

# Obtém o arquivo CSV mais recente
latest_csv_file = get_latest_csv_file(csv_directory)

if latest_csv_file:
    st.write(f"Arquivo CSV mais recente: {latest_csv_file}")
else:
    st.error("Nenhum arquivo CSV encontrado no diretório especificado.")

# Se um arquivo CSV foi encontrado, lê e processa os dados
if latest_csv_file:
    # Lê os dados do arquivo CSV
    try:
        latest_csv_data = pd.read_csv(latest_csv_file)
        st.write("Dados do arquivo CSV mais recente:")
        st.dataframe(latest_csv_data.head())

        # Selecione as colunas necessárias e adicione as novas colunas
        # Assumindo que 'ProductClass' já existe no CSV e outras colunas serão adicionadas posteriormente
        if 'ProductClass' in latest_csv_data.columns:
            # Adicione as novas colunas com valores fictícios ou extraídos de outra fonte
            latest_csv_data['Primeiro Aviso/ Último Trade'] = "Valor Exemplo"  # Substitua pelo valor real
            latest_csv_data['Dias Úteis Para Liquidação'] = 0  # Substitua pelo valor real
            latest_csv_data['Entrega Física'] = "Não"  # Substitua pelo valor real

            # Mostra a tabela com as novas colunas adicionadas
            st.write("Tabela com colunas adicionais:")
            st.dataframe(latest_csv_data, use_container_width=True, hide_index=True)
        else:
            st.error("A coluna 'ProductClass' não foi encontrada no arquivo CSV.")
    except Exception as e:
        st.error(f"Erro ao ler o arquivo CSV: {e}")

import os
import glob
import pandas as pd
import streamlit as st

# Define o caminho do diretório dos arquivos TXT
txt_directory = r'Z:\Riscos\Planilhas\Atuais\Power BI\Bases Carteiras'

# Função para obter o arquivo TXT mais recente
def get_latest_txt_file(directory):
    list_of_files = glob.glob(os.path.join(directory, "*.txt"))
    print(f"Arquivos encontrados: {list_of_files}")  # Adicione esta linha para depuração
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

# Obtém o arquivo TXT mais recente
latest_txt_file = get_latest_txt_file(txt_directory)

if latest_txt_file:
    st.write(f"Arquivo TXT mais recente: {latest_txt_file}")
else:
    st.error("Nenhum arquivo TXT encontrado no diretório especificado.")

# Se um arquivo TXT foi encontrado, lê e processa os dados
if latest_txt_file:
    # Lê os dados do arquivo TXT
    try:
        # Ajuste o separador conforme necessário; exemplo usa '\t' para TSV
        latest_txt_data = pd.read_csv(latest_txt_file, delimiter='\t')  # ou use o delimitador adequado para o seu arquivo
        st.write("Dados do arquivo TXT mais recente:")
        st.dataframe(latest_txt_data.head())

        # Selecione as colunas necessárias e adicione as novas colunas
        # Assumindo que 'ProductClass' já existe no TXT e outras colunas serão adicionadas posteriormente
        if 'ProductClass' in latest_txt_data.columns:
            # Adicione as novas colunas com valores fictícios ou extraídos de outra fonte
            latest_txt_data['Primeiro Aviso/ Último Trade'] = "Valor Exemplo"  # Substitua pelo valor real
            latest_txt_data['Dias Úteis Para Liquidação'] = 0  # Substitua pelo valor real
            latest_txt_data['Entrega Física'] = "Não"  # Substitua pelo valor real

            # Mostra a tabela com as novas colunas adicionadas
            st.write("Tabela com colunas adicionais:")
            st.dataframe(latest_txt_data, use_container_width=True, hide_index=True)
        else:
            st.error("A coluna 'ProductClass' não foi encontrada no arquivo TXT.")
    except Exception as e:
        st.error(f"Erro ao ler o arquivo TXT: {e}")

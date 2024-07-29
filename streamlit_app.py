import datetime
import pandas as pd
import streamlit as st
import os
import glob

# Define o caminho do diretório dos arquivos TXT
txt_directory = r'Z:\Riscos\Planilhas\Atuais\Power BI\Bases Carteiras'

# Função para obter o arquivo TXT mais recente com base na data no nome
def get_latest_txt_file(directory):
    # Padrão de data no nome do arquivo (dia, mês abreviado, ano)
    date_format = "%d%b%Y"
    list_of_files = glob.glob(os.path.join(directory, "*.txt"))

    if not list_of_files:
        st.error("Nenhum arquivo TXT encontrado no diretório especificado.")
        return None

    # Encontra o arquivo com a data mais recente
    latest_file = None
    latest_date = None
    for file in list_of_files:
        file_name = os.path.basename(file)
        # Extrai a parte da data do nome do arquivo
        try:
            date_str = file_name.split("Stress")[-1].replace(".txt", "")
            file_date = datetime.datetime.strptime(date_str, date_format)
            # Atualiza o arquivo mais recente se for o mais recente encontrado
            if latest_date is None or file_date > latest_date:
                latest_date = file_date
                latest_file = file
        except ValueError:
            continue

    if latest_file is None:
        st.error("Nenhum arquivo TXT com data válida encontrada no diretório.")

    return latest_file

# Obtém o arquivo TXT mais recente
latest_txt_file = get_latest_txt_file(txt_directory)

if latest_txt_file:
    # Lê os dados do arquivo TXT mais recente
    try:
        latest_txt_data = pd.read_csv(latest_txt_file, delimiter='\t')  # Ajuste o delimitador conforme necessário
        # Supondo que você deseja filtrar as colunas conforme descrito anteriormente
        selected_columns = ["ProductClass"]
        # Adiciona as novas colunas
        selected_txt_data = latest_txt_data[selected_columns].copy()
        selected_txt_data["Primeiro Aviso"] = ""  # Adicione o valor adequado aqui
        selected_txt_data["Último Trade"] = ""  # Adicione o valor adequado aqui
        selected_txt_data["Dias Úteis Para Liquidação"] = ""  # Adicione o valor adequado aqui
        selected_txt_data["Entrega Física"] = ""  # Adicione o valor adequado aqui

        # Mostra os dados selecionados em uma tabela no Streamlit
        st.dataframe(selected_txt_data, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Ocorreu um erro ao ler o arquivo TXT: {e}")

else:
    st.stop()  # Para a execução do script se não houver arquivos TXT

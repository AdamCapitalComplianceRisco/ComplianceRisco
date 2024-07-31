import pandas as pd
import os

# Define o caminho para o arquivo TXT
file_path = r'Z:/Riscos/Planilhas/Atuais/Power BI/Bases Carteiras/AllTradingDesksVaRStress26Jul2024.txt'

# Função para verificar o arquivo e criar o DataFrame
def create_dataframe_from_txt(file_path):
    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado no caminho: {file_path}")
        return None

    try:
        # Carrega os dados do arquivo TXT
        # Ajuste o delimitador se necessário, aqui estou usando o tab (\t) como exemplo
        txt_data = pd.read_csv(file_path, delimiter='\t')

        # Exibe as primeiras linhas do DataFrame para verificar se a leitura está correta
        print("Primeiras linhas do DataFrame:")
        print(txt_data.head())

        # Verifica se a coluna 'ProductClass' existe
        if 'ProductClass' in txt_data.columns:
            # Cria um DataFrame com a coluna 'ProductClass' e adiciona colunas fictícias
            df = txt_data[['ProductClass']].copy()
            df['Primeiro Aviso'] = ""  # Adicione os valores reais se tiver
            df['Último Trade'] = ""    # Adicione os valores reais se tiver
            df['Dias Úteis Para Liquidação'] = ""  # Adicione os valores reais se tiver
            df['Entrega Física'] = ""  # Adicione os valores reais se tiver

            return df
        else:
            print("Coluna 'ProductClass' não encontrada no arquivo TXT.")
            return None

    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo TXT: {e}")
        return None

# Cria o DataFrame
df = create_dataframe_from_txt(file_path)

# Exibe o DataFrame, se disponível
if df is not None:
    print("DataFrame criado com sucesso:")
    print(df)
else:
    print("Não foi possível criar o DataFrame.")

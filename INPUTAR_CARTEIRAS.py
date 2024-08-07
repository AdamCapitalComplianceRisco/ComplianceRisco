import pandas as pd
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.exc import SQLAlchemyError
import os

# Configurações do banco de dados
DATABASE_URI = 'mssql+pyodbc://sqladminadam:qpE3gEF2JF98e2PBg@adamcapitalsqldb.database.windows.net/AdamDB?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(DATABASE_URI)

# Caminho para a pasta com os arquivos
folder_path = 'Z:/Riscos/Planilhas/Atuais/Power BI/Bases'

def process_files():
    # Carregar metadata
    metadata = MetaData(bind=engine)
    metadata.reflect()

    # Carregar a tabela
    table_name = 'Carteira'
    if table_name not in metadata.tables:
        print(f"Tabela {table_name} não encontrada.")
        return

    table = Table(table_name, metadata, autoload_with=engine)

    # Processar arquivos
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)

            # Ler o arquivo em um DataFrame
            try:
                df = pd.read_csv(file_path, sep='\t')  # Ajuste o separador conforme necessário
            except Exception as e:
                print(f"Erro ao ler o arquivo {filename}: {e}")
                continue

            # Verificar se as colunas necessárias estão presentes
            existing_columns = set(table.columns.keys())
            new_columns = set(df.columns)

            missing_columns = [col for col in new_columns if col not in existing_columns]
            if missing_columns:
                # Adicionar colunas ausentes
                with engine.connect() as conn:
                    for column in missing_columns:
                        try:
                            # Adicionar coluna
                            column_name = column
                            conn.execute(f"ALTER TABLE {table_name} ADD [{column_name}] VARCHAR(255)")
                            print(f"Coluna adicionada: {column_name}")
                        except SQLAlchemyError as e:
                            print(f"Erro ao adicionar a coluna {column_name}: {e}")

            # Inserir dados
            try:
                df['NomeArquivo'] = filename  # Adicionar coluna NomeArquivo com o nome do arquivo
                df.to_sql(table_name, engine, if_exists='append', index=False)
                print(f"Dados do arquivo {filename} inseridos com sucesso.")
            except Exception as e:
                print(f"Erro ao inserir dados do arquivo {filename}: {e}")

if __name__ == '__main__':
    process_files()

import os
import glob
import pandas as pd
import streamlit as st

# Define o caminho do diretório dos arquivos TXT
txt_directory = r'Z:/Riscos/Planilhas/Atuais/Power BI/Bases Carteiras'

# Verifique se o diretório está correto
st.write(f"Diretório sendo verificado: {txt_directory}")

# Função para obter o arquivo TXT mais recente
def get_latest_txt_file(directory):
    # Verifique o conteúdo do diretório
    st.write(f"Listando arquivos no diretório: {directory}")

    list_of_files = glob.glob(os.path.join(directory, "*.txt"))

    # Verifique se a lista de arquivos está vazia
    if not list_of_files:
        st.error("Nenhum arquivo TXT encontrado no diretório especificado.")
        st.write("Arquivos encontrados no diretório:", list_of_files)  # Lista vazia
        return None

    # Encontre o arquivo mais recente
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

# Obtém o arquivo TXT mais recente
latest_txt_file = get_latest_txt_file(txt_directory)

if latest_txt_file:
    try:
        # Ajuste o separador conforme necessário; exemplo usa '\t' para TSV
        latest_txt_data = pd.read_csv(latest_txt_file, delimiter='\t')  # ou use o delimitador adequado para o seu arquivo

        # Seleciona as colunas necessárias do TXT
        selected_columns = ["ProductClass"]
        selected_txt_data = latest_txt_data[selected_columns]

        # Adiciona as novas colunas com valores fictícios ou placeholders
        selected_txt_data["Primeiro Aviso"] = "Placeholder"  # Substitua com dados reais
        selected_txt_data["Último Trade"] = "Placeholder"  # Substitua com dados reais
        selected_txt_data["Dias Úteis Para Liquidação"] = "Placeholder"  # Substitua com dados reais
        selected_txt_data["Entrega Física"] = "Placeholder"  # Substitua com dados reais

        # Mostra os dados selecionados em uma tabela no Streamlit
        st.dataframe(selected_txt_data, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Erro ao ler o arquivo TXT: {e}")

else:
    st.stop()  # Para a execução do script se não houver arquivos TXT

# Restante do código da aplicação Streamlit
st.set_page_config(page_title="Rolagem", page_icon="🎫")
st.title("Rolagem")
st.write(
    """
    Aqui será possível verificar as rolagens dos Ativos (Last Date Tradeable)
    """
)

# Show a section to add a new ticket.
st.header("Add a ticket")

with st.form("add_ticket_form"):
    issue = st.text_area("Describe the issue")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("Submit")

if submitted:
    recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{recent_ticket_number+1}",
                "Issue": issue,
                "Status": "Open",
                "Priority": priority,
                "Date Submitted": today,
            }
        ]
    )
    st.write("Ticket submitted! Here are the ticket details:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

# Show section to view and edit existing tickets in a table.
st.header("Existing tickets")
st.write(f"Number of tickets: {len(st.session_state.df)}")

st.info(
    "You can edit the tickets by double clicking on a cell. Note how the plots below "
    "update automatically! You can also sort the table by clicking on the column headers.",
    icon="✍️",
)

# Show the tickets dataframe with st.data_editor.
edited_df = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            help="Ticket status",
            options=["Open", "In Progress", "Closed"],
            required=True,
        ),
        "Priority": st.column_config.SelectboxColumn(
            "Priority",
            help="Priority",
            options=["High", "Medium", "Low"],
            required=True,
        ),
    },
    # Disable editing the ID and Date Submitted columns.
    disabled=["ID", "Date Submitted"],
)

# Show some metrics and charts about the ticket.
st.header("Statistics")

# Show metrics side by side using st.columns and st.metric.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# Show two Altair charts using st.altair_chart.
st.write("")
st.write("##### Ticket status per month")
status_plot = (
    alt.Chart(edited_df)
    .mark_bar()
    .encode(
        x="month(Date Submitted):O",
        y="count():Q",
        xOffset="Status:N",
        color="Status:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

st.write("##### Current ticket priorities")
priority_plot = (
    alt.Chart(edited_df)
    .mark_arc()
    .encode(theta="count():Q", color="Priority:N")
    .properties(height=300)
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")

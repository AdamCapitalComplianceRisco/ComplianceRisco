import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

def local_css(file_name):
    with open(file_name) as f:

local_css("styles.css")

# Configuração do aplicativo Streamlit
st.set_page_config(page_title="Rolagem", page_icon="🎫", layout="wide")

# Título e Faixa
st.title("Rolagem")
st.markdown(
    """
    <div style='border-bottom: 5px solid rgb(49, 74, 96); margin-bottom: 10px;'></div>
    """,
    unsafe_allow_html=True,
)

st.write(
    """
    Aqui será possível verificar as rolagens dos Ativos (Last Date Tradeble).
    """
)

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:
    # Set seed for reproducibility.
    np.random.seed(42)

    # Make up some fake issue descriptions.
    issue_descriptions = [
        "Network connectivity issues in the office",
        "Software application crashing on startup",
        "Printer not responding to print commands",
        "Email server downtime",
        "Data backup failure",
        "Login authentication problems",
        "Website performance degradation",
        "Security vulnerability identified",
        "Hardware malfunction in the server room",
        "Employee unable to access shared files",
        "Database connection failure",
        "Mobile application not syncing data",
        "VoIP phone system issues",
        "VPN connection problems for remote employees",
        "System updates causing compatibility issues",
        "File server running out of storage space",
        "Intrusion detection system alerts",
        "Inventory management system errors",
        "Customer data not loading in CRM",
        "Collaboration tool not sending notifications",
    ]

    # Generate the dataframe with 100 rows/tickets.
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Issue": np.random.choice(issue_descriptions, size=100),
        "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100),
        "Priority": np.random.choice(["High", "Medium", "Low"], size=100),
        "Date Submitted": [
            datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df

# Show a section to add a new ticket.
st.header("Adicionar um ticket")

# We're adding tickets via an `st.form` and some input widgets. If widgets are used
# in a form, the app will only rerun once the submit button is pressed.
with st.form("add_ticket_form"):
    issue = st.text_area("Descreva o problema")
    priority = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
    submitted = st.form_submit_button("Enviar")

if submitted:
    # Make a dataframe for the new ticket and append it to the dataframe in session
    # state.
    recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{recent_ticket_number+1}",
                "Issue": issue,
                "Status": "Aberto",
                "Priority": priority,
                "Date Submitted": today,
            }
        ]
    )

    # Show a little success message.
    st.write("Ticket enviado! Aqui estão os detalhes do ticket:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

# Show section to view and edit existing tickets in a table.
st.header("Tickets existentes")
st.write(f"Número de tickets: `{len(st.session_state.df)}`")

st.info(
    "Você pode editar os tickets clicando duas vezes em uma célula. Note como os gráficos abaixo "
    "atualizam automaticamente! Você também pode ordenar a tabela clicando nos cabeçalhos das colunas.",
    icon="✍️",
)

# Use colunas para a caixa de seleção e a tabela
col1, col2 = st.columns([1, 3])

with col1:
    st.checkbox("Mostrar tickets fechados")

with col2:
    # Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
    # cells. The edited data is returned as a new dataframe.
    edited_df = st.data_editor(
        st.session_state.df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                help="Status do ticket",
                options=["Aberto", "Em Progresso", "Fechado"],
                required=True,
            ),
            "Priority": st.column_config.SelectboxColumn(
                "Prioridade",
                help="Prioridade",
                options=["Alta", "Média", "Baixa"],
                required=True,
            ),
        },
        # Disable editing the ID and Date Submitted columns.
        disabled=["ID", "Date Submitted"],
    )

# Show some metrics and charts about the ticket.
st.header("Estatísticas")

# Show metrics side by side using `st.columns` and `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Aberto"])
col1.metric(label="Número de tickets abertos", value=num_open_tickets, delta=10)
col2.metric(label="Tempo de primeira resposta (horas)", value=5.2, delta=-1.5)
col3.metric(label="Tempo médio de resolução (horas)", value=16, delta=2)

# Show two Altair charts using `st.altair_chart`.
st.write("")
st.write("##### Status dos tickets por mês")
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

st.write("##### Prioridades dos tickets atuais")
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

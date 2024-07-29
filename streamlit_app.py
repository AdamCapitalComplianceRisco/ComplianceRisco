import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Configurar a página do Streamlit
st.set_page_config(page_title="Rolagem", page_icon="🎫", layout="wide")

# Título e descrição do aplicativo
st.title("Rolagem")
st.write(
    """
    Aqui será possível verificar as rolagens dos Ativos(Last Date Tradeble)
    """
)

# Faixa azul abaixo do título
st.markdown("<div style='height: 10px; background-color: #314a60;'></div>", unsafe_allow_html=True)

# Criar um dataframe aleatório com tickets existentes
if "df" not in st.session_state:
    # Configurar a semente para reprodutibilidade
    np.random.seed(42)

    # Criar algumas descrições de problemas
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

    # Gerar o dataframe com 100 linhas/tickets
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

    # Salvar o dataframe no estado da sessão
    st.session_state.df = df

# Seção para adicionar um novo ticket
st.header("Add a ticket")

# Adicionar tickets via formulário
with st.form("add_ticket_form"):
    issue = st.text_area("Describe the issue")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("Submit")

if submitted:
    # Criar um dataframe para o novo ticket e adicionar ao dataframe no estado da sessão
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

    # Mostrar mensagem de sucesso
    st.write("Ticket submitted! Here are the ticket details:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

# Seção para visualizar e editar tickets existentes
st.header("Existing tickets")
st.write(f"Number of tickets: `{len(st.session_state.df)}`")

st.info(
    "You can edit the tickets by double clicking on a cell. Note how the plots below "
    "update automatically! You can also sort the table by clicking on the column headers.",
    icon="✍️",
)

# Layout para tabela de tickets e caixa de seleção lado a lado
col1, col2 = st.columns([3, 1])

with col1:
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
        # Desativar edição das colunas ID e Date Submitted
        disabled=["ID", "Date Submitted"],
    )

with col2:
    st.write("## Filter options")
    priority_filter = st.selectbox("Filter by priority", ["All", "High", "Medium", "Low"])
    if priority_filter != "All":
        edited_df = edited_df[edited_df["Priority"] == priority_filter]

# Mostrar algumas métricas e gráficos sobre os tickets
st.header("Statistics")

# Mostrar métricas lado a lado usando st.columns e st.metric
col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# Mostrar dois gráficos Altair usando st.altair_chart
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

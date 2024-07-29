import datetime
import random
import numpy as np
import pandas as pd
import streamlit as st
import os
import glob

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

# Directory where CSV files are stored
csv_directory = "Z:/Riscos/Planilhas/Atuais/Power BI/Bases Carteiras"

# Function to get the latest CSV file
def get_latest_csv_file(directory):
    list_of_files = glob.glob(os.path.join(directory, "*.csv"))
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

# Get the latest CSV file
latest_csv_file = get_latest_csv_file(csv_directory)
latest_csv_data = pd.read_csv(latest_csv_file)

# Select the required columns from the CSV file
csv_columns = ["ProductClass"]
csv_data = latest_csv_data[csv_columns]

# Add additional columns with data from another source
csv_data["Primeiro Aviso"] = "Dados de outra fonte"
csv_data["Último Trade"] = "Dados de outra fonte"
csv_data["Dias Úteis Para Liquidação"] = "Dados de outra fonte"
csv_data["Entrega Física"] = "Dados de outra fonte"

# Create the main dataframe for the application
if "df" not in st.session_state:
    # Set seed for reproducibility.
    np.random.seed(42)

    # Generate the dataframe with 100 rows/tickets.
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Issue": np.random.choice(["Network connectivity issues", "Software application crashing", "Printer not responding"], size=100),
        "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100),
        "Priority": np.random.choice(["High", "Medium", "Low"], size=100),
        "Date Submitted": [
            datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)

    # Merge with CSV data
    df = pd.concat([df, csv_data], axis=1)

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df

# Show a section to add a new ticket.
st.header("Add a ticket")

# We're adding tickets via an st.form and some input widgets. If widgets are used
# in a form, the app will only rerun once the submit button is pressed.
with st.form("add_ticket_form"):
    issue = st.text_area("Describe the issue")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("Submit")

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
                "Status": "Open",
                "Priority": priority,
                "Date Submitted": today,
                "ProductClass": "",
                "Primeiro Aviso": "",
                "Último Trade": "",
                "Dias Úteis Para Liquidação": "",
                "Entrega Física": ""
            }
        ]
    )

    # Show a little success message.
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

# Show the tickets dataframe with st.data_editor. This lets the user edit the table
# cells. The edited data is returned as a new dataframe.
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

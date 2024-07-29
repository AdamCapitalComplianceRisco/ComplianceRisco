import datetime
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

# Define the directory path for the TXT files
txt_directory = r'Z:/RiscosPlanilhas/Atuais/Power BI/Bases Carteiras/AllTradingDesksVaRStress26Jul2024.txt'

# Function to get the latest TXT file based on the name
def get_latest_txt_file(directory):
    # List all TXT files in the directory
    list_of_files = glob.glob(os.path.join(directory, "*.txt"))

    if not list_of_files:
        st.error("Nenhum arquivo TXT encontrado no diretório especificado.")
        return None

    # Find the most recent file based on the date in the filename
    latest_file = None
    latest_date = None
    for file in list_of_files:
        file_name = os.path.basename(file)
        # Extract date from the filename
        try:
            date_str = file_name.split("Stress")[-1].replace(".txt", "")
            file_date = datetime.datetime.strptime(date_str, "%d%b%Y")
            # Update the latest file if the current file is newer
            if latest_date is None or file_date > latest_date:
                latest_date = file_date
                latest_file = file
        except ValueError:
            continue

    if latest_file is None:
        st.error("Nenhum arquivo TXT com data válida encontrado no diretório.")

    return latest_file

# Get the latest TXT file
latest_txt_file = get_latest_txt_file(txt_directory)

if latest_txt_file:
    # Read data from the latest TXT file
    try:
        latest_txt_data = pd.read_csv(latest_txt_file, delimiter='\t')  # Adjust the delimiter as needed

        # Select the necessary column
        selected_columns = ["ProductClass"]
        if all(col in latest_txt_data.columns for col in selected_columns):
            selected_txt_data = latest_txt_data[selected_columns].copy()

            # Add new columns with empty values
            selected_txt_data["Primeiro Aviso"] = ""  # Add the appropriate value here
            selected_txt_data["Último Trade"] = ""  # Add the appropriate value here
            selected_txt_data["Dias Úteis Para Liquidação"] = ""  # Add the appropriate value here
            selected_txt_data["Entrega Física"] = ""  # Add the appropriate value here

            # Display the selected data in a table on Streamlit
            st.dataframe(selected_txt_data, use_container_width=True, hide_index=True)

        else:
            st.error("Coluna 'ProductClass' não encontrada no arquivo TXT.")

    except Exception as e:
        st.error(f"Ocorreu um erro ao ler o arquivo TXT: {e}")

else:
    st.stop()  # Stop execution if no TXT files are found

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:
    np.random.seed(42)
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
    st.session_state.df = df

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
    disabled=["ID", "Date Submitted"],
)

# Show some metrics and charts about the ticket.
st.header("Statistics")

col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

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

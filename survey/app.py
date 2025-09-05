import os
import datetime
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from questions import questions  # file containing survey questions

###########################
### GOOGLE SHEETS SETUP ###
###########################
 
SHEET_ID = "1vfSVFCsJtIete13ERh1DkuLM3nBAPhJkw5YzXULBQOM"   
SHEET_NAME = "Responses"

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_gspread_client():
    """Authorize Google Sheets via st.secrets (cloud) or credentials.json (local)."""
    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scope
        )
        return gspread.authorize(creds)
    except Exception:
        if os.path.exists("credentials.json"):
            creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
            return gspread.authorize(creds)
        else:
            st.error("❌ No credentials found (neither st.secrets nor credentials.json).")
            st.stop()

client = get_gspread_client()

# Open or create worksheet
try:
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
except gspread.WorksheetNotFound:
    sh = client.open_by_key(SHEET_ID)
    sheet = sh.add_worksheet(title=SHEET_NAME, rows="100", cols="20")

########################
# ENSURE HEADERS EXIST #
########################

expected_headers = ["Event_Name", "Timestamp"]
for q in questions:
    expected_headers.append(f"{q['id']}_likert")
    expected_headers.append(f"{q['id']}_text")

existing_headers = sheet.row_values(1)
if existing_headers != expected_headers:
    if existing_headers:
        sheet.delete_rows(1)
    sheet.insert_row(expected_headers, 1)

########################
# DETERMINE EVENT NAME #
########################
DEFAULT_EVENT = "NeuroGame_workshop"
query_params = st.query_params
EVENT_NAME = query_params.get("event", [DEFAULT_EVENT])[0]

# APP MODES

mode = st.sidebar.radio("Choose Mode", ["About", "Survey"])

# SURVEY MODE

if mode == "Survey":
    if "page" not in st.session_state:
        st.session_state.page = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    st.title("Survey on perspectives on Neurotechnologies in a clinical context")

    q = questions[st.session_state.page]

    st.subheader(f"Question {st.session_state.page+1} of {len(questions)}")
    likert = st.radio(
        q["question"],
        q["scale_labels"],
        index=(st.session_state.answers.get(q["id"]+"_likert", None) or 1)-1,
        key=f"likert_{q['id']}"
    )

    text = st.text_area(
        "Optional feedback (share any thoughts that influenced your choice):",
        value=st.session_state.answers.get(q["id"]+"_text", ""),
        key=f"text_{q['id']}"
    )

    st.session_state.answers[q["id"]+"_likert"] = q["scale_labels"].index(likert)+1
    st.session_state.answers[q["id"]+"_text"] = text

    col1, col2 = st.columns([1,1])

    with col1:
        if st.session_state.page > 0:
            if st.button("⬅ Back"):
                st.session_state.page -= 1
                st.rerun()

    with col2:
        if st.session_state.page < len(questions)-1:
            if st.button("Next ➡"):
                st.session_state.page += 1
                st.rerun()
        else:
            if st.button("✅ Submit Survey"):

                row = [EVENT_NAME, datetime.datetime.now().isoformat()]
                for q in questions:
                    row.append(st.session_state.answers[q["id"]+"_likert"])
                    row.append(st.session_state.answers[q["id"]+"_text"])
                sheet.append_row(row)

                st.success("✅ Thank you! Your responses have been recorded.")
                st.session_state.page = 0
                st.session_state.answers = {}


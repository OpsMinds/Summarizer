import streamlit as st
from summarizer import get_summary, fetch_servicenow_data_by_incident_number

st.title("ServiceNow Incident Summarizer using ChatGPT")

# Create a form for input
with st.form("incident_form"):
    incident_number = st.text_input("Enter Incident Number:")
    submitted = st.form_submit_button("Summarize")

if submitted:
    if incident_number:
        try:
            data = fetch_servicenow_data_by_incident_number(incident_number)
            if data:
                text_to_summarize = data.get('short_description', '') + "\n\n" + data.get('description', '')
                st.subheader("Original Text:")
                st.write(text_to_summarize)
                summary = get_summary(text_to_summarize)
                st.subheader("Summary:")
                st.write(summary)
            else:
                st.error(f"No data found for incident number {incident_number}.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")
    else:
        st.error("Please enter an incident number.")

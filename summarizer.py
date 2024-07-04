import openai
import requests
from requests.auth import HTTPBasicAuth
import streamlit as st

# Fetching secrets from Streamlit's secrets management
openai.api_key = st.secrets["openai"]["api_key"]
instance_url = st.secrets["servicenow"]["instance_url"]
username = st.secrets["servicenow"]["username"]
password = st.secrets["servicenow"]["password"]

def get_summary(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": text}
        ]
    )
    summary = response.choices[0].message['content']
    return summary

def fetch_servicenow_data_by_incident_number(incident_number):
    url = f"{instance_url}/api/now/table/incident"
    headers = {
        "Accept": "application/json"
    }
    query = {
        "sysparm_query": f"number={incident_number}"
    }
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, password), params=query)
    if response.status_code == 200:
        result = response.json()['result']
        return result[0] if result else None
    else:
        response.raise_for_status()
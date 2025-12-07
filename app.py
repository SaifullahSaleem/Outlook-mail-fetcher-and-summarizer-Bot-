import streamlit as st
from email_fetcher import fetch_emails_for_day
from langchain_email_qa import create_langchain_pipeline
import openai
import os

# Set OpenAI Key
os.environ["OPENAI_API_KEY"] = "your API key"

st.title("📨 Outlook Email Query App")
st.write("Fetch your Outlook emails for a specific date and ask questions about them!")

selected_date = st.date_input("Select a date:")
if st.button("Fetch Emails"):
    with st.spinner("Fetching emails..."):
        emails = fetch_emails_for_day(selected_date.strftime("%Y-%m-%d"))
        if not emails:
            st.warning("No emails found for the selected date.")
        else:
            st.success(f"Fetched {len(emails)} emails.")
            st.session_state["qa_chain"] = create_langchain_pipeline(emails)

if "qa_chain" in st.session_state:
    user_query = st.text_input("Ask a question about your emails:")
    if st.button("Get Answer"):
        if user_query.strip():
            with st.spinner("Analyzing emails..."):
                answer = st.session_state["qa_chain"].run(user_query)
                st.write("**Answer:** ", answer)

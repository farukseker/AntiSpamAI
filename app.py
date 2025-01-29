from ai_service import LocalLLM
import streamlit as st
from email_service import EmailFetcher
from config import TEST_USERNAME, TEST_PASSWORD
from dataclasses import dataclass


# @dataclass(frozen=True)
# class EmailResult:
#     is_spam: bool | None = None
#     sentiment: str | None = None
#     themes: list[str] | None = None
#     is_important: bool | None = None
#     has_error: bool = False
#
#     ...

st.set_page_config(layout="wide")

local_llm: LocalLLM = LocalLLM()
local_llm_list = local_llm.list_llm()

llm_side: str = 'local'
last_model: str = 'llama3.2:1b'

st.title("Email Spam Classifier")

selected_model = st.selectbox("Choose a model", local_llm_list,
                              index=local_llm_list.index(last_model) if last_model in local_llm_list else 0)


st.subheader("SMTP Login")
email_user = st.text_input("Email Address", value=TEST_USERNAME)
email_pass = st.text_input("Email Password", value=TEST_PASSWORD, type="password")

row = st.number_input(label='Set a mail limit or 0 unlimited', value=10)

email_fetcher: EmailFetcher = EmailFetcher(email_user, email_pass)

if st.button("Fetch and Analyze Emails"):
    email_fetcher.connect()

    st.info("Analyzing emails...")
    table_placeholder = st.empty()
    results = []
    local_llm.selected_model = selected_model

    for mail in email_fetcher.fetch_emails(row):
        if analyze := local_llm.analyze_mail(email=mail.body):
            results.append({
                "is_spam": analyze.is_spam,
                "is_important": analyze.is_important,
                "sentiment": analyze.sentiment,
                "themes": analyze.themes,
                "id": mail.id,
                "subject": mail.subject,
                "is_starred": mail.is_starred,
                "labels": mail.labels,
                "flags": mail.flags,
                "_from": mail._from,
            })

            # id
            # subject
            # _from
            # flags
            # labels
            # is_starred

            # is_spam
            # sentiment
            # themes
            # is_important
            # OR
            # error

        table_placeholder.table(results)

    st.subheader("Analysis Results")
    st.table(results)

    email_fetcher.disconnect()

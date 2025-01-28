from ai_service import LocalLLM
import streamlit as st
from email_service import EmailFetcher
from config import TEST_USERNAME, TEST_PASSWORD


local_llm: LocalLLM = LocalLLM()
local_llm_list = local_llm.list_llm()

llm_side: str = 'local'
last_model: str = 'llama3.2:1b'

st.title("Email Spam Classifier")

selected_model = st.selectbox("Choose a model", local_llm_list,
                              index=local_llm_list.index(last_model) if last_model in local_llm_list else 0)


# email_fetcher: EmailFetcher = EmailFetcher(TEST_USERNAME, TEST_PASSWORD)
#
# try:
#     email_fetcher.connect()
#
#     llm = LocalLLM()
#     if llms := llm.list_llm():
#         print(llms)
#
#     llm.selected_model = llms[1]
#     print('mail')
#
#     for mail in email_fetcher.fetch_emails(10):
#         print(mail.subject)
#         llm.analyze_mail(email=mail.body)
# except Exception as e:
#     print(f'ERROR: {str(e)}')
# finally:
#     email_fetcher.disconnect()

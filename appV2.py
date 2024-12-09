import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

genai.configure(api_key="AIzaSyAK0fUMW6n5Fw0Lq4xT_spYsELwnt503pc")
model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
)

st.set_page_config(layout="wide")
st.title("Assignment Chatbot")

with st.sidebar:
    st.title("Sidebar")
    uploadedFiles = st.file_uploader("PDF File Uploader", type="pdf", accept_multiple_files=False)

# Initialize messages if there is none 
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "Hello, what can i do for you?"}
    ]

# Display all of the messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# When user upload pdf files
if uploadedFiles is not None:

    pdf_reader = PdfReader(uploadedFiles)
    text_content = ""

    for page in pdf_reader.pages:
        if page.extract_text() is not None:
            text_content += page.extract_text() + "\n"

    st.session_state.pdf_text = text_content

    with st.chat_message("human"):
        st.markdown("PDF Upload")

    response = chat.send_message("PDF Upload:\n" + text_content)
    response = response.text

    with st.chat_message("ai"):
        st.markdown(response)

    st.session_state.messages.append({"role": "human", "content": "PDF Upload"})
    st.session_state.messages.append({"role": "ai", "content": response})


# When user enter input
if userInput:= st.chat_input("Message Chatbot"):
    
    with st.chat_message("human"):
        st.markdown(userInput)

    response = chat.send_message(userInput)
    response = response.text

    with st.chat_message("ai"):
        st.markdown(response)

    st.session_state.messages.append({"role": "human", "content": userInput})
    st.session_state.messages.append({"role": "ai", "content": response})







    


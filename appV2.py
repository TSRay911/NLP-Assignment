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

    #PDF File Uploader
    with st.form("PDF Form", clear_on_submit=True, border=False):
        uploadedFiles = st.file_uploader(label="PDF File Uploader", type="pdf", accept_multiple_files=False)
        

        button_html = """
        <style>
            .stFormSubmitButton > button{
                width: 100%;
            }

            .stFileUploader > section > button{
                width: 100%;
            }

            .stFileUploader > label > div > p{
                font-size: 1.2em;
            }
            
        </style>
        """
        st.markdown(button_html, unsafe_allow_html=True)
        submitted = st.form_submit_button("Submit")

    # When user press submit and have uploaded files
    if submitted and uploadedFiles:
        pdf_reader = PdfReader(uploadedFiles)
        textContent = ""

        for page in pdf_reader.pages:
            if page.extract_text() is not None:
                textContent += page.extract_text() + "\n"

        response = chat.send_message("PDF Upload:\n" + textContent)
        response = response.text

        st.session_state.messages.append({"role": "human", "content": "PDF Upload"})
        st.session_state.messages.append({"role": "ai", "content": response})

    #Model Picker


# Initialize messages if there is none 
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "Hello, what can i do for you?"}
    ]

# Display all of the messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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







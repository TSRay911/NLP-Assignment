import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

genai.configure(api_key="AIzaSyAK0fUMW6n5Fw0Lq4xT_spYsELwnt503pc")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

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

    #File Uploader
    with st.form("Form", clear_on_submit=True, border=False):
        uploadedFiles = st.file_uploader(label="File Uploader", type=["pdf", "mp3", 'wav'], accept_multiple_files=False)
        

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

            .stSelectbox > label > div > p{
                font-size: 1.5em;
                font-weight: bold;
            }
            
        </style>
        """
        st.markdown(button_html, unsafe_allow_html=True)
        submitted = st.form_submit_button("Submit")

    # When user press submit and have uploaded files
    if submitted:
        if not uploadedFiles:
            st.error("No file uploaded.")
        elif uploadedFiles.name.lower().endswith(".pdf"):
            pdf_reader = PdfReader(uploadedFiles)
            textContent = ""

            for page in pdf_reader.pages:
                if page.extract_text() is not None:
                    textContent += page.extract_text() + "\n"

            response = chat.send_message("PDF Upload:\n" + textContent)
            response = response.text

            st.session_state.messages.append({"role": "human", "content": "PDF Upload"})
            st.session_state.messages.append({"role": "ai", "content": response})

        elif uploadedFiles.name.lower().endswith((".mp3", "wav")):

            if uploadedFiles.name.lower().endswith(".mp3"):
                mimeType = "audio/mpeg"
            else:
                mimeType = "audio/wav"

            audioFile = genai.upload_file(uploadedFiles, mime_type=mimeType)
            response = model.generate_content([audioFile, "Describe this audio clip"])
            response = response.text

            st.session_state.messages.append({"role": "human", "content": "Audio Upload"})
            st.session_state.messages.append({"role": "ai", "content": response})
        

    #Model Picker
    option = st.selectbox(
        "Model",
        ("Gemini 1.5 Flash", "Gemini 1.5 Flash-8B", "Gemini 1.5 Pro"),
        index=0
    )
    
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







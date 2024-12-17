import streamlit as st
from PyPDF2 import PdfReader
import shelve
import google.generativeai as genai


genai.configure(api_key="AIzaSyApjjQc7BUbTbTog3W0pJlkzfdAJvvdlao")

st.set_page_config(layout="wide")
st.title("NLP Chatbot")

htmlStyle = """
    <style>
        .stFormSubmitButton > button{
            width: 100%;
        }

        .stFileUploader > section > button{
            width: 100%;
        }

        .stFileUploader > label > div > p{
            font-size: 1.2em;
            font-weight: bold;
        }

        .stSelectbox > label > div > p{
            font-size: 1.5em;
            font-weight: bold;
        }
            
        .stAudioInput > label > div > P{
            font-size: 1.5em;
            font-weight: bold;
        }

        .stButton > button{
            width: 100%;
        }

    </style>
    
    """
st.markdown(htmlStyle, unsafe_allow_html=True)

def loadChatHistory():
    with shelve.open("chatHistory") as db:
        return db.get("messages", [
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Gemini 1.5 Flash : Great to meet you. What would you like to know?"}
        ])

def saveChatHistory(messages):
    with shelve.open("chatHistory") as db:
        db["messages"] = messages

if "messages" not in st.session_state:
    st.session_state.messages = loadChatHistory()

if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel("gemini-1.5-flash")

if "modelName" not in st.session_state:    
    st.session_state.modelName = "Gemini-1.5 Flash"

if "chatHistory" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-flash")
    st.session_state.chatHistory = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Gemini 1.5 Flash : Great to meet you. What would you like to know?"},
        ]
    )

with st.sidebar:

    options = ["Gemini 1.5 Flash", "Gemini 1.5 Pro", "Gemini 2.0 Flash EXP"]
    selectedOption = st.selectbox("Model", options)

    if selectedOption != st.session_state.model:
        st.session_state.model = selectedOption
        if selectedOption == "Gemini 1.5 Flash":
            model = genai.GenerativeModel("gemini-1.5-flash")
            st.session_state.modelName = "Gemini-1.5 Flash"
        elif selectedOption == "Gemini 1.5 Pro":
            model = genai.GenerativeModel("gemini-1.5-pro")
            st.session_state.modelName = "Gemini 1.5 Pro"
        else:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            st.session_state.modelName = "Gemini 2.0 Flash Exp"

        st.session_state.chat = model.start_chat(history=st.session_state.messages)

    with st.form("Form1", border=False, clear_on_submit=True):
        uploadedFile = st.file_uploader("File Uploader", type=[".pdf", '.mp3', '.wav'], accept_multiple_files=False)
        submitted1 = st.form_submit_button("Submit")

    if submitted1:
        if not uploadedFile:
            st.error("No file uploaded.")
        elif uploadedFile.name.lower().endswith(".pdf"):
            pdf_reader = PdfReader(uploadedFile)
            textContent = ""

            for page in pdf_reader.pages:
                if page.extract_text() is not None:
                    textContent += page.extract_text() + "\n"

            chat = st.session_state.chat
            response = chat.send_message("PDF Upload: Please Summarized \n" + textContent)
            response = (st.session_state.modelName) + " : " + response.text

            st.session_state.messages.append({"role": "user", "parts": "PDF Upload"})
            st.session_state.messages.append({"role": "model", "parts": response})

        else:
            if uploadedFile.name.lower().endswith(".mp3"):
                mimeType = "audio/mpeg"
            else:
                mimeType = "audio/wav"
            
            chat = st.session_state.chat
            audioFile = genai.upload_file(uploadedFile, mime_type=mimeType)
            response = chat.send_message([audioFile, "Describe this audio clip"])
            response = (st.session_state.modelName) + " : " + response.text

            st.session_state.messages.append({"role": "user", "parts": "Audio Upload"})
            st.session_state.messages.append({"role": "model", "parts": response})

    with st.form("Form2", clear_on_submit=True):

        audioInput = st.audio_input("Audio Input")
        submitted2 = st.form_submit_button("Submit")
        
        if submitted2:

            if not audioInput:
                st.error("No audio.")
            else:
                with st.spinner("Processing audio..."):
                    chat = st.session_state.chat
                    audio = genai.upload_file(audioInput, mime_type="audio/wav")
                    response = chat.send_message([audio, "Describe this audio clip"])
                    response = (st.session_state.modelName) + " : " + response.text

                    st.session_state.messages.append({"role": "user", "parts": "Audio Upload"})
                    st.session_state.messages.append({"role": "model", "parts": response})

    if st.button("Delete Chat History"):
        st.session_state.messages = [
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Gemini 1.5 Flash : Great to meet you. What would you like to know?"}
        ]
        saveChatHistory(st.session_state.messages)
        st.success("Chat history deleted!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"])

if userInput:=st.chat_input("Message Chatbot"): 
    with st.chat_message("user"):
        st.markdown(userInput)

    chat = st.session_state.chat
    response = chat.send_message(userInput)
    response = (st.session_state.modelName) + " : " + response.text    

    with st.chat_message("model"):
        st.markdown(response)   

    st.session_state.messages.append({"role": "user", "parts": userInput})
    st.session_state.messages.append({"role": "model", "parts": response})

saveChatHistory(st.session_state.messages)
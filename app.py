import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyAK0fUMW6n5Fw0Lq4xT_spYsELwnt503pc")
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("Assignment Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Message Chatbot", key="chat_input_1"):

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = response = model.generate_content(prompt)
    response = response.text

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(f"Chatbot: {response}")

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})




import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Sky", layout="centered")

# Doğrudan Google AI Studio API anahtarın
genai.configure(api_key="AQ.Ab8RN6L1_GkO9w1Z6L-PzHMuMnDSr_FKcay0fn-g8SWjEgHklg")

# Model ayarı
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-flash")
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Sky")

# Geçmiş mesajları ekrana basma
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi alma
if prompt := st.chat_input("Sky'a sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Hata oluştu: {e}")

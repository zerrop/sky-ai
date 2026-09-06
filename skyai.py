import os
import time
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai.errors import APIError

# Sayfa Yapılandırması
st.set_page_config(page_title="Sky", layout="centered")

# --- DİNAMİK TARİH VE ZAMAN ---
simdi = datetime.now()
gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
bugun_adi = gunler[simdi.weekday()]
bugun_tarih = simdi.strftime(f"%d.%m.%Y ({bugun_adi}) Saat: %H:%M")

# --- SİSTEM TALİMATI ---
system_instruction = f"""
Senin adın Sky. Sen son derece zeki, nazik, samimi, eğlenceli ve yardımsever bir yapay zeka asistanısın.
Bugünün tarihi ve saati: {bugun_tarih}.

Kuralların:
1. Kullanıcıya karşı her zaman doğal, arkadaş canlısı ve akıcı bir dil kullan.
2. Gereksiz resmiyetten uzak dur, konuşma diline yakın ama saygılı ol.
3. Sorulara net, açıklayıcı ve yapıcı yanıtlar ver.
4. Kod veya teknik konularda anlaşılır ve adım adım rehberlik et.
"""

# --- CSS STİLLERİ ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0d0f18 !important;
        color: #FFFFFF !important;
    }
    
    header {visibility: hidden;}

    .main .block-container {
        padding-bottom: 220px !important;
        max-width: 800px !important;
    }

    div[data-testid="stBottom"] {
        position: fixed !important;
        bottom: 0px !important;
        left: 0 !important;
        right: 0 !important;
        background: transparent !important;
        padding-bottom: 25px !important;
        padding-top: 10px !important;
        z-index: 999999 !important;
    }

    div[data-testid="stChatInput"] {
        max-width: 680px !important;
        margin: 0 auto !important;
        background: rgba(18, 21, 33, 0.95) !important;
        border-radius: 35px !important;
        border: 1px solid rgba(0, 132, 255, 0.3) !important;
        box-shadow: 0 0 20px rgba(0, 132, 255, 0.15) !important;
        padding: 4px 10px !important;
        transition: all 0.3s ease-in-out !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #0084FF !important;
        box-shadow: 0 0 25px rgba(0, 132, 255, 0.4) !important;
        transform: translateY(-2px);
    }

    div[data-testid="stChatInput"] > div {
        background: transparent !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #F0F4FF !important;
        font-size: 15px !important;
    }

    div[data-testid="stChatInput"] button {
        background-color: #0084FF !important;
        color: #FFFFFF !important;
        border-radius: 50% !important;
        border: none !important;
        transition: transform 0.2s ease !important;
    }

    div[data-testid="stChatInput"] button:hover {
        transform: scale(1.1);
    }

    [data-testid="stChatMessageAvatar"],
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    @keyframes bubbleAppear {
        0% {
            opacity: 0;
            transform: translateY(15px) scale(0.96);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    .chat-row {
        display: flex;
        width: 100%;
        margin-bottom: 18px;
        animation: bubbleAppear 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }

    .user-row { justify-content: flex-end; }
    .sky-row { justify-content: flex-start; }

    .user-bubble {
        background: linear-gradient(135deg, #0084FF, #0055FF);
        color: #FFFFFF;
        border-radius: 20px 20px 4px 20px;
        padding: 12px 18px;
        max-width: 80%;
        font-size: 15px;
        word-break: break-word;
        box-shadow: 0 4px 15px rgba(0, 132, 255, 0.25);
    }

    .sky-bubble {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #E2E8F0;
        border-radius: 20px 20px 20px 4px;
        padding: 14px 20px;
        max-width: 85%;
        font-size: 15px;
        word-break: break-word;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .typing-dots {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 4px;
    }

    .typing-dots span {
        width: 8px;
        height: 8px;
        background-color: #0084FF;
        border-radius: 50%;
        display: inline-block;
        animation: bounce 1.4s infinite ease-in-out both;
        box-shadow: 0 0 10px #0084FF;
    }

    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }

    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); opacity: 0.3; }
        40% { transform: scale(1.2); opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Google AI Studio API Key
API_KEY = "AQ.Ab8RN6JNGdqWs_UXR_015I6de0pgCFJH9Yd4Cg-jbFTZGKZGEA"

if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=API_KEY)

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.6-flash",
        config={"system_instruction": system_instruction}
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# Başlık
st.markdown("<h2 style='text-align: center; color: #E0E0FF; font-weight: 300; margin-top: 10px; margin-bottom: 20px;'>Sky</h2>", unsafe_allow_html=True)

# Geçmiş Mesajlar
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-row user-row"><div class="user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-row sky-row"><div class="sky-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)

# Giriş Kutusu
user_input = st.chat_input("Sky'a sorun...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-row user-row"><div class="user-bubble">{user_input}</div></div>', unsafe_allow_html=True)

    # 3 Nokta Düşünüyor Animasyonu Kutusu
    sky_message_placeholder = st.empty()
    sky_message_placeholder.markdown(
        '<div class="chat-row sky-row"><div class="sky-bubble"><div class="typing-dots"><span></span><span></span><span></span></div></div></div>',
        unsafe_allow_html=True
    )

    full_text = ""
    try:
        response_stream = st.session_state.chat.send_message_stream(user_input)
        
        for chunk in response_stream:
            if chunk.text:
                full_text += chunk.text
                sky_message_placeholder.markdown(
                    f'<div class="chat-row sky-row"><div class="sky-bubble">{full_text}▌</div></div>',
                    unsafe_allow_html=True
                )
        
        sky_message_placeholder.markdown(
            f'<div class="chat-row sky-row"><div class="sky-bubble">{full_text}</div></div>',
            unsafe_allow_html=True
        )
        st.session_state.messages.append({"role": "assistant", "content": full_text})

    except APIError as e:
        sky_message_placeholder.empty()
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            st.warning("Ücretsiz kullanım limitine ulaştın. Lütfen biraz bekleyip tekrar dene.")
        else:
            st.error(f"API Hatası: {e}")
    except Exception as e:
        sky_message_placeholder.empty()
        st.error(f"Hata oluştu: {e}")

# Sayfa Sonu Kaydırma
st.markdown("<div id='scroll-bottom' style='height: 80px;'></div>", unsafe_allow_html=True)
components.html(
    """
    <script>
        setTimeout(function() {
            var el = window.parent.document.getElementById('scroll-bottom');
            if (el) {
                el.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }
        }, 150);
    </script>
    """,
    height=0,
)

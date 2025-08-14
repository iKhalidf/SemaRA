import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from rag_logic import run_rag
from streamlit import session_state


# right-align arabic text
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
    ..header-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 30px;
}
.header-container img {
    width: 100px;
    height: 100px;
}
.header-container h1 {
    margin-top: 10px;
    font-size: 2rem;
    font-weight: bold;
}
h1, h2, h3, h4, h5, h6, p, .stButton, .stTextInput, .stTextArea, .stSelectbox, .stFileUploader {
    margin-left: auto;
    margin-right: auto;
    text-align: center;
}
        * {
            direction: rtl;
            text-align: right;
            font-family: 'IBM Plex Sans';
        }
        textarea, input, .stTextInput > div > div > input {
            direction: rtl !important;
            text-align: right !important;
        }
*,
html, body,
[class*="css"],
.stTextInput, .stTextArea, .stButton, .stSelectbox, .stRadio, .stCheckbox, .stMarkdown, .stSidebar {
    font-family: 'IBM Plex Sans Arabic', sans-serif !important;
}
    </style>
""", unsafe_allow_html=True)# ====================================================
st.set_page_config(
    page_title="SemaRA • Arabic RAG",
    page_icon="assets/icon.png",
    layout="centered",                   # more horizontal space for dashboards
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://docs.yourdomain/help",
        "Report a bug": "https://docs.yourdomain/bugs",
        "About": "SemaRA — Arabic PDF RAG system"
    }
)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
    ..header-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 30px;
}
.header-container img {
    width: 100px;
    height: 100px;
}
.header-container h1 {
    margin-top: 10px;
    font-size: 2rem;
    font-weight: bold;
}
h1, h2, h3, h4, h5, h6, p, .stButton, .stTextInput, .stTextArea, .stSelectbox, .stFileUploader {
    margin-left: auto;
    margin-right: auto;
    text-align: center;
}
        * {
            direction: rtl;
            text-align: right;
            font-family: 'IBM Plex Sans';
        }
        textarea, input, .stTextInput > div > div > input {
            direction: rtl !important;
            text-align: right !important;
        }
*,
html, body,
[class*="css"],
.stTextInput, .stTextArea, .stButton, .stSelectbox, .stRadio, .stCheckbox, .stMarkdown, .stSidebar {
    font-family: 'IBM Plex Sans Arabic', sans-serif !important;
}
    </style>
""", unsafe_allow_html=True)
# ====================================================

# Logo in the center with lots of padding
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("assets/logo.png", width=150)
st.markdown("<br>", unsafe_allow_html=True)  # Bottom padding


if "db_loaded" not in session_state or not st.session_state.db_loaded:
    st.warning("أرفع الملف في الصفحة الرئيسية أول")
    st.stop()


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    role = "Human" if isinstance(msg, HumanMessage) else "AI"
    with st.chat_message(role):
        st.markdown(msg.content)


# Input
query = st.chat_input("على ايش تسأل؟")
if query:
    st.session_state.chat_history.append(HumanMessage(query))
    with st.chat_message("Human"):
        st.markdown(query)

    with st.chat_message("AI"):
        # Get RAG response
        answer = run_rag(query)
        st.markdown(answer)
        print(type(answer))
        print(repr(answer))
        st.session_state.chat_history.append(AIMessage(answer))

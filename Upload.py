import streamlit as st
from dotenv import load_dotenv
from rag_logic import extract_text, split_by_word, load_vector_db
import tempfile
load_dotenv()


# ====================================================
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
.header-container {
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
*, html, body, [class*="css"], .stTextInput, .stTextArea, .stButton, .stSelectbox, .stRadio, .stCheckbox, .stMarkdown, .stSidebar {
    font-family: 'IBM Plex Sans Arabic', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)


# ====================================================


col1, col2, col3 = st.columns([1.2, 1, 1.2])
with col2:
    st.image("assets/logo.png", width=150)



if "db_loaded" not in st.session_state:
    st.session_state.db_loaded = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []




st.title("إرفع ملفك")
uploaded_file = st.file_uploader("ارفع ملف PDF", type=["pdf"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name


    text = extract_text(temp_path)

    splits = split_by_word(text)

    load_vector_db(splits)

    st.session_state.db_loaded = True
    st.success("الملفات تحملت 🟢")

with st.sidebar:
    if st.session_state.get("db_loaded"):
        st.success("ملفاتك جاهزة للبحث 🔎")
    else:
        st.info("⬆️ ارفع الملفات أول")


st.info("بعد رفع الملف، اختار العملية من القائمة على اليمين")






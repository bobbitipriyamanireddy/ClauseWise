import os
import requests
import streamlit as st
import pandas as pd
import re

# -----------------------------
# Streamlit page setup
# -----------------------------
st.set_page_config(page_title="ClauseWise — Legal Analyzer", layout="wide")
st.markdown("""
<style>
/* General body */
body {background-color: #f5f7fa; font-family: 'Segoe UI', sans-serif;}

/* Header */
h1, h2, h3 {color: #0B3D91; font-weight: bold;}

/* Card style */
.card {
    background: #ffffff;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 6px 12px rgba(0,0,0,0.1);
}

/* Buttons */
.stButton>button {
    background-color: #0B3D91;
    color: white;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #062c63;
}

/* Text areas */
.stTextArea textarea {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 8px;
}

/* Dataframes */
.stDataFrame {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Sidebar headings */
[data-testid="stSidebar"] h2 {
    color: #0B3D91;
    font-weight: bold;
}

/* Tabs */
.css-1lcbmhc.e16nr0p30 {background-color: #e6ebf7; border-radius: 12px; padding: 10px;}
</style>
""", unsafe_allow_html=True)

st.title("⚖ ClauseWise — Legal Document Analyzer")

# -----------------------------
# API setup
# -----------------------------
API_BASE = os.getenv("CLAUSEWISE_API", "http://localhost:8000")
if "doc_text" not in st.session_state:
    st.session_state["doc_text"] = ""
if "api_base" not in st.session_state:
    st.session_state["api_base"] = API_BASE

# Sidebar
with st.sidebar:
    st.markdown("### Setup")
    st.text_input("FastAPI base URL", value=st.session_state["api_base"], key="api_base")
    st.markdown("*Tip:* Run the backend first, then this UI.")
    st.divider()
    st.markdown("*Features*")
    st.checkbox("Enable NER", value=True, key="enable_ner")
    st.checkbox("Enable classification", value=True, key="enable_cls")

# Helper functions
def get_api_base():
    return st.session_state.get("api_base", API_BASE).rstrip("/")

def api_post(path: str, json_body: dict):
    url = get_api_base() + path
    try:
        r = requests.post(url, json=json_body, timeout=120)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {e}")
        return {}

def api_upload(file_bytes: bytes, filename: str):
    url = get_api_base() + "/extract"
    files = {"file": (filename, file_bytes)}
    try:
        r = requests.post(url, files=files, timeout=120)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Upload failed: {e}")
        return {}

# Tabs
tab_upload, tab_simplify, tab_cls, tab_ner, tab_search, tab_bulk = st.tabs(
    ["📄 Upload", "📝 Simplify Clauses", "🏷 Classify", "🔎 NER", "🔍 Search", "📑 Bulk Simplify"]
)

# -----------------------------
# Upload Tab
# -----------------------------
with tab_upload:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Upload a legal document (PDF, DOCX, TXT)")
    uploaded = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    if uploaded:
        data = uploaded.read()
        uploaded.seek(0)
        with st.spinner("Extracting text…"):
            resp = api_upload(data, uploaded.name)
            text = resp.get("text", "")
            if text:
                st.session_state["doc_text"] = text
                st.success(f"Extracted {len(text)} characters.")
                st.text_area("Extracted Text", value=text[:5000], height=300)
            else:
                st.error("Extraction failed.")
    st.markdown('</div>', unsafe_allow_html=True)

doc_text = st.session_state.get("doc_text", "")

# -----------------------------
# Simplify Tab
# -----------------------------
with tab_simplify:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Simplify specific clause(s)")
    default_clause = doc_text[:1200] if doc_text else ""
    clause = st.text_area("Paste a clause to simplify", value=default_clause, height=200, key="clause_to_simplify")
    if st.button("Simplify"):
        if clause.strip():
            with st.spinner("Simplifying…"):
                resp = api_post("/simplify", {"text": clause})
                simplified = resp.get("simplified", "")
                if simplified:
                    st.success("Simplified clause:")
                    st.text_area("Plain-English", value=simplified, height=220)
                else:
                    st.error("Simplification failed.")
        else:
            st.warning("Please paste some text.")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Classification Tab
# -----------------------------
with tab_cls:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Classify document type")
    txt = st.text_area("Text to classify", value=doc_text[:4000], height=200, key="text_to_classify")
    if st.session_state.get("enable_cls") and st.button("Classify"):
        with st.spinner("Classifying…"):
            resp = api_post("/classify", {"text": txt})
            label = resp.get("label")
            if label:
                st.success(f"Predicted: *{label}*")
            else:
                st.error("Classification failed.")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# NER Tab
# -----------------------------
with tab_ner:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Named Entity Recognition")
    ner_text = st.text_area("Text to extract entities from", value=doc_text[:3000], height=200, key="ner_text")
    if st.session_state.get("enable_ner") and st.button("Extract Entities"):
        with st.spinner("Finding entities…"):
            resp = api_post("/ner", {"text": ner_text})
            ents = resp.get("entities", [])
            if ents:
                df = pd.DataFrame(ents)[["entity", "text", "score", "start", "end"]]
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", data=csv, file_name="entities.csv", mime="text/csv")
            else:
                st.info("No entities found.")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
#

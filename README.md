# ⚖️ ClauseWise — Legal Document Analyzer

AI-powered legal document analyzer combining **FastAPI** (backend) and **Streamlit** (frontend).  
ClauseWise converts complex legal text into user-friendly insights—simplifying clauses, extracting entities, classifying documents, and more.

---

## Features

- **Upload & Extract**: Supports PDF, DOCX, and TXT file formats.  
- **Clause Simplification**: Translates dense legalese into plain English.  
- **Document Classification**: Identifies types like NDA, Lease, Employment, Service Agreement.  
- **Named Entity Recognition (NER)**: Captures parties, dates, organizations, amounts, and legal terms.  
- **Keyword Search**: Quickly find matching clauses or terms.  
- **Bulk Simplify**: Streamline multiple clauses simultaneously.  

---

## Tech Stack

- **Backend**: FastAPI, Hugging Face Transformers, PyTorch  
- **Frontend**: Streamlit  
- **Libraries**: pypdf, python-docx, pandas, re  

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/YOUR-USERNAME/ClauseWise.git
cd ClauseWise

# 2. Project structure
# ClauseWise/
# ├── backend/
# │   ├── main.py
# │   ├── requirements.txt
# │   └── ... (other backend files)
# ├── frontend/
# │   ├── app.py
# │   ├── requirements.txt
# │   └── ... (other frontend files)
# ├── README.md
# └── ... (other project files)

# 3. Install and run Backend (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 4. Open a new terminal, install and run Frontend (Streamlit)
cd frontend
pip install -r requirements.txt
streamlit run app.py

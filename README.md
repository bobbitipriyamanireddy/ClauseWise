# ⚖️ **ClauseWise — Legal Document Analyzer**

AI-powered legal document analyzer built with **FastAPI** (backend) and **Streamlit** (frontend).  
It simplifies and classifies legal documents, extracts entities, and provides quick clause search.  


🚀 Features

Clause Simplification → Rewrites complex legal text into plain English.

Named Entity Recognition (NER) → Extracts parties, dates, amounts, legal terms.

Clause Extraction & Breakdown → Sements legal contracts into smaller clauses.

Document Classification → Predicts type: NDA, Lease, Employment, Service Agreement.

Multi-format Support → Upload PDF, DOCX, TXT files.

Search & Bulk Simplify → Keyword-based search and full document simplification.

🛠️ Tech Stack

Backend → FastAPI, Hugging Face Transformers, PyTorch

Frontend → Streamlit

Other Tools → Hugging Face Hub, PyPDF, python-docx

📂 Project Structure
ClauseWise/
│── app.py             # Streamlit frontend
│── main.py            # FastAPI backend
│── test_ner.py        # Testing NER
│── requirements.txt   # Dependencies
│── README.md          # Documentation

⚡ Setup & Installation
1️⃣ Clone Repository
git clone https://github.com/your-username/ClauseWise.git
cd ClauseWise

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Backend (FastAPI)
uvicorn main:app --reload --host 0.0.0.0 --port 8000


API available at 👉 http://localhost:8000/docs

5️⃣ Run Frontend (Streamlit)
streamlit run app.py

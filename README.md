
# 🧠 AI Codebase Copilot (Pro)

Advanced multi-agent code understanding system using RAG + local LLMs.

## Features
- Codebase ingestion (local)
- RAG with FAISS
- Chat-based code Q&A
- Architecture explanation
- File-aware answers
- Clean UI

## Run
pip install -r requirements.txt
ollama pull mistral

uvicorn backend.main:app --reload
streamlit run frontend/app.py

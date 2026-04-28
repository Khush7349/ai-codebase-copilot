# 🧠 AI Codebase Copilot

An AI-powered developer assistant that understands and explains entire codebases using **RAG (Retrieval-Augmented Generation)**, **LangGraph multi-agent workflows**, and a **local LLM (Ollama)** — all wrapped in an intuitive IDE-style interface.

---

## 🚀 Overview

Understanding large codebases is time-consuming and difficult.

**AI Codebase Copilot** solves this by allowing you to:
- Ask questions about any codebase
- Get contextual answers with file references
- Explore code using an IDE-like interface
- Analyze architecture automatically

👉 All **locally**, without any paid APIs.

---

## 🏗️ Architecture
```
User Query
↓
LangGraph Multi-Agent Workflow
↓
Query Refinement → Retrieval (FAISS) → Context Builder → LLM
↓
Answer + Source Context
```

---

## 🧩 Tech Stack

- **LLM** → Ollama (Mistral, local)
- **Agents** → LangGraph
- **Embeddings** → Sentence Transformers
- **Vector DB** → FAISS
- **Backend** → FastAPI
- **Frontend** → Streamlit (IDE-style UI)

---

## ✨ Features

### 🧠 Intelligent Code Understanding
- Ask natural language questions about code
- Context-aware answers using RAG

### 🔍 Source-Aware Responses
- Answers include relevant file references
- Transparent reasoning via retrieved code

### 🏗️ Architecture Analysis
- Auto-generates system architecture explanations
- Identifies components and data flow

### 💻 IDE-Style Interface
- File explorer
- Code viewer
- Integrated chat assistant

### 🔄 Multi-Agent Workflow (LangGraph)
- Query refinement agent
- Retrieval agent
- Context builder
- Answer generation agent

### 🔒 Fully Local & Free
- No API keys required
- Runs entirely on your machine

---

## ⚙️ Setup Instructions

### 1. Clone Repository
- git clone https://github.com/your-username/ai-codebase-copilot.git
- cd ai-codebase-copilot
---
### 2. Install Dependencies
- pip install -r requirements.txt
---
### 3. Install and Run Ollama
- Download from: https://ollama.com
- Pull model: ollama pull mistral
- Run: ollama run mistral
---
### 4. Start Backend
uvicorn main:app --reload
---
### 5. Start Frontend
streamlit run app.py
---

## 🧪 Usage

1. Load a local repository  
2. Navigate using IDE interface  
3. Ask questions like:
   - “Explain this project”
   - “Where is authentication handled?”
   - “How does the data flow work?”
---

## 🎯 Key Highlights

- Multi-agent orchestration using LangGraph  
- Code-aware RAG pipeline  
- Fully local AI system (no API dependency)  
- Developer-focused UI (not just a chatbot)  

---

## 🚀 Future Improvements

- Code line highlighting from context  
- GitHub repo ingestion (remote)  
- Advanced multi-agent routing  
- Streaming responses  

---

## 🤝 Contributing

Pull requests and ideas are welcome!

---

## 👤 Author

Khushi Sharma

---

## ⭐ If You Like This Project

Give it a star on GitHub ⭐

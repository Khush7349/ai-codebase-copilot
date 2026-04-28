from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from loader import load_repo
from rag import add, reset
from graph import app_graph

app = FastAPI(
    title="AI Codebase Copilot API",
    version="1.0"
)

state = {
    "repo_loaded": False,
    "file_count": 0,
    "files": []
}

class LoadRequest(BaseModel):
    path: str


class QueryRequest(BaseModel):
    question: str

@app.post("/load")
def load_repo_endpoint(req: LoadRequest):
    try:
        if not os.path.exists(req.path):
            raise HTTPException(status_code=400, detail="Invalid path")
        reset()

        files = load_repo(req.path)

        if not files:
            raise HTTPException(status_code=400, detail="No valid code files found")

        add(files)

        state["repo_loaded"] = True
        state["file_count"] = len(files)
        state["files"] = [f["path"] for f in files]

        return {
            "message": "Repository loaded successfully",
            "files_loaded": len(files)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def ask_endpoint(req: QueryRequest):
    if not state["repo_loaded"]:
        raise HTTPException(
            status_code=400,
            detail="Repository not loaded. Please load a repo first."
        )

    try:
        result = app_graph.invoke({
            "question": req.question
        })

        return {
            "answer": result.get("answer", ""),
            "context": result.get("context", [])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/explain")
def explain_endpoint():
    if not state["repo_loaded"]:
        raise HTTPException(
            status_code=400,
            detail="Repository not loaded"
        )

    try:
        result = app_graph.invoke({
            "question": "Explain the architecture of this codebase"
        })

        return {
            "summary": result.get("answer", "")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
def get_files():
    if not state["repo_loaded"]:
        raise HTTPException(status_code=400, detail="Repository not loaded")

    return {
        "files": state.get("files", [])
    }
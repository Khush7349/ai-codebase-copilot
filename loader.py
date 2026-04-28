import os
EXCLUDE_DIRS = {
    ".git", "node_modules", "__pycache__", "venv",
    "dist", "build", ".idea", ".vscode"
}

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".java", ".cpp", ".c", ".go"
}

MAX_FILE_SIZE = 100_000  
def safe_read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(path, "r", encoding="latin-1") as f:
                return f.read()
        except Exception:
            return None
    except Exception:
        return None
def load_repo(repo_path):
    code_files = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.startswith("."):
                continue

            ext = os.path.splitext(file)[1]
            if ext not in SUPPORTED_EXTENSIONS:
                continue

            full_path = os.path.join(root, file)
            try:
                if os.path.getsize(full_path) > MAX_FILE_SIZE:
                    continue
            except Exception:
                continue

            content = safe_read_file(full_path)
            if not content or not content.strip():
                continue

            code_files.append({
                "path": os.path.normpath(full_path),
                "name": file,
                "extension": ext,
                "content": content
            })

    return code_files
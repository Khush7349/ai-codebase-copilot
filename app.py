import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(
    layout="wide",
    page_title="AI Codebase Copilot",
    page_icon="🧠"
)

# -------------------- STYLING --------------------
st.markdown("""
<style>
body { background-color: #0e1117; }

.main-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 10px;
}

.subtle {
    color: #9ca3af;
    font-size: 0.9rem;
}

.sidebar-title {
    font-size: 1.4rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "repo_loaded" not in st.session_state:
    st.session_state.repo_loaded = False

if "files" not in st.session_state:
    st.session_state.files = []

if "selected_file" not in st.session_state:
    st.session_state.selected_file = None

st.sidebar.markdown('<div class="sidebar-title">🧠 Copilot Pro</div>', unsafe_allow_html=True)

mode = st.sidebar.radio(
    "Navigation",
    ["Load Repository", "Chat Assistant", "Architecture", "IDE Assistant"]
)

st.sidebar.markdown("---")

if st.session_state.repo_loaded:
    st.sidebar.success("✅ Repo Loaded")
else:
    st.sidebar.warning("⚠️ No Repo Loaded")

st.markdown('<div class="main-title">💻 AI Codebase Copilot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtle">Understand, navigate, and analyze any codebase with AI</div>', unsafe_allow_html=True)

st.markdown("---")

if mode == "Load Repository":

    st.subheader("📂 Load Local Repository")

    path = st.text_input("Enter repository path")

    if st.button("Load Repository"):
        if not path:
            st.error("Please enter a valid path")
        else:
            with st.spinner("Indexing repository..."):
                try:
                    r = requests.post(f"{API}/load", json={"path": path})
                    data = r.json()

                    if r.status_code != 200:
                        st.error(data.get("detail", "Error loading repository"))
                    else:
                        st.session_state.repo_loaded = True
                        st.success(f"Loaded {data.get('files_loaded', 0)} files")

                        # Fetch file list
                        try:
                            f = requests.get(f"{API}/files")
                            st.session_state.files = f.json().get("files", [])
                        except:
                            st.session_state.files = []

                except Exception as e:
                    st.error(f"Error: {str(e)}")

elif mode == "Chat Assistant":

    st.subheader("💬 Ask Questions About Code")

    if not st.session_state.repo_loaded:
        st.warning("Please load a repository first.")
        st.stop()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask something about the codebase...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing code..."):
                try:
                    r = requests.post(
                        f"{API}/ask",
                        json={"question": user_input}
                    )
                    data = r.json()

                    if r.status_code != 200:
                        st.error(data.get("detail", "Error processing request"))
                    else:
                        answer = data.get("answer", "No response")
                        context = data.get("context", [])

                        st.markdown(answer)

                        if context:
                            with st.expander("📂 View Source Context"):
                                for item in context:
                                    try:
                                        content, path = item
                                        st.markdown(f"**📄 {path}**")
                                    except:
                                        st.markdown(str(item))

                except Exception as e:
                    st.error(f"Error: {str(e)}")

        st.session_state.messages.append({"role": "assistant", "content": answer})

elif mode == "Architecture":

    st.subheader("🏗️ Project Architecture Overview")

    if not st.session_state.repo_loaded:
        st.warning("Please load a repository first.")
        st.stop()

    if st.button("Generate Architecture Explanation"):
        with st.spinner("Analyzing architecture..."):
            try:
                r = requests.get(f"{API}/explain")
                data = r.json()

                if r.status_code != 200:
                    st.error(data.get("detail", "Error generating explanation"))
                else:
                    st.markdown("### 🧠 System Overview")
                    st.markdown(data.get("summary", "No data"))

            except Exception as e:
                st.error(f"Error: {str(e)}")

elif mode == "IDE Assistant":

    st.subheader("🧠 IDE Assistant (Code + Chat)")

    if not st.session_state.repo_loaded:
        st.warning("Please load a repository first.")
        st.stop()

    col1, col2, col3 = st.columns([1, 2, 2])

    with col1:
        st.markdown("### 📂 Files")

        for f in st.session_state.files:
            if st.button(f, key=f"file_{f}"):
                st.session_state.selected_file = f

    with col2:
        st.markdown("### 💻 Code Viewer")

        if st.session_state.selected_file:
            try:
                with open(st.session_state.selected_file, "r", encoding="utf-8") as file:
                    code = file.read()

                st.code(code, language="python")

            except Exception:
                st.error("Unable to open file")
        else:
            st.info("Select a file")

    with col3:
        st.markdown("### 💬 Assistant")

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Ask about selected code...")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        r = requests.post(
                            f"{API}/ask",
                            json={"question": user_input}
                        )
                        data = r.json()

                        answer = data.get("answer", "")
                        context = data.get("context", [])

                        st.markdown(answer)

                        if context:
                            with st.expander("📂 Sources"):
                                for item in context:
                                    try:
                                        _, path = item
                                        st.markdown(f"📄 {path}")
                                    except:
                                        pass

                    except Exception as e:
                        st.error(str(e))

            st.session_state.messages.append({"role": "assistant", "content": answer})
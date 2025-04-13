import os
import streamlit as st
from pathlib import Path
from data_ingestion import ingest_documents
from chat_chain import create_qa_chain
from local_model import load_local_llm  # kept for local dev
from feedback import is_allowed_by_moderation
from prompts import QA_PROMPT
from langchain.chat_models import ChatOpenAI


os.environ["OPENAI_API_KEY"] = st.secrets["openai"]["OPENAI_API_KEY"]

# Streamlit page config
st.set_page_config(page_title="GradBoss AI Chatbot", page_icon="🎓", layout="wide")
st.title("🎓 GradBoss Academic Chatbot")
st.markdown("Upload your academic docs and ask questions. Powered by GPT-3.5 & LangChain.")

# Sidebar
with st.sidebar:
    st.header("📂 Upload Documents")
    uploaded_files = st.file_uploader("PDF/TXT/DOCX only", type=["pdf", "txt", "docx"], accept_multiple_files=True)

    st.markdown("---")
    st.markdown("### 🧠 How to Use This App")
    st.markdown("""
Welcome to **GradBoss Academic Chatbot**, an AI-powered assistant developed by **Anubhav** for GradBoss.

This tool helps students:
- 📄 Upload PDFs, DOCX, or TXT academic files
- 🤖 Ask questions like “summarize the document” or “what are the main challenges?”
- 🧠 Get responses powered by GPT-3.5 + LangChain (no hallucinations!)

Answers are always grounded in your uploaded documents.
""")

    st.markdown("#### 🔒 Ethical AI")
    st.markdown("""
- ✅ Retrieval-Augmented Generation (RAG)
- 🧠 Conversational Memory
- 🙅 If the bot doesn’t know, it says so!
""")
    st.markdown("---")
    st.caption("Powered by GPT-3.5 · Built by Anubhav · 2025")

# Session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []

# Document processing
if uploaded_files:
    doc_paths = []
    Path("uploaded_docs").mkdir(exist_ok=True)
    for file in uploaded_files:
        filepath = Path("uploaded_docs") / file.name
        filepath.write_bytes(file.getvalue())
        doc_paths.append(str(filepath))

    with st.spinner("Indexing documents..."):
        vectorstore = ingest_documents(doc_paths, persist_dir="vector_store")
        st.session_state.vectorstore = vectorstore

        # Use GPT-3.5 (OpenAI) for deployed version
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        st.toast("✅ QA Chain initialized successfully", icon="✅")

        st.session_state.qa_chain = create_qa_chain(vectorstore, llm=llm)
        st.success("Documents indexed and chatbot ready!")

# Chat interface
if st.session_state.qa_chain:
    user_input = st.chat_input("Ask a question about your documents...")
    if user_input:
        st.chat_message("user").write(user_input)
        if not is_allowed_by_moderation(user_input):
            st.chat_message("assistant").write("⚠️ Sorry, I cannot answer that.")
        else:
            result = st.session_state.qa_chain({"question": user_input})
            answer = result["answer"]
            st.chat_message("assistant").write(answer)
            st.session_state.chat_history.append((user_input, answer))

            # Feedback buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍", key=f"up_{len(st.session_state.chat_history)}"):
                    st.session_state.feedback.append({"q": user_input, "a": answer, "vote": "up"})
            with col2:
                if st.button("👎", key=f"down_{len(st.session_state.chat_history)}"):
                    st.session_state.feedback.append({"q": user_input, "a": answer, "vote": "down"})

import os
from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# Initialize the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def ingest_documents(file_paths, persist_dir="vector_store"):
    """
    Load documents from file_paths, split them into chunks, embed them, and store in ChromaDB.
    """
    all_documents = []
    for file_path in file_paths:
        ext = file_path.split(".")[-1].lower()
        if ext == "pdf":
            loader = PyPDFLoader(file_path)
            docs = loader.load()
        elif ext == "txt":
            loader = TextLoader(file_path, encoding='utf-8')
            docs = loader.load()
        elif ext == "docx":
            loader = Docx2txtLoader(file_path)
            docs = loader.load()
        else:
            print(f"❌ Skipping unsupported file: {file_path}")
            continue
        all_documents.extend(docs)

    # Split into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunked_docs = text_splitter.split_documents(all_documents)

    # Create Chroma vector DB
    vectorstore = Chroma.from_documents(
        chunked_docs,
        embedding_model,
        persist_directory=persist_dir
    )
    vectorstore.persist()
    return vectorstore


#Explanation
"""
data_ingestion.py — both in theory and practice — so you fully understand how your chatbot's “brain” is built 👇

🧠 What Is This Step?
This step is about preparing your documents so your chatbot can understand and retrieve the right information when asked.
We're doing four major tasks:

✅ 1. Loading PDFs, TXT, and DOCX Files
📘 Theory:
Your documents (like a syllabus, course notes, academic calendar, etc.) are stored in different formats (PDF, text, Word).


These need to be read and converted into plain text so we can process and understand their content.


🛠️ What We Use:
LangChain’s loaders abstract away the logic to read each file type and return a clean Document object.


PyPDFLoader → for PDFs


TextLoader → for plain .txt files


Docx2txtLoader → for Microsoft Word .docx


Each loader outputs a list of Document objects that LangChain understands (each with .page_content + .metadata).

✅ 2. Chunking the Text with Overlap
📘 Theory:
LLMs like GPT-3.5 have a token limit (~4,096 tokens), and longer documents can’t fit into a single prompt.


Also, embeddings work better when context is small and focused.


So we break long texts into smaller overlapping chunks, each of which will be independently embedded.


🛠️ What We Use:
CharacterTextSplitter from LangChain:


chunk_size=1000 means each chunk is up to 1000 characters.


chunk_overlap=100 means each chunk shares 100 characters with the next to preserve context between them.


Example:
If your doc is:
css
CopyEdit
"This is a long syllabus. It covers multiple topics. Topic A is about ML. Topic B is about AI..."

Then chunking would produce:
nginx
CopyEdit
Chunk 1: "This is a long syllabus. It covers multiple topics. Topic A is about ML."
Chunk 2: "covers multiple topics. Topic A is about ML. Topic B is about AI..."

This overlapping preserves coherence for Q&A tasks.

✅ 3. SentenceTransformer Embeddings
📘 Theory:
LLMs generate answers by reading documents retrieved based on semantic similarity.


So we need to convert each chunk into a vector — a numerical representation of its meaning.


This is done using embeddings.


🛠️ What We Use:
sentence-transformers/all-MiniLM-L6-v2:


Small, fast, and accurate embedding model


Maps each text chunk to a 384-dimensional vector


Captures semantic meaning: “student login” and “access portal” will have similar vectors


These vectors are what make it possible to later retrieve the “most relevant chunks” for any question you ask.

✅ 4. ChromaDB Indexing with Persistence
📘 Theory:
We need to store and search these vectors efficiently.


A vector database lets us:


Store the chunk + its vector


Query “which chunks are most similar to this question?”


We also want this to persist (save to disk) so we don’t have to re-process files every time.


🛠️ What We Use:
ChromaDB:


Lightweight vector database


Fast, local, and works offline


Perfect for prototyping and even small production apps


We use:

 python
CopyEdit
Chroma.from_documents(..., persist_directory=\"vector_store\")
vectorstore.persist()
 This saves the vector DB in a folder called vector_store/.



📦 Why This Step Is Critical
This is the foundation of Retrieval-Augmented Generation (RAG).
Without this, your chatbot would:
Only rely on its pretrained knowledge (GPT), not your course docs


Risk hallucinations and miss document-specific answers


Lose context after a long prompt


With this step, you’ve created a searchable, intelligent memory of your documents.



chat_chain.py — here’s exactly what’s going on behind the scenes and why it’s critical to your GradBoss academic chatbot 🔍
"""
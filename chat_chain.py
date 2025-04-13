from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from prompts import QA_PROMPT

def create_qa_chain(vectorstore, llm):
    """
    Builds a conversational RAG (retrieval-augmented generation) chain using:
    - An LLM (GPT-3.5 or fallback)
    - A retriever (e.g., ChromaDB)
    - A memory object to hold conversation history
    - A custom QA prompt template
    """
    # ✅ Move memory creation INSIDE the function so it links properly
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"  # 🔑 This is what makes the error go away
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True,
        output_key="answer"
    )

    return qa_chain

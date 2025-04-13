from langchain.prompts import PromptTemplate

# Custom prompt for academic assistant behavior
# - Avoid hallucination
# - Answer only from context
# - Respond in a helpful, structured way
# - Use reasoning steps (Chain-of-Thought)

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are GradBoss, an AI academic assistant. Your job is to help students by answering their questions
based ONLY on the provided context documents. Do not use any outside knowledge.

Instructions:
- If the context contains the answer, provide a detailed academic-style explanation.
- If the answer is not in the context, say "I'm not sure based on the provided information."
- Be concise, clear, and do not fabricate facts.
- Think step-by-step and explain your reasoning if helpful.

Context:
{context}

Question:
{question}

Helpful Answer:
"""
)



#Explanation
"""
Why We Need prompts.py
A prompt is what you give to the LLM (like GPT-3.5) to guide its behavior. Without a clear prompt:

It might hallucinate information (make things up)

Use inconsistent tone or format

Answer from general world knowledge instead of your documents

prompts.py defines a template — a structured instruction — that controls:

What the bot is

How it should behave

What to do when information is missing

How to sound (tone, clarity, length, structure)

This is essential when you're building a production-ready GenAI assistant.

🧠 Explanation of Each Element
🎓 “You are GradBoss, an AI academic assistant...”
Purpose: Sets the identity and context for the model.

Effect: Makes it behave more like a tutoring assistant and less like a casual chatbot.

Why important: The LLM’s persona affects tone, formality, and how it structures information. You want a calm, academic tone here — not something like ChatGPT’s general chattiness.

🔒 “Answer based ONLY on the provided context documents”
Purpose: Tells the LLM to treat the retrieved document chunks as its entire source of truth.

Effect: Prevents the model from using its pretrained general knowledge (which may be outdated or wrong).

Why important: You're using a RAG system — the whole point is to answer based on indexed documents, not guesswork.

🙅‍♂️ “If the answer is not in the context, say 'I'm not sure…'”
Purpose: Gives the model explicit permission to not answer.

Effect: Prevents hallucination and builds user trust.

Why important: In production apps, it’s better for an AI to say “I don’t know” than to make up a false answer.

🧠 “Think step-by-step and explain your reasoning if helpful”
Purpose: Applies Chain-of-Thought (CoT) prompting.

Effect: Encourages the model to reason more carefully, especially for complex queries (e.g., “What classes should I take for AI?”).

Why important: CoT improves accuracy and makes the response more interpretable for users — they see how the answer was formed.

🗂️ {context} and {question} variables
These get dynamically filled in:

{context} ← comes from the ChromaDB retriever (top-k relevant chunks)

{question} ← comes from the user’s latest input

You can even add examples (few-shot) here later if you want to improve structure.

🧩 Summary
This prompt ensures that your chatbot:

Feature	Benefit
🎓 Academic identity	Sound formal, structured
🔒 Context-only answers	Reduces hallucination
🙅 Honest fallback	Doesn’t pretend to know
🧠 Chain-of-thought	More accurate, reasoned replies
💡 Think of prompts.py as the ethical contract + tone of voice + behavior rulebook for your AI.


"""
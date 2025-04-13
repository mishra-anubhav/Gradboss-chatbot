# local_model.py

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from langchain.llms import HuggingFacePipeline

def load_local_llm(model_name="google/flan-t5-small"):
    """
    Loads a lightweight open-source model (like Flan-T5) for local inference.
    Returns a LangChain-compatible LLM wrapper.
    """
    # Load tokenizer and model from Hugging Face
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Set up a text2text-generation pipeline
    hf_pipeline = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    device=-1  # 🔁 Force CPU (device -1)
    )


    # Wrap it in LangChain-compatible format
    local_llm = HuggingFacePipeline(pipeline=hf_pipeline)
    return local_llm

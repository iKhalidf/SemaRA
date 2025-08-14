from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain_core.prompts.prompt import PromptTemplate
from chromadb.config import Settings
from typing import List
from langchain.vectorstores import Chroma
import chromadb
chroma_client = chromadb.Client()
import re

import os



load_dotenv()

# Initialize embedding model once
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Chroma persistence directory
CHROMA_DIR = "./chroma_langchain_db"

# Global vector DB variable
db = None


# ====================== new ==========================

def extract_text(path: str) -> str:
    pages = PyPDFLoader(path).load()
    text = "\n".join(p.page_content for p in pages)
    return text


def split_by_word(text: str) -> List[str]:
    chunks = []
    matches = list(re.finditer(r"(?m)^\s*المادة\s+\S+", text))

    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunks.append(text[start:end])

    return chunks

def load_vector_db(splits: list[str]) -> None:
    global db
    chroma_client = chromadb.Client()
    db = Chroma.from_texts(
        texts=splits,
        embedding=embeddings,
        collection_name="rag_docs",
        client=chroma_client,
        persist_directory="chroma_db"
    )
    db.persist()

def query_vector_db(query: str) -> list:
    global db
    if db is None:
        raise RuntimeError("Vector DB is not loaded. Please run load_vector_db() first.")
    results = db.similarity_search(query, k=10)

    return [
        {"text": doc.page_content}
        for doc in results
    ]


def format_context(docs: list[dict]) -> str:
    return "\n".join(doc["text"] for doc in docs)


def run_rag(query: str):
    global db

    retrieved_docs = query_vector_db(query)
    """
    article_nums = extract_article_numbers(retrieved_docs)
    articles_str = "، ".join(article_nums) if article_nums else "غير متوفر"
    """
    context = format_context(retrieved_docs)

    prompt_template = PromptTemplate.from_template(f"""
    You are a highly skilled legal assistant. Your task is to answer questions strictly based on the provided "Context", which comes from an Arabic legal document extracted from PDF files.

    Instructions:
    - The Context may contain corrupted, misspelled, or noisy words due to OCR or PDF extraction errors (e.g., "المؤؤؤؤسسة" instead of "المؤسسة").
    - If you encounter an unclear, corrupted, or misspelled word, do your best to infer the correct word or intended meaning from the sentence and overall context.
    - Use your knowledge of common legal and academic terminology to interpret likely intended words, and base your answer on this understanding.
    - Do not ignore a corrupted word if it is critical to the question—always attempt to recover its meaning from context.
    - If the answer is not found in the context, reply with: "لم يتم العثور على الإجابة في الوثيقة." or "Not found in the provided document." based on the question and Context language.
    - Always cite the article or section number if available in the context (e.g., "المادة الثالثة", "Article 3").
    - Respond in clear and simple Arabic if the question is in Arabic, or in simple English if the question is in English. Do not translate unless requested.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """)

    prompt = prompt_template.format(
        context=context,
        query=query
    )

    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,
        max_tokens=2000
    )
    answer = llm.invoke(prompt)
    return answer.content

import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from openai import OpenAI

from backend.vector_store import (
    create_embeddings,
    store_embeddings,
    search_similar_chunks
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def load_pdf(file_path):

    loader = PyPDFLoader(file_path)

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    text_chunks = []

    for chunk in chunks:

        text_chunks.append(
            chunk.page_content
        )

    embeddings = create_embeddings(
        text_chunks
    )

    store_embeddings(
        text_chunks,
        embeddings
    )

    return len(text_chunks)


def ask_question(question):

    retrieved_docs = search_similar_chunks(
        question,
        k=3
    )

    context = "\n".join(
        [
            chunk
            for chunk, score in retrieved_docs
        ]
    )

    prompt = f"""
You are a helpful AI assistant.

Answer only using the provided context.

If the answer is unavailable in the context, say:

"I could not find the answer in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(

        model="meta-llama/llama-3.1-8b-instruct",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    similarity_score = retrieved_docs[0][1]

    return {

        "answer": answer,

        "score": similarity_score,

        "source": "Uploaded PDF"
    }
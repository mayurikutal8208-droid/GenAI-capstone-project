import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Embedding dimension
dimension = 384

# Create FAISS index
index = faiss.IndexFlatL2(dimension)

# Store text chunks
document_chunks = []


def create_embeddings(text_chunks):

    embeddings = embedding_model.encode(
        text_chunks,
        show_progress_bar=True
    )

    embeddings = np.array(
        embeddings
    ).astype("float32")

    return embeddings


def store_embeddings(text_chunks, embeddings):

    global document_chunks

    index.add(embeddings)

    document_chunks.extend(text_chunks)

    print(f"Added {len(text_chunks)} chunks")
    print(f"Total chunks stored: {len(document_chunks)}")


def search_similar_chunks(question, k=3):

    if len(document_chunks) == 0:

        return [
            (
                "No documents uploaded yet.",
                0
            )
        ]

    # Convert query to embedding
    question_embedding = embedding_model.encode(
        [question]
    )

    question_embedding = np.array(
        question_embedding
    ).astype("float32")

    # Similarity search
    distances, indices = index.search(
        question_embedding,
        k
    )

    retrieved_chunks = []

    for idx, distance in zip(
            indices[0],
            distances[0]
    ):

        if idx != -1:

            retrieved_chunks.append(
                (
                    document_chunks[idx],
                    float(distance)
                )
            )

    return retrieved_chunks
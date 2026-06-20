import os

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from backend.rag import (
    load_pdf,
    ask_question
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@app.get("/")
def home():

    return {
        "message": "Backend running successfully"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as f:

        f.write(
            await file.read()
        )

    chunks = load_pdf(
        file_path
    )

    return {

        "message": "Document uploaded successfully",

        "chunks_created": chunks
    }


@app.post("/ask")
async def ask(
        data: dict
):

    question = data["question"]

    result = ask_question(
        question
    )

    return result
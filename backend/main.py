from pypdf import PdfReader
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ai import ask_ai
from database import (
    create_database,
    save_document,
    get_document,
    DATABASE
)
import sqlite3
import shutil
import os


app = FastAPI()


# ==========================================
# Create Database
# ==========================================

create_database()


# ==========================================
# Enable CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Upload Folder
# ==========================================

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# Question Model
# ==========================================

class Question(BaseModel):
    document_id: int
    question: str


# ==========================================
# Home
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Backend is working!"
    }


# ==========================================
# Get All Documents
# ==========================================

@app.get("/documents")
def get_documents():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, filename
        FROM documents
        ORDER BY id ASC
        """
    )

    documents = cursor.fetchall()

    connection.close()

    return {
        "documents": [
            {
                "id": row[0],
                "filename": row[1]
            }
            for row in documents
        ]
    }


# ==========================================
# Upload PDF
# ==========================================

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    # Check file
    if not file.filename.lower().endswith(".pdf"):

        return {
            "message": "Only PDF files are allowed."
        }


    # File path
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )


    # Save PDF
    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    # Extract PDF text
    reader = PdfReader(file_path)

    text = ""


    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"


    # Save document to database
    document_id = save_document(
        file.filename,
        text
    )


    print("--------------------------------")
    print("PDF uploaded successfully")
    print("Filename:", file.filename)
    print("Document ID:", document_id)
    print("--------------------------------")


    # Return document ID to frontend
    return {

        "message": "File uploaded successfully",

        "filename": file.filename,

        "document_id": document_id

    }


# ==========================================
# Ask Question
# ==========================================

@app.post("/ask")
async def ask(question: Question):

    print("--------------------------------")
    print("Received document ID:",
          question.document_id)

    print("Question:",
          question.question)


    # Get document from database
    document = get_document(
        question.document_id
    )


    print("Found document:", document)
    print("--------------------------------")


    # Document does not exist
    if document is None:

        return {
            "answer": "Document not found."
        }


    filename, content = document


    # AI prompt
    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the information in the uploaded document.

If the answer is not present in the document, reply:

"I couldn't find that information in the uploaded document."

Document name:
{filename}

Document:
{content}

Question:
{question.question}

Answer:
"""


    # Ask AI
    answer = ask_ai(prompt)


    print("AI ANSWER:", answer)


    return {

        "answer": answer

    }
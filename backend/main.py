from pypdf import PdfReader
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ai import ask_ai
from database import create_database, save_document, get_document
import sqlite3
import shutil
import os

app = FastAPI()

# Create database
create_database()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store extracted PDF text
pdf_text = ""


class Question(BaseModel):
    document_id: int
    question: str


@app.get("/")
def home():
    return {"message": "Backend is working!"}
@app.get("/documents")
def get_documents():
    connection = sqlite3.connect("documents.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, filename FROM documents"
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


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global pdf_text

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    pdf_text = text

    document_id = save_document(file.filename, text)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "document_id": document_id
    }


@app.post("/ask")
async def ask(question: Question):

    print("Received document ID:", question.document_id)

    document = get_document(question.document_id)

    print("Found document:", document)

    if document is None:
        return {
            "answer": "Document not found."
        }

    filename, content = document

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

    answer = ask_ai(prompt)

    print("AI ANSWER:", answer)

    return {
        "answer": answer
    }
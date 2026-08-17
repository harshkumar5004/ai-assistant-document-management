from pypdf import PdfReader
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ai import ask_ai
import shutil
import os

app = FastAPI()

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
    question: str


@app.get("/")
def home():
    return {"message": "Backend is working!"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global pdf_text

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save uploaded PDF
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read PDF
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    # Store extracted text
    pdf_text = text

    print(pdf_text)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }


@app.post("/ask")
async def ask(question: Question):
    global pdf_text

    if pdf_text == "":
        return {
            "answer": "Please upload a PDF first."
        }

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the information in the uploaded document.

If the answer is not present in the document, reply:
"I couldn't find that information in the uploaded document."

Document:
{pdf_text}

Question:
{question.question}

Answer:
"""

    answer = ask_ai(prompt)

    print("AI ANSWER:", answer)

    return {
        "answer": answer
    }
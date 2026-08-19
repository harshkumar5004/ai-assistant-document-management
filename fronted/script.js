// Check backend connection
async function getMessage() {
    const response = await fetch("http://127.0.0.1:8000/");
    const data = await response.json();

    document.getElementById("result").innerText = data.message;
}


// Upload PDF
async function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");

    if (fileInput.files.length === 0) {
        alert("Please select a PDF file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        document.getElementById("result").innerText = data.message;

        // Refresh document list after upload
        loadDocuments();

    } catch (error) {
        console.error(error);
        document.getElementById("result").innerText =
            "Error uploading PDF.";
    }
}


// Load saved documents
async function loadDocuments() {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/documents"
        );

        const data = await response.json();

        console.log("Documents received:", data);

        const select = document.getElementById("documentSelect");

        select.innerHTML =
            '<option value="">Select a document</option>';

        data.documents.forEach(doc => {
            const option = document.createElement("option");

            option.value = doc.id;
            option.textContent = doc.filename;

            select.appendChild(option);
        });

    } catch (error) {
        console.error("Error loading documents:", error);

        document.getElementById("result").innerText =
            "Could not load documents.";
    }
}

window.onload = function () {
    loadDocuments();
};


// Ask Question
async function askQuestion() {
    const question =
        document.getElementById("question").value;

    const documentId =
        document.getElementById("documentSelect").value;

    if (!documentId) {
        alert("Please select a document.");
        return;
    }

    if (!question.trim()) {
        alert("Please enter a question.");
        return;
    }

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/ask",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    document_id: Number(documentId),
                    question: question
                })
            }
        );

        const data = await response.json();

        console.log(data);

        document.getElementById("result").innerText =
            data.answer;

    } catch (error) {
        console.error(error);
        document.getElementById("result").innerText =
            "Error asking question.";
    }
}


// ==========================================
// Check Backend Connection
// ==========================================

async function getMessage() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/"
        );

        if (!response.ok) {

            throw new Error(
                "Backend connection failed"
            );
        }

        const data = await response.json();

        document.getElementById(
            "result"
        ).innerText = data.message;

    } catch (error) {

        console.error(error);

        document.getElementById(
            "result"
        ).innerText =
            "Cannot connect to backend.";

    }
}


// ==========================================
// Upload PDF
// ==========================================

async function uploadPDF() {

    const fileInput = document.getElementById("pdfFile");

    if (fileInput.files.length === 0) {
        alert("Please select a PDF file.");
        return;
    }

    const file = fileInput.files[0];

    if (file.type !== "application/pdf") {
        alert("Please select a PDF file only.");
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

        document.getElementById("result").innerText =
            "Uploading PDF...";

        const response = await fetch(
            "http://127.0.0.1:8000/upload",
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error("Upload failed");
        }

        const data = await response.json();

        console.log("Upload response:", data);

        // Get the ID created by the database
        const uploadedDocumentId = String(data.document_id);

        console.log(
            "Uploaded document ID:",
            uploadedDocumentId
        );

        // Reload dropdown
        await loadDocuments();

        // Get dropdown
        const select =
            document.getElementById("documentSelect");

        // Automatically select uploaded document
        select.value = uploadedDocumentId;

        console.log(
            "Dropdown selected ID:",
            select.value
        );

        // Verify
        if (select.value === uploadedDocumentId) {

            document.getElementById("result").innerText =
                `Uploaded and selected: ${data.filename}`;

        } else {

            console.error(
                "Could not select uploaded document"
            );

            console.error(
                "Wanted:",
                uploadedDocumentId
            );

            console.error(
                "Actual:",
                select.value
            );
        }

        // Clear file input
        fileInput.value = "";

    } catch (error) {

        console.error(
            "Upload Error:",
            error
        );

        document.getElementById("result").innerText =
            "Error uploading PDF. Make sure the backend is running.";
    }
}


// ==========================================
// Load Documents
// ==========================================

async function loadDocuments() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/documents"
        );

        if (!response.ok) {
            throw new Error("Could not load documents");
        }

        const data = await response.json();

        console.log(
            "Documents received:",
            data
        );

        const select =
            document.getElementById("documentSelect");

        // Clear dropdown
        select.innerHTML =
            '<option value="">Select a document</option>';

        // Add documents
        data.documents.forEach(function(doc) {

            const option =
                document.createElement("option");

            option.value = String(doc.id);

            option.textContent = doc.filename;

            select.appendChild(option);
        });

        console.log(
            "Dropdown populated successfully."
        );

    } catch (error) {

        console.error(
            "Error loading documents:",
            error
        );

        document.getElementById("result").innerText =
            "Could not load documents.";
    }
}


// ==========================================
// Ask Question
// ==========================================

async function askQuestion() {

    const question =
        document.getElementById(
            "question"
        ).value.trim();


    const documentId =
        document.getElementById(
            "documentSelect"
        ).value;


    console.log(
        "Selected document ID:",
        documentId
    );


    console.log(
        "Question:",
        question
    );


    // ==================================
    // Check document
    // ==================================

    if (!documentId) {

        alert(
            "Please select a document."
        );

        return;
    }


    // ==================================
    // Check question
    // ==================================

    if (!question) {

        alert(
            "Please enter a question."
        );

        return;
    }


    try {

        document.getElementById(
            "result"
        ).innerText =
            "Thinking...";


        const response =
            await fetch(
                "http://127.0.0.1:8000/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        document_id:
                            Number(documentId),

                        question:
                            question

                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                "Question request failed"
            );
        }


        const data =
            await response.json();


        console.log(
            "AI Response:",
            data
        );


        document.getElementById(
            "result"
        ).innerText =
            data.answer ||
            "No answer received.";


    } catch (error) {

        console.error(
            "Question Error:",
            error
        );


        document.getElementById(
            "result"
        ).innerText =
            "Error asking question.";

    }
}


// ==========================================
// Page Loaded
// ==========================================

window.onload = function () {

    loadDocuments();

};
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

    const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("result").innerText = data.message;
}

// Ask Question
async function askQuestion() {

    const question = document.getElementById("question").value;

    const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: question
        })
    });

    const data = await response.json();

    console.log(data);   // <-- Add this line

    document.getElementById("result").innerText = data.answer;
}
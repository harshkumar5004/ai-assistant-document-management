import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API Key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


def ask_ai(question):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=question
        )

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"
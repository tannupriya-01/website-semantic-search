import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("Gemini_API_Key"))

def generate_summary(page_content):
    prompt = f"""
You are a professional content writer.
Read the webpage carefully.
Extract the important information.

Ignore:
- menus
- navigation
- footer
- advertisements

Generate a concise summary.
Return plain text only.
Website Content:

{page_content}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text
import json
import re
import requests
from io import BytesIO
import fitz  # PyMuPDF
import docx
import io

def parse_resume(file_content: bytes) -> dict:
    print("[INFO] Parsing resume...")

    resume_text = extract_text(file_content)
    print("[INFO] Resume text extracted.")

    parsed_data = extract_resume_details_from_model(resume_text)
    print("[INFO] Resume details extracted from Ollama.")

    if not isinstance(parsed_data, dict):
        raise ValueError("Parsed data should be a dictionary")

    return parsed_data

def extract_text(file_content: bytes) -> str:
    print("[INFO] Detecting file format...")
    if file_content.startswith(b"%PDF"):
        print("[INFO] PDF format detected.")
        return extract_text_from_pdf(file_content)
    elif file_content[:4] == b'PK\x03\x04':
        print("[INFO] DOCX format detected.")
        return extract_text_from_docx(file_content)
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")

def extract_text_from_pdf(content: bytes) -> str:
    print("[INFO] Extracting text from PDF...")
    text = ""
    with fitz.open(stream=content, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(content: bytes) -> str:
    doc = docx.Document(io.BytesIO(content))
    return "\n".join([para.text for para in doc.paragraphs])


def extract_resume_details_from_model(resume_text: str) -> dict:
    print("[INFO] Sending resume text to Ollama model...")

    url = "http://localhost:11434/api/generate"
    prompt = f"""
You are an intelligent resume parser. Your task is to extract key information from resumes in plain text format and output it as structured JSON. Carefully analyze the text and identify the following fields:

- `name`: Full name of the candidate
- `email`: Valid email address
- `phone`: Valid phone number
- `skills`: List of technical and soft skills
- `education`: List of education entries, each with `degree`, `institution`, and `years`
**experience** (list of objects): For each job or role listed in the resume, extract:
   - `title`: Job title
   - `company`: Company name
   - `start_date`: month and year if available
   - `end_date`: end date if available
   - `duration`: calculate time between start and end if both present
   - `description`: A brief description of work done, responsibilities, tools used, or achievements

- `projects`: List of projects, each with `name`, and `description`
- `certifications`: List of certifications, each with `name` and `year`
- `summary`: A short professional summary, if present
“Skills may appear at the end of the resume. Please ensure to read through the entire content, especially the last few sections or pages, to extract all relevant skills accurately.”

Please identify sections like 'Skills', 'Education', 'Certifications', 'Projects'—even if they appear out of order or are at the end of the document. Carefully extract skills from sections like 'Key Skills', 'Technical Proficiencies', or 'Tools', even if they're at the bottom of the resume.

📌 Output the result as a clean and complete JSON object.  
📌 If a field is missing in the resume, output a reasonable default like an empty string or empty list.  
📌 Be resilient to formatting issues, typos, and mixed structures.

Resume Text:
{resume_text}

Only return raw JSON. No markdown, no comments, no explanations.
"""

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()

        if not response.content:
            raise RuntimeError("API returned empty response")

        result = response.json()
        response_text = result.get("response", "")
        print("[DEBUG] Raw response from model:\n", response_text)

        if not response_text.strip():
            raise RuntimeError("Model returned an empty string")

        # Try to find the first valid JSON using a sliding window
        for i in range(len(response_text)):
            if response_text[i] == '{':
                for j in range(len(response_text), i, -1):
                    if response_text[j - 1] == '}':
                        try:
                            json_str = response_text[i:j]
                            parsed_json = json.loads(json_str)
                            print("[INFO] JSON parsed successfully.")
                            return parsed_json
                        except json.JSONDecodeError:
                            continue

        raise ValueError("No valid JSON found in model response")

    except requests.exceptions.RequestException as e:
        print("[ERROR] RequestException:", str(e))
        raise RuntimeError(f"API error: {str(e)}")
    except ValueError as e:
        print("[ERROR] ValueError:", str(e))
        raise RuntimeError(f"ValueError: {str(e)}")
    except Exception as e:
        print("[ERROR] Unexpected exception:", str(e))
        raise RuntimeError(f"Unexpected error: {str(e)}")

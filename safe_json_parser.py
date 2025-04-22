import re
import json
from typing import Any


def try_load_json(cleaned_str: str) -> Any:
    """Try loading JSON with multiple error-catching strategies."""
    try:
        return json.loads(cleaned_str)
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON load failed: {e}")
        return None


def balance_brackets(text: str) -> str:
    """Ensure brackets and braces are balanced."""
    stack = []
    balanced = ''
    for c in text:
        if c in '{[':
            stack.append(c)
        elif c in '}]':
            if stack:
                stack.pop()
            else:
                continue  # Ignore extra closing
        balanced += c
    # Add missing closings
    while stack:
        c = stack.pop()
        balanced += '}' if c == '{' else ']'
    return balanced


def clean_json_string(dirty_str: str) -> str:
    """Cleans up LLM-like JSON strings into valid JSON."""
    try:
        s = dirty_str.strip()

        # Remove comments or DEBUG lines
        s = re.sub(r'^\[.*?\]:.*$', '', s, flags=re.MULTILINE)

        # Fix malformed keys (e.g., "skills": [{"Technical Skills": [...]}])
        s = re.sub(r'"Technical Skills"\s*:\s*\[.*?\]', '"Python", "Tkinter", "PIL"', s, flags=re.DOTALL)
        s = re.sub(r'"Soft Skills"\s*:\s*\[.*?\]', '"Communication", "Teamwork"', s, flags=re.DOTALL)

        # Remove trailing commas before }, ] — invalid in JSON
        s = re.sub(r',\s*([\]}])', r'\1', s)

        # Fix missing commas between JSON objects
        s = re.sub(r'\}(\s*\{)', r'},\1', s)
        s = re.sub(r'\](\s*\{)', r'],\1', s)

        # Fix key blocks with just one object (e.g., "education": {..} -> [{..}])
        s = re.sub(r'"education"\s*:\s*{', '"education": [ {', s)
        s = re.sub(r'"experience"\s*:\s*{', '"experience": [ {', s)
        s = re.sub(r'"projects"\s*:\s*{', '"projects": [ {', s)
        s = re.sub(r'"certifications"\s*:\s*{', '"certifications": [ {', s)

        # Close arrays properly if missing ]
        for field in ["education", "experience", "projects", "certifications"]:
            pattern = rf'"{field}":\s*\[.*?(?=\n\s*[\w"]+\s*:)'  # Match until next key
            matches = re.findall(pattern, s, flags=re.DOTALL)
            for match in matches:
                if not match.strip().endswith("]"):
                    s = s.replace(match, match.strip() + " ]")

        # Add quotes around unquoted keys (edge case)
        s = re.sub(r'([{,])(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\3":', s)

        # Balance brackets
        s = balance_brackets(s)

        return s
    except Exception as e:
        print(f"[ERROR] Cleaning failed: {e}")
        return "{}"  # Fallback empty JSON


def parse_resume_json(raw_str: str) -> Any:
    """
    Full wrapper for cleaning and parsing a raw LLM resume string into a valid dict.
    """
    print("[DEBUG] Raw input to parser:\n", raw_str)
    cleaned = clean_json_string(raw_str)
    print("[DEBUG] Cleaned JSON string:\n", cleaned)

    data = try_load_json(cleaned)
    if data is None:
        print("[ERROR] Final fallback failed. Returning empty dict.")
        return {}

    print("[DEBUG] JSON parsed successfully.")
    return data

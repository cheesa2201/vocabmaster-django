import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def translate_word(word: str):
    prompt = f"""
Explain the English word: "{word}"

Return ONLY valid JSON in this format:

{{
  "word": "{word}",
  "ipa": "",
  "type": "",
  "meaning_en": "",
  "meaning_vi": "",
  "examples": [
    "",
    ""
  ]
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

      
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        data = json.loads(text)

        return data

    except Exception as e:
        print(f"Gemini error: {e}")

        return {
            "error": str(e),
            "word": word
        }
        
def generate_sentences(word: str):

    prompt = f"""
Create 3 example sentences using the word "{word}".

Return JSON:

{{
 "sentences": []
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        return {"error": str(e)}
    
def generate_flashcard(word: str):


    prompt = f"""
Create a flashcard for the English word "{word}".

Return ONLY JSON:

{{
 "front": "",
 "back": ""
}}

Front should contain the word.
Back should contain:
- IPA
- Vietnamese meaning
- one example sentence
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        return {"error": str(e)}
    
def generate_quiz(word: str):

    prompt = f"""
Create a multiple choice quiz for the word "{word}".

Return ONLY JSON:

{{
 "question": "",
 "options": ["", "", "", ""],
 "answer": ""
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        return {"error": str(e)}
    

def dictionary_lookup(word: str, lang: str):

    prompt = f"""
Explain the word "{word}" in language "{lang}".

Return ONLY JSON:

{{
 "word": "",
 "language": "{lang}",
 "ipa": "",
 "meaning_en": "",
 "meaning_vi": "",
 "examples": []
}}

Rules:
- give pronunciation if available
- give 2 example sentences
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        return {"error": str(e)}
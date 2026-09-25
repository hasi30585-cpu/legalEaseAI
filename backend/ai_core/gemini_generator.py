import os
from typing import List

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv(override=True)


class GeminiDocumentGenerator:
    """
    Generates legal document drafts using Google's Gemini API.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash"
        )

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Please add it to your .env file."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    def _build_prompt(
        self,
        document_type: str,
        parties: str,
        terms: List[str],
        effective_date: str
    ) -> str:

        terms_text = "\n".join(
            f"- {term}" for term in terms if term.strip()
        )

        prompt = f"""
You are a professional legal-document drafting assistant.

Your task is to create a structured FIRST-DRAFT legal document
based strictly on the information supplied by the user.

IMPORTANT:
- This is a drafting assistant, not a substitute for a lawyer.
- Do not invent names, dates, amounts, addresses, obligations,
  or facts that were not supplied.
- If important information is missing, use a clearly marked
  placeholder such as [TO BE PROVIDED].
- Use clear professional legal language.
- Make the document easy to edit.
- Include appropriate headings and numbered sections.
- Do not include markdown code fences.
- Do not include explanations before or after the document.
- Return only the document itself.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{effective_date}

USER-PROVIDED TERMS:
{terms_text}

Create a complete legal document draft with the following general
structure where appropriate:

TITLE

PARTIES

EFFECTIVE DATE

RECITALS / BACKGROUND

DEFINITIONS

MAIN TERMS AND CONDITIONS

OBLIGATIONS OF THE PARTIES

PAYMENT / COMPENSATION, if applicable

CONFIDENTIALITY, if applicable

INTELLECTUAL PROPERTY, if applicable

TERM AND TERMINATION, if applicable

REPRESENTATIONS AND WARRANTIES, if applicable

LIMITATION OF LIABILITY, if applicable

DISPUTE RESOLUTION, if applicable

GOVERNING LAW, if applicable

GENERAL PROVISIONS

SIGNATURES

Use only sections relevant to the selected document type.
"""

        return prompt.strip()

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: List[str],
        effective_date: str
    ) -> str:

        prompt = self._build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=8000,
            )
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text.strip()
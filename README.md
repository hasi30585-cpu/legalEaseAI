# LegalEase

LegalEase is an AI-powered legal document drafting application.

## Architecture

Frontend:
- Streamlit

Backend:
- FastAPI

AI:
- Google Gemini

Document generation:
- TXT
- DOCX
- PDF

## Project Structure

```text
LegalEase/
├── backend/
│   ├── ai_core/
│   │   └── gemini_generator.py
│   ├── utils/
│   │   └── document_formats.py
│   ├── main.py
│   └── routes.py
├── frontend/
│   └── app.py
├── tests/
│   └── test_api.py
├── assets/
├── requirements.txt
├── .env
└── README.md
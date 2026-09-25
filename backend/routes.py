from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator
)


router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000
    )

    terms: List[str] = Field(
        default_factory=list
    )

    effective_date: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


class DocumentResponse(BaseModel):
    success: bool
    document_type: str
    document_text: str


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    request: DocumentRequest
):

    try:

        generator = GeminiDocumentGenerator()

        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date
        )

        return DocumentResponse(
            success=True,
            document_type=request.document_type,
            document_text=document
        )

    except ValueError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Document generation failed. "
                f"Details: {str(error)}"
            )
        )
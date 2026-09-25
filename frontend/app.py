import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import os
from io import BytesIO

import requests
import streamlit as st
from dotenv import load_dotenv

from backend.utils.document_formats import (
    create_txt,
    create_docx,
    create_pdf
)


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8001"
)


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# -----------------------------
# Custom CSS
# -----------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .preview-box {
        background-color: #111827;
        color: #f9fafb;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #374151;
        min-height: 400px;
        max-height: 700px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-family: Georgia, serif;
        line-height: 1.7;
    }

    .warning-box {
        background-color: #fff7ed;
        border: 1px solid #fdba74;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    AI-Powered Legal Document Generator
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="warning-box">
    <b>Important:</b> LegalEase generates AI-assisted
    document drafts for informational and drafting purposes.
    Review the document carefully and consult a qualified
    legal professional before signing or relying on it.
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("About LegalEase")

    st.write(
        """
        LegalEase helps users create editable drafts
        of common legal documents using Generative AI.
        """
    )

    st.divider()

    st.subheader("Supported examples")

    st.write(
        """
        • Employment Contract

        • NDA

        • Lease Agreement

        • Freelance Agreement

        • Service Agreement

        • Offer Letter

        • General Contract
        """
    )

    st.divider()

    st.caption(
        "AI-assisted drafting tool"
    )


# -----------------------------
# Input section
# -----------------------------

st.header("1. Document Details")


document_type = st.selectbox(
    "Document Type",
    [
        "Employment Contract",
        "Non-Disclosure Agreement (NDA)",
        "Lease Agreement",
        "Freelance Work Contract",
        "Service Agreement",
        "Employment Offer Letter",
        "Partnership Agreement",
        "General Contract",
        "Other"
    ]
)


if document_type == "Other":

    custom_document_type = st.text_input(
        "Enter document type"
    )

    if custom_document_type.strip():
        document_type = custom_document_type


parties = st.text_area(
    "Parties Involved",
    placeholder=(
        "Example:\n"
        "Jane Doe (Service Provider)\n"
        "TechNova Inc. (Client)"
    ),
    height=120
)


effective_date = st.text_input(
    "Effective Date",
    placeholder="Example: September 23, 2026"
)


terms_input = st.text_area(
    "Terms & Conditions",
    placeholder=(
        "Enter each term separated by a semicolon (;)\n\n"
        "Example:\n"
        "Payment within 30 days; "
        "Confidentiality must be maintained; "
        "Either party may terminate with 15 days notice"
    ),
    height=160
)


terms = [
    term.strip()
    for term in terms_input.split(";")
    if term.strip()
]


# -----------------------------
# Generate button
# -----------------------------

st.divider()

generate_button = st.button(
    "✨ Generate Document",
    type="primary",
    use_container_width=True
)


if generate_button:

    if not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

        st.stop()

    if not effective_date.strip():

        st.error(
            "Please enter the effective date."
        )

        st.stop()

    if not terms:

        st.warning(
            "No terms were entered. "
            "The AI will use only the supplied party "
            "and document information."
        )

    request_data = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "effective_date": effective_date
    }

    with st.spinner(
        "Generating your legal document..."
    ):

        try:

            response = requests.post(
                f"{BACKEND_URL}/generate",
                json=request_data,
                timeout=180
            )

            if response.status_code != 200:

                try:
                    error_detail = response.json().get(
                        "detail",
                        "Unknown backend error."
                    )
                except Exception:
                    error_detail = response.text

                st.error(
                    f"Generation failed: {error_detail}"
                )

                st.stop()

            result = response.json()

            st.session_state[
                "document_text"
            ] = result["document_text"]

            st.session_state[
                "document_type"
            ] = document_type

            st.session_state[
                "parties"
            ] = parties

            st.session_state[
                "effective_date"
            ] = effective_date

            st.session_state[
                "terms"
            ] = terms

            st.success(
                "Document generated successfully."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the FastAPI backend. "
                "Make sure the backend is running on "
                f"{BACKEND_URL}."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request timed out. "
                "Please try again."
            )

        except Exception as error:

            st.error(
                f"Unexpected error: {str(error)}"
            )


# -----------------------------
# Document preview
# -----------------------------

if "document_text" in st.session_state:

    st.divider()

    st.header("2. Document Preview & Editing")

    edited_document = st.text_area(
        "Edit your document below",
        value=st.session_state["document_text"],
        height=600,
        key="editable_document"
    )


    # Save edited content in session
    st.session_state[
        "document_text"
    ] = edited_document


    # HTML-style preview
    st.subheader("Preview")

    preview_text = (
        st.session_state["document_text"]
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    st.markdown(
        f"""
        <div class="preview-box">
        {preview_text}
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------
    # Download section
    # -----------------------------

    st.divider()

    st.header("3. Download Document")

    document_type_for_file = (
        st.session_state.get(
            "document_type",
            "legal_document"
        )
    )

    safe_name = (
        document_type_for_file
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "_")
    )

    col1, col2, col3 = st.columns(3)


    # TXT
    with col1:

        txt_data = create_txt(
            st.session_state["document_text"]
        )

        st.download_button(
            label="⬇️ Download TXT",
            data=txt_data,
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True
        )


    # DOCX
    with col2:

        docx_data = create_docx(
            text=st.session_state["document_text"],
            document_type=document_type_for_file,
            parties=st.session_state.get(
                "parties",
                ""
            ),
            effective_date=st.session_state.get(
                "effective_date",
                ""
            ),
            terms=";".join(
                st.session_state.get(
                    "terms",
                    []
                )
            )
        )

        st.download_button(
            label="⬇️ Download DOCX",
            data=docx_data,
            file_name=f"{safe_name}.docx",
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml.document"
            ),
            use_container_width=True
        )


    # PDF
    with col3:

        pdf_data = create_pdf(
            text=st.session_state["document_text"],
            document_type=document_type_for_file
        )

        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_data,
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True
        )


    # -----------------------------
    # Reset
    # -----------------------------

    st.divider()

    if st.button(
        "🔄 Start New Document",
        use_container_width=True
    ):

        keys_to_remove = [
            "document_text",
            "document_type",
            "parties",
            "effective_date",
            "terms",
            "editable_document"
        ]

        for key in keys_to_remove:

            if key in st.session_state:
                del st.session_state[key]

        st.rerun()
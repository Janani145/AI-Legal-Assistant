# backend/file_reader.py

import pdfplumber
from docx import Document


def read_txt(file):
    try:
        return file.read().decode("utf-8")
    except Exception:
        raise ValueError("Unable to read TXT file")


def read_docx(file):
    try:
        doc = Document(file)
        paragraphs = [p.text.rstrip() for p in doc.paragraphs]
        return "\n".join(paragraphs)
    except Exception:
        raise ValueError("Unable to read DOCX file")


def read_pdf(file):
    try:
        extracted_text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text(
                    layout=True,
                    x_tolerance=2,
                    y_tolerance=2
                )
                if text:
                    extracted_text += text + "\n"

        if not extracted_text.strip():
            raise ValueError

        return extracted_text

    except Exception:
        raise ValueError(
            "PDF is scanned or protected. Only text-based PDFs are supported."
        )


def normalize_text(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines)


def extract_text(uploaded_file):
    filename = uploaded_file.name.lower()

    if filename.endswith(".txt"):
        raw_text = read_txt(uploaded_file)

    elif filename.endswith(".docx"):
        raw_text = read_docx(uploaded_file)

    elif filename.endswith(".pdf"):
        raw_text = read_pdf(uploaded_file)

    else:
        raise ValueError(
            "Unsupported file format. Please upload PDF, DOCX, or TXT."
        )

    return normalize_text(raw_text)

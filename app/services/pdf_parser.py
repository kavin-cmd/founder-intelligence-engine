import fitz  # PyMuPDF
from typing import List


def parse_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a PDF file (pitch deck)

    Args:
        file_bytes (bytes): Raw PDF file

    Returns:
        str: Extracted text
    """

    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")

        text_chunks: List[str] = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # Extract text
            text = page.get_text("text")

            if text:
                text_chunks.append(text)

        doc.close()

        full_text = "\n".join(text_chunks)

        return full_text.strip()

    except Exception as e:
        raise Exception(f"PDF parsing failed: {str(e)}")
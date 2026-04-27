import re
from typing import List


def clean_text(text: str) -> str:
    """
    Cleans raw extracted text from PDFs/web

    Steps:
    - Lowercasing
    - Remove special characters
    - Remove excessive whitespace
    - Normalize text

    Args:
        text (str): Raw input text

    Returns:
        str: Cleaned text
    """

    try:
        # -------------------------------
        # 1. Lowercase
        # -------------------------------
        text = text.lower()

        # -------------------------------
        # 2. Remove URLs
        # -------------------------------
        text = re.sub(r"http\S+|www\S+|https\S+", "", text)

        # -------------------------------
        # 3. Remove special characters
        # -------------------------------
        text = re.sub(r"[^a-z0-9\s]", " ", text)

        # -------------------------------
        # 4. Remove numbers (optional)
        # Keep if you later want revenue signals
        # -------------------------------
        # text = re.sub(r"\d+", "", text)

        # -------------------------------
        # 5. Normalize whitespace
        # -------------------------------
        text = re.sub(r"\s+", " ", text).strip()

        return text

    except Exception as e:
        raise Exception(f"Text cleaning failed: {str(e)}")
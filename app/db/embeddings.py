from openai import OpenAI
import os
from typing import List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for given text

    Args:
        text (str): Input text

    Returns:
        List[float]: Embedding vector
    """

    try:
        # Clean input (avoid empty / huge strings)
        text = text.strip()

        if not text:
            return [0.0] * 1536  # fallback vector

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        embedding = response.data[0].embedding

        return embedding

    except Exception as e:
        raise Exception(f"Embedding generation failed: {str(e)}")
import faiss
import numpy as np
from typing import List, Dict


class VectorStore:
    def __init__(self, dim: int = 1536):
        """
        Initialize FAISS index
        """
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.texts: List[str] = []

    def add(self, texts: List[str], embeddings: List[List[float]]):
        """
        Add texts and their embeddings to the index
        """
        if not texts or not embeddings:
            return

        vectors = np.array(embeddings).astype("float32")

        self.index.add(vectors)
        self.texts.extend(texts)

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
        """
        Search for similar vectors

        Returns:
            List of top_k results with text + score
        """
        if self.index.ntotal == 0:
            return []

        query_vector = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_vector, top_k)

        results = []

        for i, idx in enumerate(indices[0]):
            if idx < len(self.texts):
                results.append({
                    "text": self.texts[idx],
                    "score": float(distances[0][i])
                })

        return results
from typing import Dict
import re


def extract_features(text: str) -> Dict[str, float]:
    """
    Converts cleaned text into structured numerical features for ML model

    Args:
        text (str): Cleaned startup text

    Returns:
        Dict[str, float]: Feature dictionary
    """

    try:
        features = {}

        # -------------------------------
        # 1. BASIC LENGTH FEATURES
        # -------------------------------
        features["text_length"] = len(text)
        features["word_count"] = len(text.split())

        # -------------------------------
        # 2. KEYWORD SIGNALS (binary / counts)
        # -------------------------------
        keywords = {
            "ai": ["ai", "artificial intelligence", "machine learning"],
            "saas": ["saas", "software as a service"],
            "marketplace": ["marketplace", "platform"],
            "fintech": ["fintech", "payments", "banking", "crypto"],
            "growth": ["growth", "scaling", "users", "traction"],
            "revenue": ["revenue", "arr", "mrr", "profit"],
        }

        for key, words in keywords.items():
            features[f"{key}_signal"] = sum(
                1 for w in words if w in text
            )

        # -------------------------------
        # 3. TRACTION SIGNALS
        # -------------------------------
        traction_patterns = [
            r"\b\d+\s?users\b",
            r"\b\d+\s?customers\b",
            r"\b\d+\s?mrr\b",
            r"\b\d+\s?arr\b",
            r"\b\d+\s?growth\b",
        ]

        traction_score = 0
        for pattern in traction_patterns:
            matches = re.findall(pattern, text)
            traction_score += len(matches)

        features["traction_score"] = traction_score

        # -------------------------------
        # 4. TEAM / FOUNDER SIGNALS
        # -------------------------------
        founder_keywords = ["founder", "team", "experience", "ex-google", "ex-meta"]

        features["team_strength_signal"] = sum(
            1 for word in founder_keywords if word in text
        )

        # -------------------------------
        # 5. MARKET SIGNAL
        # -------------------------------
        market_keywords = ["market", "opportunity", "industry", "billion", "tam"]

        features["market_signal"] = sum(
            1 for word in market_keywords if word in text
        )

        # -------------------------------
        # 6. RISK SIGNAL (inverse)
        # -------------------------------
        risk_keywords = ["idea stage", "pre-revenue", "prototype", "beta"]

        features["risk_signal"] = sum(
            1 for word in risk_keywords if word in text
        )

        return features

    except Exception as e:
        raise Exception(f"Feature engineering failed: {str(e)}")
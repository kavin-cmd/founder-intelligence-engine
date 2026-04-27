import os
import joblib
import numpy as np
from typing import Dict

MODEL_PATH = "app/models/xgboost_model.pkl"

# Global model cache
_model = None


def load_model():
    """
    Loads the trained ML model from disk
    """
    global _model

    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        else:
            _model = None  # fallback mode

    return _model


def predict_success(features: Dict[str, float]) -> float:
    """
    Predict startup success probability

    Args:
        features (dict): Engineered features

    Returns:
        float: Success probability (0–100)
    """

    try:
        model = load_model()

        # Convert feature dict → ordered array
        feature_values = np.array(list(features.values())).reshape(1, -1)

        # -------------------------------
        # If model exists → real prediction
        # -------------------------------
        if model:
            prob = model.predict_proba(feature_values)[0][1]
            return round(prob * 100, 2)

        # -------------------------------
        # Fallback (important for dev/demo)
        # -------------------------------
        else:
            # Simple heuristic scoring
            score = 50

            score += features.get("traction_score", 0) * 5
            score += features.get("revenue_signal", 0) * 4
            score += features.get("team_strength_signal", 0) * 3
            score += features.get("market_signal", 0) * 2
            score -= features.get("risk_signal", 0) * 5

            # Clamp between 0–100
            score = max(0, min(100, score))

            return round(score, 2)

    except Exception as e:
        raise Exception(f"Prediction failed: {str(e)}")
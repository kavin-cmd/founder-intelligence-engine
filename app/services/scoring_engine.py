from typing import Dict, Any


def compute_final_score(ml_score: float, llm_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Combines ML prediction + LLM insights into final report

    Args:
        ml_score (float): ML-based success probability (0–100)
        llm_output (dict): LLM analysis output

    Returns:
        dict: Final structured report
    """

    try:
        # -------------------------------
        # 1. Extract LLM fields safely
        # -------------------------------
        founder_strength = llm_output.get("founder_strength", 50)
        market_clarity = llm_output.get("market_clarity", 50)
        execution_risk = llm_output.get("execution_risk", "Medium")

        strengths = llm_output.get("strengths", [])
        weaknesses = llm_output.get("weaknesses", [])
        insights = llm_output.get("insights", "")

        # -------------------------------
        # 2. Normalize risk → numeric penalty
        # -------------------------------
        risk_penalty_map = {
            "Low": 0,
            "Medium": 5,
            "High": 10
        }

        risk_penalty = risk_penalty_map.get(execution_risk, 5)

        # -------------------------------
        # 3. Hybrid score calculation
        # -------------------------------
        hybrid_score = (
            0.5 * ml_score +
            0.2 * founder_strength +
            0.2 * market_clarity -
            risk_penalty
        )

        # Clamp between 0–100
        hybrid_score = max(0, min(100, hybrid_score))

        # -------------------------------
        # 4. Risk label refinement
        # -------------------------------
        if hybrid_score >= 75:
            final_risk = "Low"
        elif hybrid_score >= 50:
            final_risk = "Medium"
        else:
            final_risk = "High"

        # -------------------------------
        # 5. Final output
        # -------------------------------
        return {
            "startup_score": round(hybrid_score, 2),
            "ml_score": ml_score,
            "founder_strength": founder_strength,
            "market_clarity": market_clarity,
            "risk_level": final_risk,
            "execution_risk": execution_risk,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "insights": insights
        }

    except Exception as e:
        raise Exception(f"Scoring failed: {str(e)}")
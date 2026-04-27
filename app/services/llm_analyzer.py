from openai import OpenAI
import os
from typing import Dict

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_with_llm(text: str) -> Dict:
    """
    Uses LLM to analyze startup qualitatively

    Args:
        text (str): Cleaned startup text

    Returns:
        Dict: Structured analysis
    """

    try:
        prompt = f"""
You are a top-tier venture capitalist.

Analyze the following startup and return a structured evaluation.

Startup Description:
{text[:4000]}

Return JSON with:
- founder_strength (0-100)
- market_clarity (0-100)
- execution_risk (Low/Medium/High)
- strengths (list)
- weaknesses (list)
- insights (short paragraph)
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a sharp VC analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content

        # ⚠️ naive parsing (we'll improve later)
        return {
            "raw_output": content
        }

    except Exception as e:
        raise Exception(f"LLM analysis failed: {str(e)}")
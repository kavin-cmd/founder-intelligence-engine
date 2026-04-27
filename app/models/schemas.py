from pydantic import BaseModel, Field
from typing import List, Optional


class AnalysisResponse(BaseModel):
    """
    Final output schema for startup analysis
    """

    startup_score: float = Field(..., ge=0, le=100)
    ml_score: float = Field(..., ge=0, le=100)

    founder_strength: float = Field(..., ge=0, le=100)
    market_clarity: float = Field(..., ge=0, le=100)

    risk_level: str
    execution_risk: str

    strengths: List[str]
    weaknesses: List[str]

    insights: str


class ErrorResponse(BaseModel):
    """
    Standard error response
    """

    status: str = "error"
    message: str


class AnalyzeAPIResponse(BaseModel):
    """
    Wrapper response for API
    """

    status: str = "success"
    data: Optional[AnalysisResponse]
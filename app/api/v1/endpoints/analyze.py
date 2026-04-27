from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any

from app.services.pdf_parser import parse_pdf
from app.services.text_cleaner import clean_text
from app.services.feature_engineering import extract_features
from app.services.llm_analyzer import analyze_with_llm
from app.services.scoring_engine import compute_final_score
from app.models.ml_model import predict_success

router = APIRouter()


@router.post("/")
async def analyze_startup(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Core endpoint:
    Takes pitch deck → returns startup intelligence report
    """

    try:
        # -------------------------------
        # 1. READ FILE
        # -------------------------------
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files supported")

        contents = await file.read()

        # -------------------------------
        # 2. PARSE PDF
        # -------------------------------
        raw_text = parse_pdf(contents)

        if not raw_text or len(raw_text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Empty or invalid PDF")

        # -------------------------------
        # 3. CLEAN TEXT
        # -------------------------------
        cleaned_text = clean_text(raw_text)

        # -------------------------------
        # 4. FEATURE ENGINEERING (ML)
        # -------------------------------
        features = extract_features(cleaned_text)

        # -------------------------------
        # 5. ML PREDICTION
        # -------------------------------
        ml_score = predict_success(features)

        # -------------------------------
        # 6. LLM ANALYSIS (QUALITATIVE)
        # -------------------------------
        llm_output = analyze_with_llm(cleaned_text)

        # -------------------------------
        # 7. HYBRID SCORING
        # -------------------------------
        final_report = compute_final_score(
            ml_score=ml_score,
            llm_output=llm_output
        )

        return {
            "status": "success",
            "data": final_report
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )
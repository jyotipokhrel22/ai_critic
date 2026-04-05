# app/api/v1/endpoints.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.schemas import StatementRequest, CritiqueResponse
from app.core.critique_engine import critique  # your unified engine

router = APIRouter()  # <-- this must exist

# POST endpoint
@router.post("/submit_statement", response_model=CritiqueResponse)
def submit_statement(data: StatementRequest):
    # Call the refactored unified critique engine
    feedback = critique(data.statement)

    # Map to CritiqueResponse
    return CritiqueResponse(
        logic_issues=[i for i in feedback["issues"] if i["category"] == "Logic"],
        philosophical_insights=[i for i in feedback["issues"] if i["category"] == "Philosophy"],
        argument_strength=feedback["strength"],
        missing_evidence=feedback["evidence"]["details"] if feedback["evidence"]["score"] < 0.6 else [],
        reflection_prompts=feedback["reflection_prompts"]
    )
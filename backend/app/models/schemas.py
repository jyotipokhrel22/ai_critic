from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class StatementRequest(BaseModel):
    statement: str = Field(..., min_length=5, max_length=1000, description="The statement to analyze")

class CritiqueResponse(BaseModel):
    logic_issues: List[Dict[str, Any]] = Field(default_factory=list, description="Logical fallacies detected")
    philosophical_insights: List[Dict[str, Any]] = Field(default_factory=list, description="Philosophical observations")
    argument_strength: float = Field(..., description="Overall score 0.1-1.0")
    missing_evidence: List[str] = Field(default_factory=list, description="Suggestions for better evidence")
    reflection_prompts: List[str] = Field(default_factory=list, description="Socratic prompts for the user")
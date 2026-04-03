from pydantic import BaseModel, Field

class AnalysisResponse(BaseModel):
    sector: str = Field(..., description="The sector that was analyzed (e.g. pharmaceuticals)")
    markdown_report: str = Field(..., description="Structured MARKDOWN report from Gemini")

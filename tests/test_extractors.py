from src.intelligence.requirement_extractor import RequirementExtractor
from src.schemas.schemas import RequirementAnalysisRequest


def test_requirement_extractor():
    extractor = RequirementExtractor()
    req = RequirementAnalysisRequest(
        title="FastAPI & PostgreSQL Backend Engineer",
        description="We need an expert in Python, FastAPI, and pgvector to build a high-performance vector search REST API pipeline.",
        budget=3500.0,
    )
    res = extractor.extract(req)
    assert "Fastapi" in res.primary_technologies or "Python" in res.primary_technologies
    assert len(res.deliverables) >= 1
    assert res.budget_adequacy in ("high", "premium")

from src.intelligence.classifier import FreelanceClassifier
from src.intelligence.scorer import OpportunityScorer
from src.schemas.schemas import ClassificationRequest, ClientType, OpportunityScoreRequest


def test_classifier():
    classifier = FreelanceClassifier()
    direct_req = ClassificationRequest(
        title="Python Dev",
        description="We are building a new SaaS product at our startup and need someone to join us.",
    )
    direct_res = classifier.classify(direct_req)
    assert direct_res.is_direct_client is True
    assert direct_res.client_type == ClientType.DIRECT_CLIENT

    agency_req = ClassificationRequest(
        title="Contractor",
        description="We are a staffing agency recruiting on behalf of our client for a C2C position.",
    )
    agency_res = classifier.classify(agency_req)
    assert agency_res.is_direct_client is False


def test_scorer():
    scorer = OpportunityScorer()
    req = OpportunityScoreRequest(
        title="Senior Python & FastAPI Microservice Engineer",
        description="Looking for Python, FastAPI, and Docker engineer with postgres experience.",
        skills=["Python", "FastAPI", "Docker", "PostgreSQL"],
        budget=4000.0,
        source="Hacker News",
    )
    res = scorer.score(req)
    assert res.score.overall_score >= 75.0
    assert res.qualification_verdict in ("QUALIFIED", "HIGH_PRIORITY")
    assert res.score.win_probability >= 0.5

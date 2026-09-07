from fastapi.testclient import TestClient


def test_health_endpoints(client: TestClient):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["service"] == "client-intelligence-svc"


def test_analyze_deep_api(client: TestClient):
    payload = {
        "title": "FastAPI & RAG Pipeline Engineer",
        "description": "Looking for FastAPI + pgvector specialist. Reach out to Alex at alex@ai-startup.io.",
        "skills": ["FastAPI", "Python", "RAG"],
        "budget": 4500.0,
        "source": "Hacker News",
    }
    res = client.post("/api/v1/analyze/project", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "requirements" in data
    assert "client_intel" in data
    assert data["client_intel"]["contact"]["email"] == "alex@ai-startup.io"
    assert data["scoring"]["score"]["overall_score"] >= 75.0


def test_classify_and_strategy_api(client: TestClient):
    class_res = client.post(
        "/api/v1/classify",
        json={"title": "Founder Seeking Dev", "description": "I am the founder of a startup building AI tools."},
    )
    assert class_res.status_code == 200
    assert class_res.json()["is_direct_client"] is True

    strat_res = client.post(
        "/api/v1/strategy",
        json={"title": "Urgent bug fix", "description": "Need urgent fix today ASAP."},
    )
    assert strat_res.status_code == 200
    assert strat_res.json()["recommended_angle"] == "speed_delivery"

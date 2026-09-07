# Client Intelligence Service (`CLIENT-INTELLIGENCE-SVC`)

Cognitive lead enrichment, requirement extraction, multi-factor opportunity scoring, and freelance client classification microservice (Port 8002).

---

## 🚀 Quickstart

### 1. Start Server
```powershell
cd "C:\PRIVATE PROJECTS\CLIENT-INTELLIGENCE-SVC"
python -m src.cli run-server --port 8002
```

- Swagger UI: [http://localhost:8002/docs](http://localhost:8002/docs)
- Health Check: [http://localhost:8002/health](http://localhost:8002/health)

### 2. Analyze Lead from CLI
```powershell
python -m src.cli analyze --title "FastAPI Engineer" --desc "Looking for FastAPI + pgvector. Email me at ceo@startup.io" --budget 3500
```

### 3. Run Tests
```powershell
pytest tests -v --cov=src
```

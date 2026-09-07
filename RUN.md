# How to Run `CLIENT-INTELLIGENCE-SVC`

---

## 1. Start Server
```powershell
cd "C:\PRIVATE PROJECTS\CLIENT-INTELLIGENCE-SVC"
python -m src.cli run-server --port 8002
```

## 2. CLI Analysis Command
```powershell
python -m src.cli analyze --title "Python LLM Developer" --desc "We at Acme AI are building a RAG search engine. Contact CTO Alex at alex@acme.ai" --budget 4000
```

## 3. Run Tests
```powershell
pytest tests -v --cov=src
```

from src.intelligence.client_enricher import ClientEnricher
from src.schemas.schemas import ClientEnrichmentRequest, ClientType


def test_client_enricher():
    enricher = ClientEnricher()
    req = ClientEnrichmentRequest(
        title="AI Engineer",
        description="Hi, I'm Sarah Connor from Cyberdyne AI (https://cyberdyne.ai). Reach out at sarah@cyberdyne.ai.",
    )
    res = enricher.enrich(req)
    assert res.contact.email == "sarah@cyberdyne.ai"
    assert res.contact.name == "Sarah Connor"
    assert res.contact.company == "Cyberdyne AI"
    assert res.contact.confidence >= 0.8

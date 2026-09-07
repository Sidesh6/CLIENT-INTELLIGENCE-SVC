"""
Client profile and contact enrichment engine.
"""

import re
from urllib.parse import urlparse
from src.schemas.schemas import (
    ClientEnrichmentRequest,
    ClientEnrichmentResponse,
    ClientType,
    ContactDetail,
    EngagementType,
)

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
URL_REGEX = r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)"

FOUNDER_PATTERNS = [
    r"(?:i am|i'm|my name is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
    r"(?:founder|ceo|cto|manager|contact)\s*:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
    r"(?:reach out to|email)\s+([A-Z][a-z]+)\s+at",
]

COMPANY_PATTERNS = [
    r"(?:we at|at|company|team at|from)\s+([A-Z][A-Za-z0-9\s]{2,25}(?:Inc|LLC|Corp|Technologies|Tech|Labs|AI|Studio)?)",
    r"([A-Z][A-Za-z0-9]{2,20}(?:\s+AI|\s+Technologies|\s+Labs)?)\s+is looking for",
]


class ClientEnricher:
    """Enriches raw opportunity text with structured contact details and company signals."""

    def enrich(self, req: ClientEnrichmentRequest) -> ClientEnrichmentResponse:
        text = f"{req.title}\n{req.description}"
        source_evidence: list[str] = []

        # 1. Extract Email
        email = None
        email_match = re.search(EMAIL_REGEX, text)
        if email_match:
            candidate_email = email_match.group(0).lower().strip(".")
            # Filter obvious false positives like example.com or image filenames
            if not candidate_email.endswith((".png", ".jpg", ".svg", "example.com")):
                email = candidate_email
                source_evidence.append(f"Direct email found: {email}")

        # 2. Extract Website & Domain
        website = None
        domain = None
        url_matches = re.findall(URL_REGEX, text)
        for u in url_matches:
            if not any(ign in u for ign in ["github.com", "ycombinator.com", "upwork.com", "reddit.com", "twitter.com"]):
                website = u
                parsed = urlparse(u)
                domain = parsed.netloc.replace("www.", "")
                source_evidence.append(f"Company website identified: {website}")
                break

        if not website and req.source_url:
            parsed = urlparse(req.source_url)
            if not any(ign in req.source_url for ign in ["ycombinator.com", "upwork.com", "reddit.com"]):
                website = req.source_url
                domain = parsed.netloc.replace("www.", "")

        # 3. Extract Decision Maker Name
        name = None
        for pattern in FOUNDER_PATTERNS:
            name_match = re.search(pattern, text, re.IGNORECASE)
            if name_match:
                extracted_name = name_match.group(1).strip()
                if len(extracted_name) > 2 and len(extracted_name) < 30:
                    name = extracted_name
                    source_evidence.append(f"Decision maker name matched: {name}")
                    break

        # 4. Extract Company Name
        company = None
        for pattern in COMPANY_PATTERNS:
            comp_match = re.search(pattern, text)
            if comp_match:
                extracted_comp = comp_match.group(1).strip()
                if len(extracted_comp) > 2 and len(extracted_comp) < 35:
                    company = extracted_comp
                    source_evidence.append(f"Company name identified: {company}")
                    break

        if not company and domain:
            company = domain.split(".")[0].capitalize()

        # 5. Compute Confidence Score
        confidence = 0.4
        if email:
            confidence += 0.35
        if name:
            confidence += 0.15
        if website or domain:
            confidence += 0.10
        confidence = min(1.0, confidence)

        # 6. Engagement Type
        lower_text = text.lower()
        if "retainer" in lower_text or "monthly" in lower_text or "part-time" in lower_text:
            engagement_type = EngagementType.RETAINER
        elif "hourly" in lower_text or "$/hr" in lower_text or "/hour" in lower_text:
            engagement_type = EngagementType.HOURLY
        elif "full-time" in lower_text or "permanent" in lower_text or "salary" in lower_text:
            engagement_type = EngagementType.FULL_TIME
        else:
            engagement_type = EngagementType.FIXED_PRICE

        # 7. Client Type
        if "recruiter" in lower_text or "staffing" in lower_text or "c2c" in lower_text:
            client_type = ClientType.RECRUITER
        elif "agency" in lower_text or "client of ours" in lower_text:
            client_type = ClientType.AGENCY
        else:
            client_type = ClientType.DIRECT_CLIENT

        contact = ContactDetail(
            name=name,
            email=email,
            company=company,
            website=website,
            domain=domain,
            confidence=round(confidence, 2),
            source_evidence=source_evidence,
        )

        return ClientEnrichmentResponse(
            contact=contact,
            client_type=client_type,
            engagement_type=engagement_type,
            industry=None,
            company_size_estimate="Startup (1-50)",
            risk_flags=[],
        )

"""
Classification engine for distinguishing Direct Clients from Recruiters/Agencies.
"""

import re
from src.schemas.schemas import ClassificationRequest, ClassificationResponse, ClientType, EngagementType

AGENCY_PATTERNS = [
    r"\b(staffing|recruiting|recruiter|talent acquisition agency|on behalf of our client)\b",
    r"\b(client of ours|our client is|for one of our clients)\b",
    r"\b(c2c|corp-to-corp|w2 only|third party)\b",
    r"\b(placement fee|headhunting|brokerage)\b",
]

DIRECT_PATTERNS = [
    r"\b(we are building|my startup|our team|we need someone to join us)\b",
    r"\b(i am the founder|i'm the ceo|i'm building|my company)\b",
    r"\b(direct contract|founding engineer|contractor for our product)\b",
]


class FreelanceClassifier:
    """Classifies opportunities into direct clients or brokers."""

    def classify(self, req: ClassificationRequest) -> ClassificationResponse:
        text = f"{req.title}\n{req.description}".lower()

        agency_score = 0
        direct_score = 0

        for pat in AGENCY_PATTERNS:
            if re.search(pat, text):
                agency_score += 1

        for pat in DIRECT_PATTERNS:
            if re.search(pat, text):
                direct_score += 1

        # Source based hints
        if req.source in ("Hacker News", "Direct Email", "Founder Inquiries"):
            direct_score += 2

        if agency_score > direct_score:
            is_direct = False
            client_type = ClientType.RECRUITER if "recruiter" in text or "staffing" in text else ClientType.AGENCY
            confidence = min(0.95, 0.6 + 0.15 * agency_score)
            rationale = "Text contains intermediary staffing or recruiter phrasing ('client of ours' / staffing markers)."
        else:
            is_direct = True
            client_type = ClientType.DIRECT_CLIENT
            confidence = min(0.95, 0.7 + 0.1 * direct_score)
            rationale = "Direct client indicators detected (first-person founder language or verified direct posting)."

        # Engagement type
        if "retainer" in text or "monthly" in text:
            eng = EngagementType.RETAINER
        elif "hourly" in text or "$/hr" in text:
            eng = EngagementType.HOURLY
        elif "full-time" in text or "permanent" in text:
            eng = EngagementType.FULL_TIME
        else:
            eng = EngagementType.FIXED_PRICE

        return ClassificationResponse(
            is_direct_client=is_direct,
            client_type=client_type,
            engagement_type=eng,
            confidence=round(confidence, 2),
            rationale=rationale,
        )

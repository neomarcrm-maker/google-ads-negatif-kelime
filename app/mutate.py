from collections import defaultdict

from google.ads.googleads.errors import GoogleAdsException

from app.ads_client import get_client, _customer_id


def add_negative_keywords(
    customer_id: str, terms: list[dict], validate_only: bool = False
) -> dict:
    """terms: [{"campaign_id": str, "search_term": str}, ...]
    Her terimi kendi kampanyasına EXACT match negatif anahtar kelime olarak ekler.
    """
    client = get_client()
    customer_id = _customer_id(customer_id)
    criterion_service = client.get_service("CampaignCriterionService")
    campaign_service = client.get_service("CampaignService")
    keyword_match_type = client.enums.KeywordMatchTypeEnum.EXACT

    by_campaign = defaultdict(list)
    for t in terms:
        by_campaign[t["campaign_id"]].append(t["search_term"])

    operations = []
    for campaign_id, search_terms in by_campaign.items():
        for term in search_terms:
            operation = client.get_type("CampaignCriterionOperation")
            criterion = operation.create
            criterion.campaign = campaign_service.campaign_path(customer_id, campaign_id)
            criterion.negative = True
            criterion.keyword.text = term
            criterion.keyword.match_type = keyword_match_type
            operations.append(operation)

    if not operations:
        return {"added": 0, "results": []}

    try:
        response = criterion_service.mutate_campaign_criteria(
            customer_id=customer_id,
            operations=operations,
            validate_only=validate_only,
        )
    except GoogleAdsException as ex:
        raise RuntimeError(_format_ads_exception(ex)) from ex

    if validate_only:
        return {"added": 0, "validated": len(operations)}

    return {"added": len(response.results), "results": [r.resource_name for r in response.results]}


def _format_ads_exception(ex: GoogleAdsException) -> str:
    parts = [f"Request ID {ex.request_id} başarısız oldu:"]
    for error in ex.failure.errors:
        parts.append(f"  - {error.message}")
    return "\n".join(parts)

import os
import re
from collections import defaultdict
from functools import lru_cache

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

DATE_RANGE_ENUMS = {
    "LAST_7_DAYS",
    "LAST_14_DAYS",
    "LAST_30_DAYS",
    "THIS_MONTH",
    "LAST_MONTH",
}

_ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@lru_cache(maxsize=1)
def get_client() -> GoogleAdsClient:
    config = {
        "developer_token": os.environ["DEVELOPER_TOKEN"],
        "client_id": os.environ["GOOGLE_ADS_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_ADS_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
        "login_customer_id": os.environ["LOGIN_CUSTOMER_ID"],
        "use_proto_plus": True,
    }
    return GoogleAdsClient.load_from_dict(config)


def _customer_id(raw: str) -> str:
    return raw.replace("-", "").strip()


def list_accounts() -> list[dict]:
    client = get_client()
    mcc_id = _customer_id(os.environ["LOGIN_CUSTOMER_ID"])
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          customer_client.id,
          customer_client.descriptive_name,
          customer_client.manager,
          customer_client.status,
          customer_client.level
        FROM customer_client
    """

    accounts = []
    response = ga_service.search(customer_id=mcc_id, query=query)
    for row in response:
        cc = row.customer_client
        if cc.manager or cc.level == 0:
            continue
        accounts.append(
            {
                "id": str(cc.id),
                "name": cc.descriptive_name or str(cc.id),
                "status": cc.status.name,
            }
        )
    return accounts


def _build_date_filter(date_range: str, start_date: str | None, end_date: str | None) -> str:
    if date_range == "CUSTOM":
        if not start_date or not end_date:
            raise ValueError("Özel aralık için start_date ve end_date gerekli")
        if not _ISO_DATE_PATTERN.match(start_date) or not _ISO_DATE_PATTERN.match(end_date):
            raise ValueError("Tarihler YYYY-MM-DD formatında olmalı")
        if start_date > end_date:
            raise ValueError("Başlangıç tarihi bitiş tarihinden sonra olamaz")
        return f"segments.date BETWEEN '{start_date}' AND '{end_date}'"

    if date_range not in DATE_RANGE_ENUMS:
        raise ValueError(f"Geçersiz date_range: {date_range}")
    return f"segments.date DURING {date_range}"


def fetch_search_terms(
    customer_id: str,
    date_range: str = "LAST_30_DAYS",
    start_date: str | None = None,
    end_date: str | None = None,
) -> list[dict]:
    date_filter = _build_date_filter(date_range, start_date, end_date)

    client = get_client()
    customer_id = _customer_id(customer_id)
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
          search_term_view.search_term,
          campaign.id,
          campaign.name,
          ad_group.id,
          ad_group.name,
          metrics.impressions,
          metrics.clicks,
          metrics.cost_micros,
          metrics.conversions
        FROM search_term_view
        WHERE {date_filter}
        ORDER BY metrics.clicks DESC
    """

    rows = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            rows.append(
                {
                    "search_term": row.search_term_view.search_term,
                    "campaign_id": str(row.campaign.id),
                    "campaign_name": row.campaign.name,
                    "ad_group_id": str(row.ad_group.id),
                    "ad_group_name": row.ad_group.name,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost": row.metrics.cost_micros / 1_000_000,
                    "conversions": row.metrics.conversions,
                }
            )
    except GoogleAdsException as ex:
        raise RuntimeError(_format_ads_exception(ex)) from ex

    return rows


def fetch_existing_negative_keywords(customer_id: str) -> dict:
    """Hesapta zaten var olan (kampanya ve ad group seviyesindeki) negatif
    anahtar kelimeleri döner. Aynı terimin tekrar tekrar negatife eklenmeye
    çalışılmasını önlemek için find_candidates sonuçlarını elemekte kullanılır.
    Returns: {"by_campaign": {campaign_id: {text_lower, ...}}, "by_ad_group": {ad_group_id: {text_lower, ...}}}
    """
    client = get_client()
    customer_id = _customer_id(customer_id)
    ga_service = client.get_service("GoogleAdsService")

    by_campaign: dict[str, set] = defaultdict(set)
    campaign_query = """
        SELECT campaign.id, campaign_criterion.keyword.text
        FROM campaign_criterion
        WHERE campaign_criterion.negative = true
          AND campaign_criterion.type = KEYWORD
    """
    try:
        for row in ga_service.search(customer_id=customer_id, query=campaign_query):
            by_campaign[str(row.campaign.id)].add(row.campaign_criterion.keyword.text.lower())
    except GoogleAdsException as ex:
        raise RuntimeError(_format_ads_exception(ex)) from ex

    by_ad_group: dict[str, set] = defaultdict(set)
    ad_group_query = """
        SELECT ad_group.id, ad_group_criterion.keyword.text
        FROM ad_group_criterion
        WHERE ad_group_criterion.negative = true
          AND ad_group_criterion.type = KEYWORD
    """
    try:
        for row in ga_service.search(customer_id=customer_id, query=ad_group_query):
            by_ad_group[str(row.ad_group.id)].add(row.ad_group_criterion.keyword.text.lower())
    except GoogleAdsException as ex:
        raise RuntimeError(_format_ads_exception(ex)) from ex

    return {"by_campaign": by_campaign, "by_ad_group": by_ad_group}


def _format_ads_exception(ex: GoogleAdsException) -> str:
    parts = [f"Request ID {ex.request_id} başarısız oldu:"]
    for error in ex.failure.errors:
        parts.append(f"  - {error.message}")
    return "\n".join(parts)

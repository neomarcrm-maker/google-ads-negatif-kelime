import os
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


def fetch_search_terms(customer_id: str, date_range: str = "LAST_30_DAYS") -> list[dict]:
    if date_range not in DATE_RANGE_ENUMS:
        raise ValueError(f"Geçersiz date_range: {date_range}")

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
        WHERE segments.date DURING {date_range}
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


def _format_ads_exception(ex: GoogleAdsException) -> str:
    parts = [f"Request ID {ex.request_id} başarısız oldu:"]
    for error in ex.failure.errors:
        parts.append(f"  - {error.message}")
    return "\n".join(parts)

import os
import re
import time
from collections import defaultdict
from functools import lru_cache

from google.api_core import exceptions as core_exceptions
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from app.negative_rules import normalize_text

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
    for row in _run_query(ga_service, customer_id, query, label="Arama terimleri sorgusu"):
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

    return rows


_TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}
_MAX_ATTEMPTS = 3


def _is_transient_ads_error(ex: GoogleAdsException) -> bool:
    """Google Ads API'nin INTERNAL_ERROR / geçici hata içeren yanıtları."""
    try:
        return any(
            getattr(e.error_code, "internal_error", 0) or getattr(e.error_code, "quota_error", 0)
            for e in ex.failure.errors
        )
    except Exception:  # noqa: BLE001
        return False


def _run_query(ga_service, customer_id: str, query: str, label: str = "sorgu"):
    """Sorguyu geçici Google sunucu hatalarında (500/503/INTERNAL_ERROR) kısa
    bekleyerek 3 kez dener. Hata mesajı hangi sorgunun düştüğünü içerir.
    Sonuç sayfalar halinde geldiği için liste olarak tamamen okunur.
    """
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        last_try = attempt == _MAX_ATTEMPTS
        try:
            return list(ga_service.search(customer_id=customer_id, query=query))
        except GoogleAdsException as ex:
            if last_try or not _is_transient_ads_error(ex):
                raise RuntimeError(f"{label}: {_format_ads_exception(ex)}") from ex
        except core_exceptions.GoogleAPICallError as ex:
            code = int(getattr(ex, "code", 0) or 0)
            if code not in _TRANSIENT_HTTP_CODES:
                raise RuntimeError(f"{label}: Google Ads hatası ({code}): {str(ex)[:300]}") from ex
            if last_try:
                raise RuntimeError(
                    f"{label}: Google Ads geçici sunucu hatası ({code}), "
                    f"{_MAX_ATTEMPTS} denemeden sonra da düzelmedi. "
                    f"Birkaç dakika sonra tekrar dene. Ayrıntı: {str(ex)[:300]}"
                ) from ex
        time.sleep(1.5 * attempt)


def _neg_entry(text: str, match_type_name: str) -> tuple:
    norm = normalize_text(text)
    return (norm, tuple(norm.split()), match_type_name)


def fetch_existing_negative_keywords(customer_id: str) -> dict:
    """Hesapta zaten var olan negatif anahtar kelimeleri döner; tekrar
    önerilmesini önlemek için kullanılır. Kapsanan kaynaklar:
      - kampanya seviyesi negatifler (by_campaign)
      - ad group seviyesi negatifler (by_ad_group)
      - kampanyalara bağlı paylaşılan negatif listeler (by_shared_set +
        campaign_shared_sets)
      - hesap seviyesi negatifler (account)
    Her kayıt (normalize_metin, kelimeler, eşleme_türü) demetidir.
    Her sorgu geçici hatalarda yeniden denenir. Yine de başarısız olan bir
    sorgu tüm analizi düşürmez: durum "notes" içinde bildirilir ve o kaynaktaki
    negatifler elenemez (özet satırında uyarı olarak görünür).
    """
    client = get_client()
    customer_id = _customer_id(customer_id)
    ga_service = client.get_service("GoogleAdsService")

    notes: list[str] = []

    by_campaign: dict[str, list] = defaultdict(list)
    campaign_names: dict[str, str] = {}
    try:
        for row in _run_query(ga_service, customer_id, """
            SELECT campaign.id, campaign.name,
                   campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
            FROM campaign_criterion
            WHERE campaign_criterion.negative = true
              AND campaign_criterion.type = KEYWORD
        """, label="Kampanya negatifleri sorgusu"):
            cid = str(row.campaign.id)
            campaign_names[cid] = row.campaign.name
            by_campaign[cid].append(_neg_entry(
                row.campaign_criterion.keyword.text,
                row.campaign_criterion.keyword.match_type.name,
            ))
    except Exception as exc:  # noqa: BLE001
        notes.append(f"Kampanya negatifleri okunamadı, bu kelimeler elenemedi ({exc})")

    by_ad_group: dict[str, list] = defaultdict(list)
    try:
        for row in _run_query(ga_service, customer_id, """
            SELECT ad_group.id,
                   ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
            FROM ad_group_criterion
            WHERE ad_group_criterion.negative = true
              AND ad_group_criterion.type = KEYWORD
        """, label="Ad group negatifleri sorgusu"):
            by_ad_group[str(row.ad_group.id)].append(_neg_entry(
                row.ad_group_criterion.keyword.text,
                row.ad_group_criterion.keyword.match_type.name,
            ))
    except Exception as exc:  # noqa: BLE001
        notes.append(f"Ad group negatifleri okunamadı, bu kelimeler elenemedi ({exc})")


    campaign_shared_sets: dict[str, list] = defaultdict(list)
    by_shared_set: dict[str, list] = defaultdict(list)
    try:
        for row in _run_query(ga_service, customer_id, """
            SELECT campaign.id, shared_set.id
            FROM campaign_shared_set
            WHERE shared_set.type = NEGATIVE_KEYWORDS
              AND campaign_shared_set.status = ENABLED
        """, label="Paylaşılan liste bağlantıları sorgusu"):
            campaign_shared_sets[str(row.campaign.id)].append(str(row.shared_set.id))
        for row in _run_query(ga_service, customer_id, """
            SELECT shared_set.id,
                   shared_criterion.keyword.text, shared_criterion.keyword.match_type
            FROM shared_criterion
            WHERE shared_set.type = NEGATIVE_KEYWORDS
              AND shared_criterion.type = KEYWORD
        """, label="Paylaşılan liste kelimeleri sorgusu"):
            by_shared_set[str(row.shared_set.id)].append(_neg_entry(
                row.shared_criterion.keyword.text,
                row.shared_criterion.keyword.match_type.name,
            ))
    except Exception as exc:  # noqa: BLE001
        notes.append(f"Paylaşılan negatif listeler okunamadı, bu listelerdeki kelimeler elenemedi: {exc}")

    account: list = []
    try:
        for row in _run_query(ga_service, customer_id, """
            SELECT customer_negative_criterion.keyword.text,
                   customer_negative_criterion.keyword.match_type
            FROM customer_negative_criterion
            WHERE customer_negative_criterion.type = KEYWORD
        """, label="Hesap seviyesi negatifler sorgusu"):
            account.append(_neg_entry(
                row.customer_negative_criterion.keyword.text,
                row.customer_negative_criterion.keyword.match_type.name,
            ))
    except Exception as exc:  # noqa: BLE001
        notes.append(f"Hesap seviyesi negatifler okunamadı: {exc}")

    return {
        "by_campaign": by_campaign,
        "by_ad_group": by_ad_group,
        "by_shared_set": by_shared_set,
        "campaign_shared_sets": campaign_shared_sets,
        "account": account,
        "campaign_names": campaign_names,
        "notes": notes,
    }


def _format_ads_exception(ex: GoogleAdsException) -> str:
    parts = [f"Request ID {ex.request_id} başarısız oldu:"]
    for error in ex.failure.errors:
        parts.append(f"  - {error.message}")
    return "\n".join(parts)

# Kural tabanlı negatif anahtar kelime aday tespiti.
# Sadece anlam/alaka bazlı tespit yapılır (performans/maliyet kriteri yok).
# Hesaba özel kriterler app/profiles/<hesap>.py dosyalarından gelir
# (bkz. app/profiles/registry.py) - bu dosya sadece TÜM hesaplarda
# geçerli olan genel (base) kuralları ve karar mantığını içerir.

import re

_TERM_PATTERN_CACHE: dict[str, re.Pattern] = {}
_PREFIX_PATTERN_CACHE: dict[str, re.Pattern] = {}


def _compile_term(term: str) -> re.Pattern:
    pattern = _TERM_PATTERN_CACHE.get(term)
    if pattern is None:
        pattern = re.compile(r"\b" + re.escape(term) + r"\b")
        _TERM_PATTERN_CACHE[term] = pattern
    return pattern


def _compile_prefix(term: str) -> re.Pattern:
    pattern = _PREFIX_PATTERN_CACHE.get(term)
    if pattern is None:
        pattern = re.compile(r"\b" + re.escape(term))
        _PREFIX_PATTERN_CACHE[term] = pattern
    return pattern


def _matches(term: str, text: str) -> bool:
    """Düz substring yerine kelime sınırına duyarlı (tam kelime/öbek) eşleşme.
    Örn. "ağda" terimi artık "yağdan" içinde, "kurs" terimi "kursu"
    içinde, "indir" terimi "indirim" içinde yanlışlıkla eşleşmez.
    """
    return bool(_compile_term(term).search(text))


def _matches_prefix(term: str, text: str) -> bool:
    """Sadece sol kelime sınırını zorunlu kılar, sağdan Türkçe ek almasına
    izin verir (örn. "otizm" kökü "otizmli" içinde de eşleşsin - context
    sinyali kökle birlikte gelen eklerle de tanınmalı). _matches'in aksine
    "yağdan" gibi kelime İÇİNDE gömülü olmayan ama kök+ek yapısında olan
    terimler için kullanılır (bkz. CONTEXT_SIGNAL_TERMS)."""
    return bool(_compile_prefix(term).search(text))


BASE_JUNK_TERMS = {
    "ücretsiz", "bedava", "iş ilanı", "iş ilanları", "indir", "download",
    "nasıl yapılır", "nasıl kullanılır", "youtube", "resim", "görsel",
    "wallpaper", "free", "job", "jobs", "salary", "maaş", "kariyer",
    "course", "kurs", "tutorial", "eğitim videosu", "şikayet", "şikayetvar",
    "eksisozluk", "ekşi sözlük", "wikipedia", "vikipedi", "second hand",
    "ikinci el", "sahibinden",
}

_AGE_YEAR_PATTERN = re.compile(r"(\d+)\s*yaş")
_AGE_MONTH_PATTERN = re.compile(r"(\d+)\s*ayl?ık?\b|(\d+)\s*\bay\b")


def _find_age_violation(term_lower: str, min_age_years) -> str | None:
    if not min_age_years:
        return None

    for match in _AGE_YEAR_PATTERN.finditer(term_lower):
        age = int(match.group(1))
        if age < min_age_years:
            return f"{age} yaş (minimum {min_age_years} yaş)"

    for match in _AGE_MONTH_PATTERN.finditer(term_lower):
        months = int(match.group(1) or match.group(2))
        if months < min_age_years * 12:
            return f"{months} aylık (minimum {min_age_years} yaş)"

    return None


def find_candidates(search_terms: list[dict], profile=None) -> list[dict]:
    """profile: app/profiles/<hesap>.py modülü, ya da None (özel profili
    olmayan hesaplar için - bu durumda sadece BASE_JUNK_TERMS uygulanır).
    """
    junk_terms = (
        BASE_JUNK_TERMS - set(getattr(profile, "JUNK_TERM_EXCEPTIONS", []))
    ) | set(getattr(profile, "EXTRA_JUNK_TERMS", []))
    competitor_names = getattr(profile, "COMPETITOR_NAMES", [])
    other_provider_names = getattr(profile, "OTHER_PROVIDER_NAMES", [])
    seasonal_terms = getattr(profile, "SEASONAL_TERMS", [])
    sales_terms = getattr(profile, "SALES_TERMS", [])
    not_offered_activities = getattr(profile, "NOT_OFFERED_ACTIVITIES", [])
    service_locations = getattr(profile, "SERVICE_LOCATIONS", [])
    other_major_cities = getattr(profile, "OTHER_MAJOR_CITIES", [])
    min_target_age_years = getattr(profile, "MIN_TARGET_AGE_YEARS", None)
    require_context_terms = getattr(profile, "REQUIRE_CONTEXT_TERMS", [])
    context_signal_terms = getattr(profile, "CONTEXT_SIGNAL_TERMS", [])
    business_name_variants = getattr(profile, "BUSINESS_NAME_VARIANTS", [])

    candidates = []
    for row in search_terms:
        term_lower = row["search_term"].lower()

        if any(_matches(name, term_lower) for name in business_name_variants):
            continue  # marka adı geçen arama - her zaman pozitif kabul edilir, diğer kontroller atlanır

        if any(_matches(comp, term_lower) for comp in competitor_names):
            continue  # rakip marka araması - marka karşılaştırma trafiği, pozitif kabul edilir

        # COMPETITOR_NAMES'in tam tersi: burada listelenen bir isim geçiyorsa
        # (rakip bir uzman/kurum vb.) marka karşılaştırması değil, doğrudan
        # başka bir sağlayıcı aranıyor demektir - her zaman negatif adaydır.
        matched_other_provider = [n for n in other_provider_names if _matches(n, term_lower)]
        if matched_other_provider:
            candidates.append({
                **row,
                "reasons": [
                    f"Farklı sağlayıcı/kurum ismi araması: {', '.join(matched_other_provider)}"
                ],
            })
            continue

        # Bazı kelimeler tek başına çok genel/belirsizdir ve sadece profilde
        # tanımlı bir "bağlam sinyali" (örn. engellilik ifadesi) eşlik ederse
        # gerçek bir hizmet arayışı sayılır. Sinyal yoksa diğer tüm muafiyet
        # kontrollerinden (sezonsal, satış vb.) önce doğrudan negatif adaydır.
        matched_context_trigger = [t for t in require_context_terms if _matches(t, term_lower)]
        if matched_context_trigger and not any(_matches_prefix(sig, term_lower) for sig in context_signal_terms):
            candidates.append({
                **row,
                "reasons": [
                    f"Özel gereksinim/engellilik bağlamı eksik: {', '.join(matched_context_trigger)}"
                ],
            })
            continue

        if any(_matches(season, term_lower) for season in seasonal_terms):
            continue  # donemsel/sezonsal arama - gercek hizmet arayisi olabilir, pozitif kabul edilir

        if any(_matches(sale, term_lower) for sale in sales_terms):
            continue  # satis firsati araması - gercek hizmet arayisi, pozitif kabul edilir

        reasons = []

        matched_junk = [j for j in junk_terms if _matches(j, term_lower)]
        if matched_junk:
            reasons.append(f"Alakasız kelime eşleşmesi: {', '.join(matched_junk)}")

        matched_activity = [a for a in not_offered_activities if _matches(a, term_lower)]
        if matched_activity:
            reasons.append(
                f"Sunulmayan hizmet/branş: {', '.join(matched_activity)}"
            )

        mentions_service_location = any(_matches(loc, term_lower) for loc in service_locations)
        if not mentions_service_location:
            matched_city = [c for c in other_major_cities if _matches(c, term_lower)]
            if matched_city:
                reasons.append(f"Hizmet bölgesi dışı şehir: {', '.join(matched_city)}")

        age_violation = _find_age_violation(term_lower, min_target_age_years)
        if age_violation:
            reasons.append(f"Hedef yaş aralığı dışı: {age_violation}")

        if reasons:
            candidates.append({**row, "reasons": reasons})

    return candidates


def filter_already_negative(candidates: list[dict], existing_negatives: dict) -> tuple[list[dict], int]:
    """Hesapta kampanya veya ad group seviyesinde zaten negatif olarak
    eklenmiş terimleri aday listesinden eler. Aynı kelimenin aynı hesaba
    tekrar tekrar negatif olarak eklenmeye çalışılmasını önler.
    Returns: (filtered_candidates, elenen_sayisi)
    """
    by_campaign = existing_negatives.get("by_campaign", {})
    by_ad_group = existing_negatives.get("by_ad_group", {})

    filtered = []
    skipped = 0
    for c in candidates:
        term_lower = c["search_term"].lower()
        already_negative = (
            term_lower in by_campaign.get(c["campaign_id"], ())
            or term_lower in by_ad_group.get(c["ad_group_id"], ())
        )
        if already_negative:
            skipped += 1
            continue
        filtered.append(c)

    return filtered, skipped

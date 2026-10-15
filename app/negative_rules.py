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


def is_exempt_row(row: dict, profile=None) -> bool:
    """Hiçbir negatif/AI incelemesine girmemesi gereken satırlar: adı
    EXEMPT_CAMPAIGN_KEYWORDS'ten birini içeren kampanyalar (örn. Türkiye
    genelinde bayi arayan franchise kampanyası) ve marka/rakip aramaları.
    """
    campaign_name = row.get("campaign_name", "").lower()
    if any(k in campaign_name for k in getattr(profile, "EXEMPT_CAMPAIGN_KEYWORDS", [])):
        return True
    term_lower = row["search_term"].lower()
    if any(_matches(n, term_lower) for n in getattr(profile, "BUSINESS_NAME_VARIANTS", [])):
        return True
    return any(_matches(c, term_lower) for c in getattr(profile, "COMPETITOR_NAMES", []))


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

    exempt_campaign_keywords = getattr(profile, "EXEMPT_CAMPAIGN_KEYWORDS", [])

    candidates = []
    for row in search_terms:
        term_lower = row["search_term"].lower()

        if any(k in row.get("campaign_name", "").lower() for k in exempt_campaign_keywords):
            continue  # muaf kampanya (örn. bayilik) - hiçbir arama negatif sayılmaz

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


def normalize_text(text: str) -> str:
    """Negatif/arama terimi karşılaştırması için Türkçe'ye duyarlı normalize.
    Python'un "İ".lower() sonucu birleşik noktalı 'i̇' üretir ve düz
    karşılaştırmada "izmir" ile eşleşmez; bu yüzden önce İ/I düzeltilir.
    Eşleme türü sembolleri ([ ] " +) ve fazla boşluklar da atılır.
    """
    text = text.replace("İ", "i").replace("I", "ı").lower()
    for ch in '[]"+':
        text = text.replace(ch, "")
    return " ".join(text.split())


def _blocks(entry: tuple, term_norm: str, term_tokens: tuple) -> bool:
    """Verilen negatif kayıt (norm, kelimeler, eşleme_türü) bu arama terimini
    Google'da fiilen engeller mi? Negatiflerde yakın varyant eşleşmesi yoktur,
    kelimeler birebir aranır."""
    neg_norm, neg_tokens, match_type = entry
    if not neg_tokens:
        return False
    if match_type == "EXACT":
        return neg_norm == term_norm
    if match_type == "PHRASE":
        n = len(neg_tokens)
        return any(term_tokens[i : i + n] == neg_tokens for i in range(len(term_tokens) - n + 1))
    return set(neg_tokens) <= set(term_tokens)  # BROAD


def _applicable_negatives(row: dict, existing: dict):
    cid, agid = row["campaign_id"], row["ad_group_id"]
    yield from existing.get("by_campaign", {}).get(cid, ())
    yield from existing.get("by_ad_group", {}).get(agid, ())
    for ssid in existing.get("campaign_shared_sets", {}).get(cid, ()):
        yield from existing.get("by_shared_set", {}).get(ssid, ())
    yield from existing.get("account", ())


def filter_already_negative(candidates: list[dict], existing_negatives: dict) -> tuple[list[dict], int]:
    """Bu aramayı Google'da zaten engelleyen bir negatif varsa (kampanya, ad
    group, kampanyaya bağlı paylaşılan liste ya da hesap seviyesinde;
    EXACT/PHRASE/BROAD eşleme türüne göre) adayı listeden eler. Aynı kelimenin
    tekrar tekrar negatife eklenmeye çalışılmasını önler.
    Returns: (filtered_candidates, elenen_sayisi)
    """
    filtered = []
    skipped = 0
    for c in candidates:
        term_norm = normalize_text(c["search_term"])
        term_tokens = tuple(term_norm.split())
        if any(_blocks(e, term_norm, term_tokens) for e in _applicable_negatives(c, existing_negatives)):
            skipped += 1
            continue
        filtered.append(c)
    return filtered, skipped


def annotate_negated_elsewhere(candidates: list[dict], existing_negatives: dict) -> None:
    """Aday başka bir kampanyada zaten negatifse (bu kampanyada değilse
    elenmez, çünkü bu kampanyayı korumaz) sebep listesine bunu ekler; böylece
    aynı kelimenin kampanyalar arası mükerrer eklenmesi bilinçli kararla yapılır.
    """
    by_campaign = existing_negatives.get("by_campaign", {})
    names = existing_negatives.get("campaign_names", {})
    for c in candidates:
        term_norm = normalize_text(c["search_term"])
        term_tokens = tuple(term_norm.split())
        elsewhere = [
            names.get(cid, cid)
            for cid, entries in by_campaign.items()
            if cid != c["campaign_id"] and any(_blocks(e, term_norm, term_tokens) for e in entries)
        ]
        if elsewhere:
            shown = ", ".join(elsewhere[:3]) + (" ..." if len(elsewhere) > 3 else "")
            c["reasons"] = [*c["reasons"], f"Başka kampanyada zaten negatif: {shown}"]

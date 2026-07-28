# Kural tabanlı negatif anahtar kelime aday tespiti.
# Sadece anlam/alaka bazlı tespit yapılır (performans/maliyet kriteri yok).
# Hesaba özel kriterler app/profiles/<hesap>.py dosyalarından gelir
# (bkz. app/profiles/registry.py) - bu dosya sadece TÜM hesaplarda
# geçerli olan genel (base) kuralları ve karar mantığını içerir.

import re

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
    junk_terms = BASE_JUNK_TERMS | set(getattr(profile, "EXTRA_JUNK_TERMS", []))
    competitor_names = getattr(profile, "COMPETITOR_NAMES", [])
    seasonal_terms = getattr(profile, "SEASONAL_TERMS", [])
    not_offered_activities = getattr(profile, "NOT_OFFERED_ACTIVITIES", [])
    service_locations = getattr(profile, "SERVICE_LOCATIONS", [])
    other_major_cities = getattr(profile, "OTHER_MAJOR_CITIES", [])
    min_target_age_years = getattr(profile, "MIN_TARGET_AGE_YEARS", None)

    candidates = []
    for row in search_terms:
        term_lower = row["search_term"].lower()

        if any(comp in term_lower for comp in competitor_names):
            continue  # rakip marka araması - marka karşılaştırma trafiği, pozitif kabul edilir

        if any(season in term_lower for season in seasonal_terms):
            continue  # donemsel/sezonsal arama - gercek hizmet arayisi olabilir, pozitif kabul edilir

        reasons = []

        matched_junk = [j for j in junk_terms if j in term_lower]
        if matched_junk:
            reasons.append(f"Alakasız kelime eşleşmesi: {', '.join(matched_junk)}")

        matched_activity = [a for a in not_offered_activities if a in term_lower]
        if matched_activity:
            reasons.append(
                f"Sunulmayan hizmet/branş: {', '.join(matched_activity)}"
            )

        mentions_service_location = any(loc in term_lower for loc in service_locations)
        if not mentions_service_location:
            matched_city = [c for c in other_major_cities if c in term_lower]
            if matched_city:
                reasons.append(f"Hizmet bölgesi dışı şehir: {', '.join(matched_city)}")

        age_violation = _find_age_violation(term_lower, min_target_age_years)
        if age_violation:
            reasons.append(f"Hedef yaş aralığı dışı: {age_violation}")

        if reasons:
            candidates.append({**row, "reasons": reasons})

    return candidates

# Kural tabanlı negatif anahtar kelime aday tespiti.
# Sadece anlam/alaka bazlı tespit yapılır (performans/maliyet kriteri yok).
# Junk kelime listesi ve işletme profili burada kolayca düzenlenebilir.

import re

from app.business_profile import (
    COMPETITOR_NAMES,
    NOT_OFFERED_ACTIVITIES,
    OTHER_MAJOR_CITIES,
    SERVICE_LOCATIONS,
)

JUNK_TERMS = {
    "ücretsiz", "bedava", "iş ilanı", "iş ilanları", "indir", "download",
    "nasıl yapılır", "nasıl kullanılır", "youtube", "resim", "görsel",
    "wallpaper", "free", "job", "jobs", "salary", "maaş", "kariyer",
    "course", "kurs", "tutorial", "eğitim videosu", "şikayet", "şikayetvar",
    "eksisozluk", "ekşi sözlük", "wikipedia", "vikipedi", "second hand",
    "ikinci el", "sahibinden", "belediye",
}

# Hedeflenen minimum yaş. Bunun altındaki bir yaş/ay geçen aramalar
# negatif aday olarak işaretlenir.
MIN_TARGET_AGE_YEARS = 4

_AGE_YEAR_PATTERN = re.compile(r"(\d+)\s*yaş")
_AGE_MONTH_PATTERN = re.compile(r"(\d+)\s*ayl?ık?\b|(\d+)\s*\bay\b")


def _find_age_violation(term_lower: str) -> str | None:
    for match in _AGE_YEAR_PATTERN.finditer(term_lower):
        age = int(match.group(1))
        if age < MIN_TARGET_AGE_YEARS:
            return f"{age} yaş (minimum {MIN_TARGET_AGE_YEARS} yaş)"

    for match in _AGE_MONTH_PATTERN.finditer(term_lower):
        months = int(match.group(1) or match.group(2))
        if months < MIN_TARGET_AGE_YEARS * 12:
            return f"{months} aylık (minimum {MIN_TARGET_AGE_YEARS} yaş)"

    return None


def find_candidates(search_terms: list[dict]) -> list[dict]:
    candidates = []
    for row in search_terms:
        term_lower = row["search_term"].lower()

        if any(comp in term_lower for comp in COMPETITOR_NAMES):
            continue  # rakip marka araması - marka karşılaştırma trafiği, pozitif kabul edilir

        reasons = []

        matched_junk = [j for j in JUNK_TERMS if j in term_lower]
        if matched_junk:
            reasons.append(f"Alakasız kelime eşleşmesi: {', '.join(matched_junk)}")

        matched_activity = [a for a in NOT_OFFERED_ACTIVITIES if a in term_lower]
        if matched_activity:
            reasons.append(
                f"Sunulmayan hizmet/branş: {', '.join(matched_activity)}"
            )

        mentions_service_location = any(loc in term_lower for loc in SERVICE_LOCATIONS)
        if not mentions_service_location:
            matched_city = [c for c in OTHER_MAJOR_CITIES if c in term_lower]
            if matched_city:
                reasons.append(f"Hizmet bölgesi dışı şehir: {', '.join(matched_city)}")

        age_violation = _find_age_violation(term_lower)
        if age_violation:
            reasons.append(f"Hedef yaş aralığı dışı: {age_violation}")

        if reasons:
            candidates.append({**row, "reasons": reasons})

    return candidates

# Kural tabanlı negatif anahtar kelime aday tespiti.
# Eşikler ve junk kelime listesi burada kolayca düzenlenebilir.

JUNK_TERMS = {
    "ücretsiz", "bedava", "iş ilanı", "iş ilanları", "indir", "download",
    "nasıl yapılır", "nasıl kullanılır", "youtube", "resim", "görsel",
    "wallpaper", "free", "job", "jobs", "salary", "maaş", "kariyer",
    "course", "kurs", "tutorial", "eğitim videosu", "şikayet", "şikayetvar",
    "eksisozluk", "ekşi sözlük", "wikipedia", "vikipedi", "second hand",
    "ikinci el", "sahibinden",
}

DEFAULT_MIN_CLICKS_ZERO_CONV = 3
DEFAULT_MIN_COST_ZERO_CONV = 50.0  # TL


def find_candidates(
    search_terms: list[dict],
    min_clicks_zero_conv: int = DEFAULT_MIN_CLICKS_ZERO_CONV,
    min_cost_zero_conv: float = DEFAULT_MIN_COST_ZERO_CONV,
) -> list[dict]:
    candidates = []
    for row in search_terms:
        term_lower = row["search_term"].lower()
        reasons = []

        if row["conversions"] == 0 and row["clicks"] >= min_clicks_zero_conv:
            reasons.append(
                f"{row['clicks']} tıklama, 0 dönüşüm (eşik: {min_clicks_zero_conv})"
            )

        if row["conversions"] == 0 and row["cost"] >= min_cost_zero_conv:
            reasons.append(
                f"{row['cost']:.2f} TL harcama, 0 dönüşüm (eşik: {min_cost_zero_conv} TL)"
            )

        matched_junk = [j for j in JUNK_TERMS if j in term_lower]
        if matched_junk:
            reasons.append(f"Alakasız kelime eşleşmesi: {', '.join(matched_junk)}")

        if reasons:
            candidates.append({**row, "reasons": reasons})

    return candidates

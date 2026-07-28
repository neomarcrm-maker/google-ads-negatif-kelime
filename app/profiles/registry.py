# Hangi Google Ads customer_id'nin hangi profile (app/profiles/*.py) ile
# eşleştiğini burada tanımla. Yeni bir hesap eklerken:
#   1. app/profiles/ altında yeni bir <hesap_adi>.py dosyası oluştur
#      (atlas.py'yi örnek al: SERVICE_LOCATIONS, NOT_OFFERED_ACTIVITIES,
#      COMPETITOR_NAMES, SEASONAL_TERMS, EXTRA_JUNK_TERMS, MIN_TARGET_AGE_YEARS)
#   2. Aşağıdaki PROFILE_MAP'e "customer_id": "modul_adi" olarak ekle

from importlib import import_module
from types import ModuleType

PROFILE_MAP: dict[str, str] = {
    "4103713203": "atlas",
    "1226048262": "issbay",
}


def get_profile(customer_id: str) -> ModuleType | None:
    module_name = PROFILE_MAP.get(customer_id.replace("-", "").strip())
    if not module_name:
        return None
    return import_module(f"app.profiles.{module_name}")

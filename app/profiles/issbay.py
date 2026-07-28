# İSBAY Kombi & Klima Servisi (issbay.com) işletme profili.
# negative_rules.py bu profili arama terimlerinin işletmeyle alakasını
# değerlendirmek için kullanır. registry.py bu dosyayı hangi customer_id
# ile eşleştireceğini belirler.

DISPLAY_NAME = "İSBAY Kombi & Klima Servisi"

BUSINESS_NAME_VARIANTS = [
    "isbay",
    "issbay",
    "isbay kombi klima servisi",
    "isbay klima",
]

# Sundukları hizmetler (bilgi amaçlı)
OFFERED_PROGRAMS = [
    "kombi servisi",
    "klima servisi",
    "doğalgaz servisi",
    "bakım",
    "arıza tespiti",
    "montaj",
    "gaz dolumu",
    "periyodik bakım",
    "ikinci el klima satışı",
]

# Hizmet bölgesi - İzmir merkez ilçeleri. Bu ilçeler geçen aramalar
# "hizmet bölgesi dışı şehir" olarak asla işaretlenmez, pozitif kabul edilir.
SERVICE_LOCATIONS = [
    "izmir", "bornova", "buca", "karşıyaka", "kemalpaşa", "bayraklı",
    "çiğli", "karabağlar", "gaziemir", "konak", "balçova", "narlıdere",
]

# Sunulmadığı bilinen, sıkça karıştırılabilecek hizmet/ürün türleri.
# "Klima"/"servis" kelimeleri çok genel olduğu için farklı bir cihaz/sektör
# arayan alakasız trafiği yakalamak için eklendi.
NOT_OFFERED_ACTIVITIES = [
    "oto klima", "araç klima", "araba klima",
    "beyaz eşya tamiri", "beyaz eşya servisi",
    "buzdolabı tamiri", "çamaşır makinesi tamiri", "bulaşık makinesi tamiri",
    "televizyon tamiri", "bilgisayar tamiri", "telefon tamiri",
]

# Büyük şehirler (İzmir hariç) - il/ilçe belirten aramalarda hizmet
# bölgesi dışı olabileceğini işaretlemek için kullanılır.
OTHER_MAJOR_CITIES = [
    "istanbul", "ankara", "bursa", "antalya", "adana", "konya",
    "gaziantep", "mersin", "kayseri", "eskişehir", "samsun", "denizli",
    "manisa", "aydın",
]

# Rakip firma isimleri - bu isimleri arayıp bizim reklamımıza tıklayanlar
# marka karşılaştırma trafiğidir, ASLA negatif işaretlenmez.
# İsimler öğrenildikçe buraya eklenecek.
COMPETITOR_NAMES: list[str] = []

# Dönemsel/sezonsal bakım aramaları - bunlar İSBAY için GERÇEK bir hizmet
# arayışıdır (yaz öncesi klima bakımı, kış öncesi kombi bakımı gibi),
# ASLA negatif işaretlenmez.
SEASONAL_TERMS = [
    "yaz bakımı", "kış bakımı", "sezon bakımı",
    "yaz öncesi bakım", "kış öncesi bakım", "sezonluk bakım",
]

# Bu hesap için genel (base) junk kelimelere ek bir kelime yok şimdilik.
EXTRA_JUNK_TERMS: set[str] = set()

# İSBAY ikinci el klima satışı da yapıyor - bu yüzden genel (base) junk
# kelime listesindeki "ikinci el" / "second hand" bu hesap için ASLA
# junk kelime sayılmaz (diğer hesaplarda alakasız sayılsa bile).
JUNK_TERM_EXCEPTIONS = {"ikinci el", "second hand"}

# Yaş kısıtı bu hesap için geçerli değil.
MIN_TARGET_AGE_YEARS = None

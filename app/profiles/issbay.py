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
    # Farklı meslek dalı - sıhhi tesisat/tesisatçılık kombi-klima servisinden
    # ayrı bir branştır.
    "sıhhi tesisat", "tesisatçı",
    # Marka garantili/ücretsiz "yetkili servis" arayanlar İSBAY'i değil,
    # ürünü sattıkları markanın kendi servisini arıyor - İSBAY yetkili
    # servis değil, bağımsız (ücretli) servistir.
    "yetkili servis",
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

# Kendin-yap / ürün arayışı - hizmet değil, kendi başına tamir/temizlik
# yapmak için ürün/malzeme arayan kişiler servis talebi değildir.
EXTRA_JUNK_TERMS: set[str] = {
    "temizleme spreyi", "klima spreyi", "gerekli malzemeler",
}

# İSBAY ikinci el klima satışı da yapıyor - bu yüzden genel (base) junk
# kelime listesindeki "ikinci el" / "second hand" bu hesap için ASLA
# junk kelime sayılmaz (diğer hesaplarda alakasız sayılsa bile).
JUNK_TERM_EXCEPTIONS = {"ikinci el", "second hand"}

# Klima satışıyla ilgili arama terimleri - bunlar İSBAY için GERÇEK bir
# satış fırsatıdır (sıfır/ikinci el klima satışı da yapıyorlar),
# ASLA negatif işaretlenmez.
SALES_TERMS = [
    "klima satış", "klima satışı", "klima satın al", "klima al",
    "sıfır klima", "kullanılmış klima", "klima fiyat", "klima fiyatları",
]

# Yaş kısıtı bu hesap için geçerli değil.
MIN_TARGET_AGE_YEARS = None

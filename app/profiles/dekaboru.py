# Deka Boru ve Ek Parçaları A.Ş. (dekaboru.com) işletme profili.
# negative_rules.py bu profili arama terimlerinin işletmeyle alakasını
# değerlendirmek için kullanır. registry.py bu dosyayı hangi customer_id
# ile eşleştireceğini belirler.
#
# Not: Bu hesap diğer profillerden (Atlas, İSBAY, Çimenci, Slimworld) farklı
# bir iş modeline sahip - yerel bir hizmet işletmesi DEĞİL, İzmir Ayrancılar'da
# üretim yapan ve 100+ bayi ile Türkiye geneline sevkiyat yapan bir polietilen
# boru ÜRETİCİSİ/toptancısıdır. Bu yüzden SERVICE_LOCATIONS / OTHER_MAJOR_CITIES
# mekanizması burada KULLANILMIYOR - başka şehirden gelen aramalar alakasız
# sayılmaz (nationwide sevkiyat yapıyorlar).

DISPLAY_NAME = "Deka Boru"

BUSINESS_NAME_VARIANTS = [
    "deka boru",
    "deka pipe",
    "deka boru ek parçaları",
]

# Sundukları ürün grupları (bilgi amaçlı)
OFFERED_PROGRAMS = [
    "damla sulama boruları",
    "su depoları",
    "pe100 boru sistemleri",
    "hortum ve ek parçaları",
    "tarımsal sulama ve peyzaj boruları",
    "koruge ve drenaj boruları",
    "mandallı yağmurlama sulama sistemleri",
    "pis su boruları ve ek parçaları",
    "pvc çatı oluğu ve yağmur iniş boruları",
    "pvc-u borular ve ek parçaları",
]

# Sadece polietilen/PVC (plastik) boru üretiyorlar. Farklı bir malzeme
# arayan trafiği yakalamak için eklendi - bu ürünleri Deka Boru üretmiyor.
NOT_OFFERED_ACTIVITIES = [
    "çelik boru", "demir boru", "metal boru", "bakır boru",
    "paslanmaz çelik boru", "dökme demir boru",
    # Deka Boru bir üretici/toptancıdır, tesisatçılık SERVİSİ vermez.
    # "tesisatçı çağır" gibi aramalar arızi bir servis talebidir, ürün
    # satın alma arayışı değildir.
    "tesisatçı", "sıhhi tesisatçı", "boru tamiri", "boru patlağı",
    "acil tesisatçı", "gider açma", "tıkanıklık açma",
]

# Rakip firma isimleri - bu isimleri arayıp bizim reklamımıza tıklayanlar
# marka karşılaştırma trafiğidir, ASLA negatif işaretlenmez.
# İsimler öğrenildikçe buraya eklenecek.
COMPETITOR_NAMES: list[str] = []

# "sahibinden" genel (base) junk kelime listesinde olsa da Deka Boru için
# istisna - bu hesapta negatif sayılmasın. "ikinci el"/"second hand" ise
# base listede kalmaya devam ediyor (istisna değil), o yüzden bu terimler
# ve türevleri yine negatif aday sayılır.
JUNK_TERM_EXCEPTIONS = {"sahibinden"}

# EN ÖNEMLİ HEDEF: Deka Boru sadece palet/kamyon/tır bazında toptan satış
# yapıyor (minimum sipariş miktarı var). Hırdavatçı, nalbur, bayilerin
# perakende mağazasını arayan küçük/tekil müşteriler bu hesabın reklamını
# TIKLAMAMALI - bu, işletmenin en büyük şikayet ettiği sorun. Bu yüzden
# perakende/küçük miktar sinyali taşıyan terimler agresif şekilde negatif
# aday sayılır.
EXTRA_JUNK_TERMS = {
    "hırdavat", "hırdavatçı", "nalbur", "nalburiye",
    "perakende", "parekende",
    "yapı market", "yapı marketi",
    "tek adet", "1 adet", "adet fiyatı",
    "en yakın", "yakınımda", "mağaza", "mağazası",
}

# Yaş kısıtı bu hesap için geçerli değil (B2B/endüstriyel ürün satışı).
MIN_TARGET_AGE_YEARS = None

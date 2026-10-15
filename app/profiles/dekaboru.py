# Deka Boru ve Ek Parçaları A.Ş. (dekaboru.com) işletme profili.
# negative_rules.py bu profili arama terimlerinin işletmeyle alakasını
# değerlendirmek için kullanır. registry.py bu dosyayı hangi customer_id
# ile eşleştireceğini belirler.
#
# Not: Bu hesap diğer profillerden (Atlas, İSBAY, Çimenci, Slimworld) farklı
# bir iş modeline sahip - yerel bir hizmet işletmesi DEĞİL, İzmir Ayrancılar'da
# üretim yapan bir polietilen boru ÜRETİCİSİ/toptancısıdır. Fiilen sadece
# belirli bir bölgede (Ege + yakın çevre illeri) faaliyet gösteriyor - bkz.
# SERVICE_LOCATIONS.

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

# Hizmet/faaliyet bölgesi illeri. Bu iller geçen aramalar "hizmet bölgesi
# dışı şehir" olarak asla işaretlenmez, pozitif kabul edilir.
SERVICE_LOCATIONS = [
    "izmir", "manisa", "aydın", "denizli", "antalya", "muğla",
    "uşak", "çanakkale", "balıkesir", "bursa",
]

# Büyük şehirler (yukarıdaki hizmet bölgesi illeri hariç) - il belirten
# aramalarda hizmet bölgesi dışı olabileceğini işaretlemek için kullanılır.
OTHER_MAJOR_CITIES = [
    "istanbul", "ankara", "adana", "konya", "gaziantep",
    "mersin", "kayseri", "eskişehir", "samsun",
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
    # Molecor - farklı bir marka (rakip) arayışı, Deka Boru ürünü değil.
    "molecor",
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
    # "ikinci el" base kuralda zaten var - bunlar onun ek yazım türevleri.
    "2. el", "2 el",
    # İşin/malzemenin nasıl yapılacağına/döşeneceğine dair aramalar (örn.
    # "drenaj borusu döşeme") kendin-yap/bilgi arayışıdır, ürün satın alma
    # niyeti değildir - Deka Boru bir üretici/toptancıdır, uygulama rehberi
    # sunmaz.
    "döşeme", "döşenir", "döşenmesi", "nasıl döşenir",
    "montajı nasıl yapılır", "nasıl monte edilir", "nasıl bağlanır",
    "kendin yap",
}

# Yaş kısıtı bu hesap için geçerli değil (B2B/endüstriyel ürün satışı).
MIN_TARGET_AGE_YEARS = None

# Anlam bazlı AI incelemesi için işletme tarifi (bkz. app/ai_review.py).
# Kelime kurallarından geçen aramalar bu tarife göre Claude tarafından
# değerlendirilir; işletmeye uymayan aramalar negatif aday olur. Kararsız
# kalınan aramalar işaretlenmez. Marka/rakip adı geçen aramalar zaten
# incelemeye girmez. Tarif yanlış yakalama/kaçırma gördükçe güncellenir.
AI_REVIEW_BRIEF = """Deka Boru ve Ek Parçaları A.Ş. (İzmir Torbalı): polietilen (PE100) ve PVC plastik boru, ek parça, damla sulama, tarımsal sulama/peyzaj boruları, koruge ve drenaj boruları, su depoları, hortum, yağmurlama sistemleri, pis su ve PVC-U boruları üreten TOPTAN satış yapan üretici. Satış palet/kamyon/tır bazında, minimum sipariş miktarı var, bayilik sistemiyle çalışıyor. Faaliyet bölgesi: İzmir, Manisa, Aydın, Denizli, Antalya, Muğla, Uşak, Çanakkale, Balıkesir, Bursa.

UYGUN (negatif yapma): toptan/fabrika/üretici boru ve ek parça arayışı, proje ve altyapı alımları, sulama sistemi ürünleri, fiyat listesi/teklif, bayilik ve bayi olma, bu illerdeki aramalar, sahibinden geçen aramalar.

UYGUN DEĞİL (negatif yap): perakende/küçük miktar alıcıları (hırdavatçı, nalbur, tek adet, metre fiyatı, yapı market, en yakın mağaza); ikinci el / 2. el; çelik, demir, bakır, dökme demir, paslanmaz gibi metal boru arayışları (GALVANİZ boru istisnadır, negatif yapma); tesisatçı, boru tamiri, gider açma gibi servis aramaları; döşeme/montaj nasıl yapılır gibi kendin yap bilgi aramaları; Molecor markası; iş ilanı; faaliyet bölgesi dışındaki büyük şehirler."""

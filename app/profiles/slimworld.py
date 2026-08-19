# Slimworld işletme profili.
# negative_rules.py bu profili arama terimlerinin işletmeyle alakasını
# değerlendirmek için kullanır. registry.py bu dosyayı hangi customer_id
# ile eşleştireceğini belirler.
#
# İşletme: kilo verme/zayıflama merkezi. Spor yoluyla zayıflama (pilates,
# reformer pilates) ve Vacu Activ / InfraShape cihaz uygulamaları sunuyor.
# Gerçek müşteri profili: kilo vermek isteyen ve bunun için spor ya da
# sahip oldukları cihaz temelli yöntemleri arayan kişiler. Sporsuz/evde
# yapılan DIY diyet arayışları ve sahip olmadıkları cihaz/hizmet
# aramaları negatif adaydır.

DISPLAY_NAME = "Slimworld"

BUSINESS_NAME_VARIANTS = [
    "slimworld",
    "slim world",
]

# Sundukları hizmetler (bilgi amaçlı)
OFFERED_PROGRAMS = [
    "pilates", "reformer pilates", "reformer",
    "vacu activ", "vacuactiv", "infrashape", "infra shape",
]

# Hizmet bölgesi - sadece İzmir ve Ankara'da reklam veriliyor. Bu şehirler
# dışındaki aramalar "hizmet bölgesi dışı şehir" olarak negatif adaydır.
SERVICE_LOCATIONS = ["izmir", "ankara"]

# Sunulmadığı bilinen, sıkça karıştırılabilecek hizmet/ürün türleri.
# Güzellik salonu hizmetleri (zayıflama değil) ve sahip olunmayan
# zayıflama cihaz/teknolojileri.
NOT_OFFERED_ACTIVITIES = [
    # Güzellik salonu hizmetleri - zayıflama merkezi değil, kozmetik/bakım arayışı
    "ağda", "epilasyon", "lazer epilasyon", "manikür", "pedikür",
    "cilt bakımı", "güzellik salonu", "kalıcı makyaj",
    # Sahip olunmayan zayıflama cihaz/teknolojileri
    "kavitasyon", "radyofrekans", "rf cihazı", "lenf drenaj",
    "lenfatik drenaj", "ems cihazı", "elektrostimülasyon",
    "g5 cihazı", "lpg cihazı", "endermologie",
    "kriyolipoliz", "soğuk lipoliz", "cool sculpting", "yağ dondurma",
    "heykeltıraş cihazı",
]

# Büyük şehirler (İzmir/Ankara hariç) - il/ilçe belirten aramalarda
# hizmet bölgesi dışı olabileceğini işaretlemek için kullanılır.
OTHER_MAJOR_CITIES = [
    "istanbul", "bursa", "antalya", "adana", "konya", "gaziantep",
    "mersin", "kayseri", "eskişehir", "samsun", "denizli", "manisa",
    "aydın", "diyarbakır", "trabzon", "kocaeli", "sakarya",
]

# Rakip firma isimleri - bu isimleri arayıp bizim reklamımıza tıklayanlar
# marka karşılaştırma trafiğidir, ASLA negatif işaretlenmez.
# İsimler öğrenildikçe buraya eklenecek.
COMPETITOR_NAMES: list[str] = []

SEASONAL_TERMS: list[str] = []

# Genel (base) junk kelimelere ek olarak bu hesaba özel eklenen kelimeler.
# Sporsuz, evde yapılan spesifik DIY diyet/tarif/kür arayışları - gerçek
# müşteri değil, kendi başına ev yöntemiyle kilo vermek isteyenler.
EXTRA_JUNK_TERMS: set[str] = {
    "lahana diyeti", "elma diyeti", "tohum diyeti",
    "diyet tarifi", "diyet tarifleri", "zayıflama tarifi",
    "kilo verme tarifi", "evde zayıflama", "ev yapımı zayıflama",
    "detoks tarifi", "sirke kürü", "limon kürü", "tarçın kürü",
    "zencefil kürü", "zayıflama çayı tarifi",
}

JUNK_TERM_EXCEPTIONS: set[str] = set()

# Spor yoluyla ya da sahip olunan cihazlarla zayıflama - gerçek hizmet
# arayışı, ASLA negatif işaretlenmez.
SALES_TERMS = [
    "pilates ile zayıflama", "reformer ile zayıflama",
    "spor ile kilo verme", "vacu activ", "infrashape",
]

REQUIRE_CONTEXT_TERMS: list[str] = []
CONTEXT_SIGNAL_TERMS: list[str] = []

# Yaş kısıtı bu hesap için geçerli değil.
MIN_TARGET_AGE_YEARS = None

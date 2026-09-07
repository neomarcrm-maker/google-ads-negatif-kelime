# Kordon Psikoloji Merkezi (kordonpsikoloji.com) işletme profili.
# negative_rules.py bu profili arama terimlerinin işletmeyle alakasını
# değerlendirmek için kullanır. registry.py bu dosyayı hangi customer_id
# ile eşleştireceğini belirler.

DISPLAY_NAME = "Kordon Psikoloji Merkezi"

BUSINESS_NAME_VARIANTS = [
    "kordon psikoloji",
    "kordon psikoloji merkezi",
    "kordon rehberlik",
    "özel kordon rehberlik",
    # Merkezin kendi uzmanları - isimleri geçen aramalar kendi markasına
    # aittir, negatif işaretlenmemeli.
    "nilay aykutlu",
    "didem hicran ersan",
]

# Sundukları hizmetler (bilgi amaçlı)
OFFERED_PROGRAMS = [
    "bireysel danışmanlık",
    "çift danışmanlığı",
    "aile danışmanlığı",
    "online psikolojik danışmanlık",
]

# Hizmet bölgesi - İzmir merkez ilçeleri. Bu ilçeler geçen aramalar
# "hizmet bölgesi dışı şehir" olarak asla işaretlenmez, pozitif kabul edilir.
# Not: online danışmanlık da sunuluyor ama hedefleme sadece İzmir odaklı
# tutuluyor (kullanıcı tercihi) - bu yüzden diğer şehir aramaları yine de
# negatif aday sayılır (bkz. OTHER_MAJOR_CITIES).
SERVICE_LOCATIONS = [
    "izmir", "balçova", "konak", "buca", "urla", "karabağlar", "gaziemir", "çeşme","güzelbahçe","narlıdere"
]

# Sunulmadığı bilinen, sıkça karıştırılabilecek meslek/hizmet dalları.
# SSS'de özellikle vurgulanmış: psikolog ilaç yazmaz/reçete vermez, bu
# psikiyatristin işidir - psikiyatrist/ilaç/reçete arayan farklı bir
# hizmet arıyordur.
NOT_OFFERED_ACTIVITIES = [
    "psikiyatrist", "psikiyatri", "ilaç tedavisi", "reçete", "ilaç yazan",
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

# Genel (base) junk kelimelere ek olarak bu hesaba özel eklenen kelimeler.
# Psikoloji bölümünü araştıran öğrenci/kariyer arayışları - danışmanlık
# hizmeti arayışı değildir.
EXTRA_JUNK_TERMS = {
    "psikoloji bölümü", "psikoloji taban puan", "psikoloji taban puanları",
    "psikolog nasıl olunur", "psikoloji lisans", "psikoloji yüksek lisans",
    # Bilinçli iş kararı: bu hizmetler sitede sunulsa da reklam bütçesi
    # başka hizmetlere ayrıldığı için artık hedeflenmiyor.
    "grup terapisi", "oyun terapi", "oyun terapisi", "ergen",
    "hastane",
}

# Yaş kısıtı bu hesap için geçerli değil - çocuk, ergen ve yetişkin
# danışmanlığı birlikte sunuluyor.
MIN_TARGET_AGE_YEARS = None

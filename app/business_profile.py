# Atlas Spor Merkezi (atlasspormerkezi.com.tr) işletme profili.
# negative_rules.py bu dosyayı arama terimlerinin işletmeyle alakasını
# değerlendirmek için kullanır. Farklı bir müşteri/proje için bu dosyayı
# güncelleyip yeni bir profil oluşturmak yeterli.

BUSINESS_NAME_VARIANTS = [
    "atlas spor merkezi",
    "atlas otizm spor merkezi",
    "atlas hareket eğitim merkezi",
    "atlas spor akademi",
    "atlas spor eğitim merkezi",
]

# Sundukları eğitim/hizmet alanları
OFFERED_PROGRAMS = [
    "hareket eğitimi",
    "temel branş eğitimi",
    "akran eğitimi",
    "kaynaştırma",
    "yaşam liderliği eğitimi",
    "sosyal adaptasyon",
    "otizm",
    "dehb",
    "down sendromu",
    "gelişim geriliği",
    "özel gereksinim",
]

# Sundukları spor branşları
OFFERED_SPORTS = [
    "masa tenisi",
    "bisiklet",
    "paten",
    "cimnastik",
    "jimnastik",
    "futbol",
    "basketbol",
]

# Hizmet bölgesi - bu şehir/ilçe dışındaki aramalar muhtemelen alakasız.
# İzmir merkez ilçeleri (Buca'ya makul mesafede) dahil edildi, bunlar
# "hizmet bölgesi dışı şehir" olarak asla işaretlenmez, pozitif kabul edilir.
SERVICE_LOCATIONS = [
    "izmir", "buca", "bornova", "karşıyaka", "konak", "çiğli",
    "gaziemir", "bayraklı", "balçova", "narlıdere", "karabağlar",
    "kemalpaşa", "torbalı", "menderes",
]

# Sunulmadığı bilinen, sıkça karıştırılabilecek spor/aktivite dalları.
# Bu dalların aranması, işletmenin sunmadığı bir hizmeti arayan
# alakasız trafiği işaret edebilir.
NOT_OFFERED_ACTIVITIES = [
    "yüzme", "yüzme kursu", "yoga", "pilates", "karate", "taekwondo",
    "güreş", "boks", "kick boks", "vücut geliştirme", "crossfit",
    "dans kursu", "bale", "halk oyunları", "yürüyüş bandı", "fitness salonu",
    "spor salonu üyelik", "gym üyelik",
]

# Büyük şehirler (İzmir/Buca hariç) - il/ilçe belirten aramalarda
# hizmet bölgesi dışı olabileceğini işaretlemek için kullanılır.
OTHER_MAJOR_CITIES = [
    "istanbul", "ankara", "bursa", "antalya", "adana", "konya",
    "gaziantep", "mersin", "kayseri", "eskişehir", "samsun", "denizli",
    "manisa", "aydın",
]

# Rakip firma isimleri. Bu isimleri arayıp bizim reklamımıza tıklayanlar
# marka karşılaştırma trafiğidir - negatif kelime olarak ASLA işaretlenmez,
# pozitif kabul edilir. İsimler öğrenildikçe buraya eklenecek.
COMPETITOR_NAMES: list[str] = []

# Dönemsel/sezonsal terimler - "yaz okulu" gibi aramalar gerçek bir hizmet
# arayışı olabilir (işletme bu programları sunuyor olabilir), bu yüzden
# negatif kelime olarak ASLA işaretlenmez, pozitif kabul edilir.
SEASONAL_TERMS = [
    "yaz okulu", "yaz kampı", "kış kampı", "yarıyıl kampı",
    "sezonluk", "yaz dönemi", "kış dönemi", "yaz etkinliği",
]

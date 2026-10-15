# Atlas Spor Merkezi (atlasspormerkezi.com.tr) işletme profili.
# negative_rules.py bu profili arama terimlerinin işletmeyle alakasını
# değerlendirmek için kullanır. registry.py bu dosyayı hangi customer_id
# ile eşleştireceğini belirler.

DISPLAY_NAME = "Atlas Spor Merkezi"

BUSINESS_NAME_VARIANTS = [
    "atlas spor merkezi",
    "atlas otizm spor merkezi",
    "atlas hareket eğitim merkezi",
    "atlas spor akademi",
    "atlas spor eğitim merkezi",
]

# Sundukları eğitim/hizmet alanları (bilgi amaçlı)
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

# Sundukları spor branşları (bilgi amaçlı)
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

# Rakip firma isimleri - bu isimleri arayıp bizim reklamımıza tıklayanlar
# marka karşılaştırma trafiğidir, ASLA negatif işaretlenmez.
COMPETITOR_NAMES: list[str] = []

# Dönemsel/sezonsal terimler - gerçek bir hizmet arayışı olabilir,
# ASLA negatif işaretlenmez. "yaz okulu" burada YOK - REQUIRE_CONTEXT_TERMS
# altında, çünkü engellilik bağlamı olmadan sıradan bir yaz okulu arayışı
# olabilir (bkz. aşağıda).
SEASONAL_TERMS = [
    "yaz kampı", "kış kampı", "yarıyıl kampı",
    "sezonluk", "yaz dönemi", "kış dönemi", "yaz etkinliği",
]

# Genel (base) junk kelimelere ek olarak bu hesaba özel eklenen kelimeler.
# "sosyal hizmet" / "sağlık bakanlığı" - ücretsiz devlet kurumu hizmeti
# arayanlar, Atlas özel (ücretli) bir merkezdir.
EXTRA_JUNK_TERMS = {"belediye", "sosyal hizmet", "sağlık bakanlığı"}

# Bu kelimelerden biri aramada geçiyorsa VE aşağıdaki CONTEXT_SIGNAL_TERMS
# listesinden hiçbiri geçmiyorsa, arama negatif aday sayılır. Atlas özel
# gereksinimli (otizm, DEHB, down sendromu vb.) çocuklara yönelik bir spor
# eğitim merkezidir - bu yüzden "jimnastik kursu", "spor akademisi" gibi
# sıradan/genel spor aramaları, içinde bir engellilik/özel gereksinim ifadesi
# geçmiyorsa muhtemelen sıradan (özel gereksinimi olmayan) bir arayıştır.
# Not: "yüzme" burada değil - Atlas hiçbir bağlamda yüzme sunmuyor, bu yüzden
# NOT_OFFERED_ACTIVITIES'te koşulsuz negatif olarak kalıyor.
REQUIRE_CONTEXT_TERMS = [
    "tenis", "jimnastik", "cimnastik", "futbol", "basketbol",
    "bisiklet", "paten", "kickbox", "kick box",
    "spor akademisi", "spor salonu", "spor alanı",
    "çocuk sporu", "çocuklar için spor", "çocuk etkinlikleri",
    "yaz okulu",
]

# REQUIRE_CONTEXT_TERMS'teki bir kelime bunlardan biriyle birlikte geçerse
# gerçek bir özel gereksinim hizmeti arayışı sayılır, negatif işaretlenmez.
CONTEXT_SIGNAL_TERMS = [
    "otizm", "otistik", "engelli", "engel", "dehb", "down sendromu",
    "down sendromlu", "gelişim geriliği", "gelişimsel gerilik",
    "özel gereksinim", "kaynaştırma", "spektrum", "asperger",
    "özel eğitim", "psikomotor",
]

# Hedeflenen minimum yaş. Bunun altındaki bir yaş/ay geçen aramalar
# negatif aday olarak işaretlenir. Yaş kısıtı olmayan hesaplarda None yapılır.
MIN_TARGET_AGE_YEARS = 4

# Anlam bazlı AI incelemesi için işletme tarifi (bkz. app/ai_review.py).
# Kelime kurallarından geçen aramalar bu tarife göre Claude tarafından
# değerlendirilir; işletmeye uymayan aramalar negatif aday olur. Kararsız
# kalınan aramalar işaretlenmez. Marka/rakip adı geçen aramalar zaten
# incelemeye girmez. Tarif yanlış yakalama/kaçırma gördükçe güncellenir.
AI_REVIEW_BRIEF = """Atlas Spor Merkezi (İzmir, Buca): otizm, DEHB, down sendromu, gelişim geriliği gibi özel gereksinimli çocuk ve gençlere yönelik hareket eğitimi ve spor merkezi (masa tenisi, bisiklet, paten, cimnastik, futbol, basketbol; akran eğitimi, kaynaştırma, sosyal adaptasyon). Müşteri: 4 yaş ve üzeri özel gereksinimli bireyin ebeveyni ya da yakını.

UYGUN (negatif yapma): özel gereksinimli çocuk için spor/hareket eğitimi, otizm/DEHB/down sendromu için spor merkezi, özel eğitim ve kaynaştırma sporu, fiyat/randevu/adres/yorum, yaz-kış kampı, İzmir ve çevresi.

UYGUN DEĞİL (negatif yap): özel gereksinimle ilgisi olmayan sıradan spor/kurs/okul aramaları (genel jimnastik kursu, spor salonu/fitness üyeliği, yüzme, yoga, pilates, karate, dans, bale), yetişkin fitness, ücretsiz belediye/devlet hizmeti arayışı, tıbbi tedavi/ilaç/doktor/hastane aramaları, iş ilanı, 4 yaşından küçük bebek aramaları, İzmir dışı şehirler."""

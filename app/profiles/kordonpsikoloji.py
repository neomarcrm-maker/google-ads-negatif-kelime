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
    # Bilinçli iş kararı: bu hesap artık psikolojik test ve kurumsal
    # danışmanlık hizmetlerini hedeflemiyor.
    "test", "testi", "testler", "testleri",
    "psikolojik test", "psikolojik testi", "psikolojik testler", "psikolojik testleri",
    "kurumsal danışmanlık", "kurum danışmanlığı",
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

# COMPETITOR_NAMES'in TERSİ: burada geçen bir isim, Kordon'un kendi
# uzmanları (Nilay Aykutlu, Didem Hicran Ersan) DIŞINDA farklı bir
# psikolog/psikoloji merkezi arandığı anlamına gelir - her zaman negatif
# aday sayılır. Aşağıdaki isimler İzmir merkez ilçelerinde (Balçova, Konak,
# Karşıyaka, Bornova, Buca, Bayraklı, Çiğli, Karabağlar, Gaziemir, Narlıdere)
# web araştırmasıyla bulunan gerçek rakip psikoloji merkezi/psikolog
# isimleridir. Bilinçli olarak "<ilçe> psikolog" gibi jenerik/markasız arama
# kalıbıyla aynı görünen isimler (örn. "bornova psikolog", "çiğli psikolog")
# DAHİL EDİLMEDİ - bunlar gerçek marka aramasından ayırt edilemez. Randevu
# dizin siteleri (DoktorTakvimi, Doktorsitesi vb.) de rakip değil, hariç.
OTHER_PROVIDER_NAMES: list[str] = [
    "anka psikoloji", "ekol tıp merkezi", "lotus psikoterapi",
    "etka psikoloji", "konak psikoloji merkezi",
    "diyalog psikoloji", "değişim psikoloji", "aybros psikoloji",
    "eka psikoloji", "pilea psikoloji", "haziran psikoloji",
    "ida psikoloji", "hipath psikoloji", "psikosentez", "idil rehberlik",
    "dese psikoloji", "kağan ay", "şans psikoloji",
    "burcu budak", "sofist psikoloji", "altuğ psikoloji",
    "enki psikolojik danışmanlık", "narlıdere yaşam merkezi",
    "yaşam psikoloji", "sarı psikoloji", "cemre özcan", "metehan aykut",
]

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
    # Belediyelerin sunduğu ÜCRETSİZ psikolojik danışmanlık hizmeti - Kordon
    # özel (ücretli) bir merkezdir, bu yüzden hedef kitle değildir.
    # SERVICE_LOCATIONS'daki her ilçe için otomatik türetilir.
    *{f"{loc} belediyesi" for loc in SERVICE_LOCATIONS},
    "belediye", "ücretsiz psikolojik danışmanlık", "izsem",
}

# Yaş kısıtı bu hesap için geçerli değil - çocuk, ergen ve yetişkin
# danışmanlığı birlikte sunuluyor.
MIN_TARGET_AGE_YEARS = None

# Anlam bazlı AI incelemesi için işletme tarifi (bkz. app/ai_review.py).
# Kelime kurallarından geçen aramalar bu tarife göre Claude tarafından
# değerlendirilir; işletmeye uymayan aramalar negatif aday olur. Kararsız
# kalınan aramalar işaretlenmez. Marka/rakip adı geçen aramalar zaten
# incelemeye girmez. Tarif yanlış yakalama/kaçırma gördükçe güncellenir.
AI_REVIEW_BRIEF = """Kordon Psikoloji Merkezi (İzmir Balçova): bireysel danışmanlık, çift ve aile danışmanlığı, online psikolojik danışmanlık veren özel (ücretli) bir psikoloji merkezi. Uzmanları: Nilay Aykutlu, Didem Hicran Ersan. İzmir odaklı hedefleme.

UYGUN (negatif yapma): İzmir ve ilçelerinde psikolog/psikolojik danışman arayışı (markasız genel aramalar dahil: "izmir psikolog", "balçova aile danışmanlığı"), kaygı, stres, ilişki sorunları, çift/aile terapisi, online terapi, fiyat/randevu.

UYGUN DEĞİL (negatif yap): grup terapisi, oyun terapisi, çocuk/ergen odaklı aramalar, psikolojik test, kurumsal danışmanlık; psikiyatrist, ilaç, reçete, hastane; belediyelerin ücretsiz danışmanlık hizmeti; başka bir psikolog ya da psikoloji merkezinin adını arayanlar; psikoloji bölümü/taban puan/lisans gibi öğrenci ve kariyer aramaları; iş ilanı; İzmir dışı şehirler."""

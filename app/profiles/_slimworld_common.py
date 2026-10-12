# Slimworld profilleri (slimworld.py = İzmir/Ankara, slimworld_zekeriyakoy.py)
# arasında ortak kullanılan negatif terimler ve AI inceleme örnekleri.
# Slimworld spor/cihaz (Vacu Activ, Infrashape, Infrastep, RollShape)
# temelli bir kilo kontrol merkezidir; aşağıdakiler gerçek müşteri
# olmayan, hesapta fiilen yakalanmış arama kalıplarıdır.
#
# Not: kelime sınırı eşleşmesi Türkçe ekleri yakalamaz, o yüzden yaygın
# çekimler ve aksansız yazımlar ayrıca listelendi. Uzun kuyruğu AI inceleme
# katmanı (app/ai_review.py) anlam bazlı yakalar.

COMMON_JUNK_TERMS: set[str] = {
    # Yiyecek / bitki / içecek ile kilo verme (spor dışı yöntem)
    "mercimek", "kabak", "karanfil", "hünnap", "pancar", "salatalık",
    "tahin", "hurma", "zerdeçal", "omlet", "ekmek", "ekmeği",
    "yulaf", "yulaf ezmesi", "yulaflı", "ezmesi",
    "içecek", "içecekler", "bitki", "bitkiler", "bitkisel",
    "otu", "karnıyarık otu", "çay", "çaylar", "çayları", "çayı",
    "kahve", "kahveler", "kahveleri", "meyve suyu", "smoothie", "detoks",
    # Takviye / marka ürün / diyet
    "kapsül", "kapsüller", "kapsülleri", "shake", "hap", "hapı",
    "takviye", "takviyesi", "herbalife", "dietto", "slimo burn",
    "grow with jo", "diet", "diyete", "diyetle",
    # İğne / enjeksiyon / medikal estetik
    "iğne", "iğneleri", "iğnesi", "iğnesini", "iğneli",
    "igne", "igneleri", "ignesi", "ignesini", "enjeksiyon", "mezoterapi",
    "liposuction", "liposakşın", "lipo", "ameliyatsız liposuction",
    "coolsculpting", "cool sculpting",
    # Alternatif tıp / terapi
    "biorezonans", "rezonans", "andulasyon", "andülasyon",
    "andulasyon terapi", "terapi", "refleksoloji", "hacamat",
    # Sahip olunmayan cihaz/yöntemler
    "g5", "g9", "g10", "selfodeep", "heykeltraş", "fragment", "abdominal",
    # Sunulmayan spor/aktiviteler ve evde/hareketsiz yöntemler
    "yoga", "yogası", "dans", "danslar", "havuz", "havuzlu",
    "calisthenics", "kalistenik", "evde", "oturarak", "sandalye",
    "sandalyede", "yatak", "yatakda", "yatakta", "yatarak",
}

# AI_REVIEW_BRIEF'in sonuna eklenir: modele somut "uygun değil" örnekleri.
AI_EXAMPLES = """

Hesapta fiilen yakalanmış UYGUN DEĞİL örnekleri (tek kelime olsalar bile): mercimek, kabak, \
pancar, tahin, hurma, zerdeçal, omlet, yulaf ezmesi, bitki çayı, kahve, kapsül, shake, \
herbalife, dietto, slimo burn, grow with jo, diyet/diet, iğne/iğneleri, akupunktur, \
biorezonans, andulasyon terapi, ameliyatsız liposuction, coolsculpting, g5/g9/g10, \
selfodeep, heykeltraş, yoga, dans, havuz, calisthenics, evde/oturarak/sandalyede/yatakta \
yapılan egzersizler, masaj, epilasyon, doktor, ilaç. Bunlar spor/cihaz temelli bir merkeze \
gelecek müşteri niyeti taşımaz. Yazım hatalı ya da aksansız yazılmış halleri de aynıdır."""

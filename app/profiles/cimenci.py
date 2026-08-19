# Çimenci işletme profili.
# negative_rules.py bu profili arama terimlerinin işletmeyle alakasını
# değerlendirmek için kullanır. registry.py bu dosyayı hangi customer_id
# ile eşleştireceğini belirler.
#
# İşletme: canlı çim üretimi/satışı yapıyor, ayrıca dükkanda suni çim
# satışı ve peyzaj/çim uygulaması (kurulum) hizmeti veriyor. Satıcı taraf -
# gerçek müşteri profili: suni/canlı çim satın almak isteyen ya da
# bahçesine/villasına uygulama yaptırmak isteyen kişiler.

DISPLAY_NAME = "Çimenci"

BUSINESS_NAME_VARIANTS = [
    "çimenci",
    "cimenci",
]

# Sundukları hizmetler (bilgi amaçlı)
OFFERED_PROGRAMS = [
    "canlı çim üretimi",
    "canlı çim satışı",
    "suni çim satışı",
    "peyzaj uygulaması",
    "çim uygulaması",
    "çim döşeme",
]

# Hizmet bölgesi - İzmir merkez, Ege bölgesi ve güney Marmara (Antalya
# sınırına kadar). Bu şehirler geçen aramalar "hizmet bölgesi dışı şehir"
# olarak asla işaretlenmez, pozitif kabul edilir.
SERVICE_LOCATIONS = [
    "izmir", "antalya", "muğla", "aydın", "manisa", "çanakkale",
    "bursa", "denizli",
]

# Sunulmadığı bilinen, sıkça karıştırılabilecek hizmet/ürün türleri.
NOT_OFFERED_ACTIVITIES: list[str] = []

# Büyük şehirler (hizmet bölgesi hariç) - Güneydoğu, Ankara, Karadeniz ve
# İstanbul dahil, il/ilçe belirten aramalarda hizmet bölgesi dışı
# olabileceğini işaretlemek için kullanılır.
OTHER_MAJOR_CITIES = [
    "istanbul", "ankara", "adana", "konya", "gaziantep", "mersin",
    "kayseri", "eskişehir", "samsun", "trabzon", "rize", "ordu", "giresun",
    "diyarbakır", "şanlıurfa", "mardin", "van", "batman", "siirt",
    "kahramanmaraş", "malatya", "elazığ", "erzurum", "sivas",
    "kocaeli", "sakarya",
]

# Rakip firma isimleri - bu isimleri arayıp bizim reklamımıza tıklayanlar
# marka karşılaştırma trafiğidir, ASLA negatif işaretlenmez.
# İsimler öğrenildikçe buraya eklenecek.
COMPETITOR_NAMES: list[str] = []

# Dönemsel/sezonsal terimler - gerçek bir hizmet arayışı olabilir,
# ASLA negatif işaretlenmez.
SEASONAL_TERMS: list[str] = []

# Genel (base) junk kelimelere ek olarak bu hesaba özel eklenen kelimeler.
# Üretim süreci / kendin-yap (DIY) bilgi arayışı - satın almak değil,
# nasıl yapıldığını öğrenmek isteyenler gerçek müşteri değildir.
EXTRA_JUNK_TERMS: set[str] = {
    "nasıl yetiştirilir", "nasıl üretilir", "nasıl hasat edilir",
    "hasat makinesi", "hasat aleti", "biçme makinesi",
    "çim tohumu", "çimen tohumu",
    "çim nasıl ekilir", "çim ekimi nasıl yapılır", "çim nasıl biçilir",
    "çim ne zaman biçilir", "çim ne kadar sulanır", "çim nasıl sulanır",
    "çim bakımı nasıl yapılır",
}

# "ikinci el" / "second hand" zaten BASE_JUNK_TERMS içinde - bu hesap için
# ekstra bir istisna gerekmiyor (Çimenci ikinci el ürün satmıyor).
JUNK_TERM_EXCEPTIONS: set[str] = set()

# Satışla/kuruluma ilişkin gerçek talep - ASLA negatif işaretlenmez.
SALES_TERMS = [
    "canlı çim satış", "çim satış", "çim satın al", "çim fiyat",
    "çim fiyatları", "suni çim satış", "suni çim fiyat",
    "peyzaj uygulama", "çim uygulama", "çim döşeme",
]

REQUIRE_CONTEXT_TERMS: list[str] = []
CONTEXT_SIGNAL_TERMS: list[str] = []

# Yaş kısıtı bu hesap için geçerli değil.
MIN_TARGET_AGE_YEARS = None

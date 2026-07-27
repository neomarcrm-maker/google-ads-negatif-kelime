# Google Ads Negatif Anahtar Kelime Bulucu

Google Ads MCC hesabındaki müşteri hesaplarından arama terimi raporlarını API ile çeker,
düşük performanslı/alakasız terimleri negatif anahtar kelime adayı olarak listeler,
onayladığın terimleri tek tıkla gerçek hesaba negatif anahtar kelime olarak ekler.

## 1. Yerel kurulum ve test

```powershell
cd google-ads-negatif-kelime
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Proje kökünde bir `.env` dosyası oluştur (bu dosya asla commit edilmez):

```
DEVELOPER_TOKEN=...
GOOGLE_ADS_CLIENT_ID=...
GOOGLE_ADS_CLIENT_SECRET=...
GOOGLE_ADS_REFRESH_TOKEN=...
LOGIN_CUSTOMER_ID=...   # MCC ID, tire olmadan
APP_PASSWORD=sectigin-bir-parola
```

Ortam değişkenlerini yükleyip yerel sunucuyu başlat:

```powershell
Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*([^#=]+)=(.*)$') { [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim()) }
}
uvicorn app.main:app --reload
```

Tarayıcıda `http://localhost:8000` adresini aç, kullanıcı adı olarak istediğin bir şey (kontrol edilmiyor),
parola olarak `APP_PASSWORD` değerini gir.

## 2. GitHub'a push

```powershell
git init
git add .
git commit -m "İlk sürüm: Google Ads negatif kelime bulucu"
git branch -M main
git remote add origin https://github.com/<kullanici-adin>/google-ads-negatif-kelime.git
git push -u origin main
```

## 3. Render.com'da deploy

1. [render.com](https://render.com) üzerinde GitHub hesabınla giriş yap.
2. "New +" → "Web Service" → bu repoyu seç. `render.yaml` otomatik algılanır.
3. Environment sekmesinde şu değişkenleri gir (gerçek değerlerini kendi Google Ads/OAuth bilgilerinden al):
   - `DEVELOPER_TOKEN`
   - `GOOGLE_ADS_CLIENT_ID`
   - `GOOGLE_ADS_CLIENT_SECRET`
   - `GOOGLE_ADS_REFRESH_TOKEN`
   - `LOGIN_CUSTOMER_ID`
   - `APP_PASSWORD`
4. Deploy'u başlat. Render sana `https://google-ads-negatif-kelime.onrender.com` gibi bir link verecek.
5. Free plan'da servis 15 dakika kullanılmazsa uykuya geçer, ilk açılışta ~30 saniye gecikme olabilir.

## Nasıl çalışır

1. Dashboard'da MCC altındaki hesaplardan birini seç, tarih aralığını belirle.
2. "Analiz Et" butonuna bas — sistem gerçek arama terimi verisini Google Ads API'den çeker ve
   kural tabanlı filtrelerle (0 dönüşümle yüksek tıklama/maliyet, alakasız kelime eşleşmesi) negatif aday listesi çıkarır.
3. Eklemek istediğin terimleri işaretle, "Seçilenleri Negatif Olarak Ekle" butonuna bas.
4. Sistem önce bir doğrulama (dry-run, `validate_only=true`) yapar, sonra senin onayınla gerçek hesaba yazar.
   **Hiçbir zaman onayın olmadan otomatik yazma yapılmaz.**

## Kuralları ayarlama

`app/negative_rules.py` içindeki `JUNK_TERMS` listesini ve varsayılan eşikleri
(`DEFAULT_MIN_CLICKS_ZERO_CONV`, `DEFAULT_MIN_COST_ZERO_CONV`) ihtiyacına göre düzenleyebilirsin.
Eşikler dashboard üzerinden de analiz anında geçici olarak değiştirilebilir.

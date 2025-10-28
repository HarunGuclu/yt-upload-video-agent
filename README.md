# 🎬 YouTube Video Yükleme Sistemi

Python Flask tabanlı, Google OAuth 2.0 ile entegre bir YouTube video yükleme uygulaması.

**Available in:** [English](#-youtube-video-upload-system) | [Türkçe](#-youtube-video-yükleme-sistemi)

## 📋 Özellikler

✅ **Google OAuth 2.0 Kimlik Doğrulaması** - Güvenli Google hesabı entegrasyonu
✅ **YouTube Data API v3 Entegrasyonu** - Direkt YouTube kanalına video yükleme
✅ **Sürükle-Bırak Desteği** - Dosya seçimi için kolay drag-and-drop arayüzü
✅ **Video Metadata** - Başlık, açıklama ve etiketler ekleme
✅ **Video Gizlilik Seçenekleri** - Public, Unlisted, Private yükleme seçenekleri
✅ **Shorts Desteği** - Otomatik YouTube Shorts algılaması (60 saniye, dikey format)
✅ **Video Format Analizi** - Otomatik video çözünürlük, süre ve en-boy oranı tespiti
✅ **İlerleme Takibi** - Yükleme ilerleme çubuğu
✅ **Dosya Doğrulaması** - Dosya türü ve boyut kontrolü
✅ **Güvenli Oturum Yönetimi** - Session tabanlı kimlik doğrulama, zorunlu yeniden giriş
✅ **Türkçe Arayüz** - Tüm metin ve arayüz Türkçe

## 🛠️ Teknik Gereksinimler

- **Python:** 3.8+
- **Web Framework:** Flask 2.3+
- **Google Kütüphaneleri:** google-auth, google-auth-oauthlib, google-api-python-client
- **Video İşleme:** opencv-python, ffmpeg-python
- **Diğer:** python-dotenv

## 📁 Proje Yapısı

```
youtube-video-yukle/
├── app.py                          # Ana Flask uygulaması
├── templates/                      # HTML şablonları
│   ├── giris.html                  # Giriş sayfası
│   ├── giris_basarili.html         # Başarılı giriş sayfası
│   ├── video_yukle.html            # Video yükleme sayfası
│   ├── sonuc.html                  # Yükleme sonucu sayfası
│   ├── gizlilik.html               # Gizlilik politikası
│   └── hata.html                   # Hata sayfası
├── static/                         # Statik dosyalar
│   ├── css/
│   │   └── stil.css                # Ana stil dosyası
│   └── js/
│       └── yukle.js                # Video yükleme JavaScript
├── uploads/                        # Geçici dosya klasörü
├── .env                            # Ortam değişkenleri (GİZLİ)
├── .env.example                    # Ortam değişkenleri şablonu
├── .gitignore                      # Git yoksayılacak dosyalar
├── requirements.txt                # Python bağımlılıkları
├── client_secret.json              # Google API anahtarları (GİZLİ)
└── README.md                       # Bu dosya
```

## 🚀 Kurulum Adımları

### 1️⃣ Google Cloud Platform Ayarı

1. [Google Cloud Console](https://console.cloud.google.com) sayfasına gidin
2. Yeni bir proje oluşturun
3. YouTube Data API v3'ü etkinleştirin
4. OAuth 2.0 Kimlik Bilgileri (Web Uygulaması) oluşturun:
   - Yetkili JavaScript kaynaklarına ekleyin: `http://localhost:5000`
   - Yetkili yönlendirme URI'lerine ekleyin: `http://localhost:5000/oauth2callback`
5. JSON dosyasını indirin ve proje klasörüne `client_secret.json` olarak kaydedin

### 2️⃣ Sanal Ortam Oluşturma

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Bağımlılıkları Yükleme

```bash
pip install -r requirements.txt
```

### 4️⃣ Ortam Değişkenlerini Ayarlama

1. `.env.example` dosyasını kopyalayın ve `.env` olarak adlandırın:
```bash
cp .env.example .env
```

2. `.env` dosyasını düzenleyin ve değerleri doldurun:
```env
FLASK_SECRET_KEY=guclu_gizli_anahtar_koyun_buraya
FLASK_ENV=production
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
REDIRECT_URI=http://localhost:5000/callback
YOUTUBE_API_KEY=your_youtube_api_key_here
```

> ⚠️ **Güvenlik Uyarısı:** `.env` dosyasını asla Git'e yüklemeyin. `.gitignore` ile zaten korunuyor.

### 5️⃣ Uygulamayı Çalıştırma

```bash
python app.py
```

Tarayıcı otomatik olarak `http://localhost:5000` adresine açılacak.

Veya manuel olarak açın:
```
http://localhost:5000
```

## 📖 Kullanım Kılavuzu

### Adım 1: Giriş Yapın

1. Ana sayfada "Google ile Giriş Yap" düğmesine tıklayın
2. Google hesabınızı seçin
3. Uygulamaya YouTube kanalına erişim izni verin
4. Giriş başarılı mesajını göreceksiniz

### Adım 2: Video Dosyası Seçin

1. Video yükleme sayfasında video dosyasını seçin
2. Dosyayı sürükleyip bırakabilir veya tıklayarak seçebilirsiniz
3. Desteklenen formatlar: MP4, MOV, AVI, MKV, FLV, WMV, WebM
4. Maximum dosya boyutu: 5GB

### Adım 3: Video Bilgileri Ekleyin

1. **Video Başlığı** (isteğe bağlı): Video adını girin
2. **Video Etiketleri** (isteğe bağlı): Virgülle ayrılmış etiketler
3. **Video Açıklaması** (isteğe bağlı): Detaylı açıklama yazın

### Adım 4: Video Gizlilik Durumunu Seçin

Videonuzun kime görüneceğini belirleyin:

- 🌐 **Herkese Açık (Public)**: Video herkesin görebilmesi için açık olur
- 🔗 **Liste Dışı (Unlisted)**: Yalnızca linki olanlar görebilir
- 🔒 **Özel (Private)**: Yalnızca sen ve davet ettiğin kişiler görebilir

### Adım 5: Video Türünü Seçin

Videonuzun formatını belirleyin:

- 🤖 **Otomatik Seçim** (Önerilen): Sistem videonuzun özelliklerini analiz ederek otomatik seçer
- 📺 **Normal Video**: Uzun formatlı YouTube videosu (yatay format)
- ⚡ **YouTube Shorts**: Kısa formatlı video (60 saniye ve altı, dikey format)

**Shorts Kriterleri:**
- Video süresi: 60 saniye veya daha kısa
- Video formatı: Dikey (9:16 en-boy oranı)

### Adım 6: Yükleyin

1. "Yükle" düğmesine tıklayın
2. Yükleme ilerleme çubuğunu izleyin
3. Yükleme tamamlandığında:
   - Video ID'si
   - Video linki
   - Video tipi (Shorts/Normal)
   - Gizlilik durumu
   - Video analiz bilgileri (çözünürlük, süre, en-boy oranı)
4. "YouTube'da Aç" düğmesiyle hemen videonuza gidebilirsiniz

## 🔐 Güvenlik Özellikleri

- **OAuth 2.0**: Google'ın güvenli kimlik doğrulama sistemi
- **HTTPS**: Production ortamında HTTPS kullanılması önerilir
- **.env Dosyası**: Gizli anahtarlar ortam değişkenlerine kaydedilir
- **Session Şifrelemesi**: Flask session'ları güvenli olarak şifrelenir
- **CSRF Koruması**: State parametresi ile CSRF saldırıları engellenir
- **Dosya Doğrulaması**: Dosya türü ve boyutu kontrol edilir
- **Geçici Dosya Silme**: Yüklendikten sonra geçici dosyalar silinir

## 📝 API Endpoints

| Endpoint | Metod | Açıklama |
|----------|-------|----------|
| `/` | GET | Ana sayfa |
| `/giris` | GET, POST | Giriş sayfası ve OAuth başlatma |
| `/callback` | GET | OAuth callback endpoint |
| `/video-yukle` | GET | Video yükleme sayfası |
| `/upload-video` | POST | Video dosyasını yükle |
| `/video-yukle-basarili` | GET | Başarılı giriş sayfası |
| `/cikis` | GET | Oturumu kapat |
| `/gizlilik` | GET | Gizlilik politikası |

## 🐛 Sorun Giderme

### "client_secret.json bulunamadı" hatası

- Google Cloud Console'dan `client_secret.json` dosyasını indirdiğinizden emin olun
- Dosyayı proje ana klasörüne koyun

### "GOOGLE_CLIENT_ID bulunamadı" hatası

- `.env` dosyasını oluşturduğunuzdan emin olun
- Tüm gerekli değişkenleri doldurun

### Yükleme sırasında "403 Forbidden" hatası

- YouTube API'yi Google Cloud Console'da etkinleştirdiğinizi kontrol edin
- Kimlik bilgilerinin doğru olduğundan emin olun
- Quota limitini kontrol edin

### Video yüklenmiyor ancak hata vermiyor

- İnternet bağlantınızı kontrol edin
- Dosya boyutunu kontrol edin (max 5GB)
- YouTube'un dosya formatını destekleyip desteklemediğini kontrol edin

## 📚 Kütüphane Versiyonları

```
Flask==2.3.2
google-auth==2.23.0
google-auth-oauthlib==1.0.0
google-auth-httplib2==0.1.1
google-api-python-client==2.91.0
python-dotenv==1.0.0
Werkzeug==2.3.6
opencv-python==4.8.1.78
ffmpeg-python==0.2.1
```

## 🌐 Production Ortamı

Production ortamında çalıştırırken:

1. **Debug Modunu Kapatın**
```python
app.run(debug=False)
```

2. **HTTPS Kullanın**
- Let's Encrypt veya diğer SSL sertifikası kullanın

3. **Gunicorn Kullanın**
```bash
pip install gunicorn
gunicorn app:app
```

4. **Environment Ayarını Yapın**
```bash
export FLASK_ENV=production
export FLASK_SECRET_KEY=guclu_anahtarınız
```

5. **Database Kullanın** (isteğe bağlı)
- Oturum verilerini database'e kaydetmeyi düşünün

## 📞 İletişim ve Destek

Sorunlar veya öneriler için:
- GitHub Issues sayfasını açın
- Email gönderin

## 📄 Lisans

MIT Lisansı altında yayınlanmıştır.

## 🙏 Teşekkürler

- Google for OAuth 2.0 and YouTube API
- Flask for web framework
- Python community

---

**Yapılış Tarihi:** 2025
**Versiyon:** 1.0.0
**Son Güncelleme:** Ekim 2025

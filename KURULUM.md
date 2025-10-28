# 🚀 YouTube Video Yükleme Sistemi - Adım Adım Kurulum Rehberi

Bu rehber, YouTube Video Yükleme Sistemini ayaklandırmak için gereken tüm adımları açıklamaktadır.

## 📋 Ön Gereksinimler

- Python 3.8 veya üstü
- pip (Python paket yöneticisi)
- Google hesabı
- İnternet bağlantısı

## 🔑 ADIM 1: Google Cloud Platform Kurulumu

### 1.1 Google Cloud Projesi Oluşturma

1. Tarayıcınızda [Google Cloud Console](https://console.cloud.google.com) açın
2. **Proje Seç** butonuna tıklayın
3. **Yeni Proje** seçeneğine tıklayın
4. Proje adını girin: `YouTube Video Yukle`
5. **Oluştur** düğmesine tıklayın

### 1.2 YouTube Data API v3 Etkinleştirme

1. Google Cloud Console'da sağ üstteki arama kutusuna `YouTube Data API` yazın
2. **YouTube Data API v3** sonucuna tıklayın
3. **Etkinleştir** butonuna tıklayın
4. İşlem tamamlanana kadar bekleyin

### 1.3 OAuth 2.0 Kimlik Bilgileri Oluşturma

1. Soldaki menüden **Kimlik Bilgileri** seçeneğine tıklayın
2. **+ Kimlik Bilgileri Oluştur** butonuna tıklayın
3. **OAuth İstemcisi ID'si** seçeneğini seçin
4. Uygulamayı yapılandırması istenirse:
   - **Kullanıcı Onayı Ekranı** seçeneğine tıklayın
   - Kullanıcı türü olarak **Harici** seçin
   - **Oluştur** düğmesine tıklayın
5. Gerekli alanları doldurun:
   - **Uygulama Adı:** YouTube Video Yükleme Sistemi
   - **Kullanıcı Desteği E-postası:** E-mail adresiniz
6. **Kaydet ve Devam Et** düğmesine tıklayın

### 1.4 OAuth Onay Ekranı Yapılandırması

1. **Kapsam Ekle Veya Kaldır** butonuna tıklayın
2. Arama kutusuna `youtube.upload` yazın
3. `https://www.googleapis.com/auth/youtube.upload` seçin
4. **Güncelle** düğmesine tıklayın
5. **Test Kullanıcıları** bölümünde **Test Kullanıcısı Ekle** butonuna tıklayın
6. Kendi Google e-posta adresinizi ekleyin
7. **Kaydet** düğmesine tıklayın

### 1.5 Web Uygulaması Kimlik Bilgileri Oluşturma

1. **Kimlik Bilgileri** sayfasına geri dönün
2. **+ Kimlik Bilgileri Oluştur** butonuna tıklayın
3. **OAuth İstemcisi ID'si** seçin
4. Uygulama türü olarak **Web Uygulaması** seçin
5. Ad girin: `YouTube Video Yukle Localhost`
6. **Yetkili JavaScript kaynaklarına** tıklayın ve ekleyin:
   ```
   http://localhost:5000
   ```
7. **Yetkili yönlendirme URI'lerine** tıklayın ve ekleyin:
   ```
   http://localhost:5000/callback
   ```
8. **Oluştur** düğmesine tıklayın
9. Açılan pencerenin sağ tarafından **İndir** (JSON simgesi) düğmesine tıklayın

### 1.6 JSON Dosyasını Kaydetme

1. İndirilen JSON dosyasını açın
2. Dosyanın adını `client_secret.json` olarak değiştirin
3. Dosyayı proje klasörünün ana dizinine kopyalayın:
   ```
   C:\Users\guclh\Desktop\yt-load-video-agent\client_secret.json
   ```

## 🐍 ADIM 2: Python Ortamı Kurulumu

### 2.1 Sanal Ortam Oluşturma

Windows'ta:
```bash
# Proje klasörüne gidin
cd C:\Users\guclh\Desktop\yt-load-video-agent

# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı etkinleştirin
venv\Scripts\activate
```

macOS / Linux'ta:
```bash
cd ~/Desktop/yt-load-video-agent
python3 -m venv venv
source venv/bin/activate
```

### 2.2 Bağımlılıkları Yükleme

```bash
pip install -r requirements.txt
```

Kurulum sırasında aşağıdakiler yüklenecek:
- Flask: Web framework
- google-auth: Google kimlik doğrulaması
- google-auth-oauthlib: OAuth 2.0 desteği
- google-api-python-client: YouTube API istemcisi
- python-dotenv: Ortam değişkenleri
- opencv-python: Video işleme ve analiz
- ffmpeg-python: FFmpeg Python arayüzü

## ⚙️ ADIM 3: Ortam Değişkenlerini Ayarlama

### 3.1 .env Dosyasını Düzenleme

1. Metin editörü (VS Code, Notepad++ vb.) ile `.env` dosyasını açın
2. Aşağıdaki değerleri doldurun:

```env
FLASK_SECRET_KEY=youtube-video-yukle-gizli-anahtar-2025
FLASK_ENV=development
GOOGLE_CLIENT_ID=<client_secret.json'dan CLIENT_ID>
GOOGLE_CLIENT_SECRET=<client_secret.json'dan CLIENT_SECRET>
REDIRECT_URI=http://localhost:5000/oauth2callback
YOUTUBE_API_KEY=<YouTube API Key>
```

### 3.2 client_secret.json'dan Değerleri Kopyalama

1. İndirilen `client_secret.json` dosyasını açın
2. İçinde şu alanları bulun:
   - `"client_id"` - GOOGLE_CLIENT_ID'ye yapıştırın
   - `"client_secret"` - GOOGLE_CLIENT_SECRET'e yapıştırın

Örnek:
```json
{
  "installed": {
    "client_id": "123456789.apps.googleusercontent.com",
    "client_secret": "GOCSPX-1234567890abcdef",
    ...
  }
}
```

## ▶️ ADIM 4: Uygulamayı Çalıştırma

### 4.1 Flask Uygulamasını Başlatma

```bash
# Sanal ortamın aktif olduğundan emin olun
# Ardından uygulamayı çalıştırın
python app.py
```

Başarılı olursa, konsol çıktısı şuna benzer olacak:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: off
```

### 4.2 Tarayıcıda Açma

1. Tarayıcınızı açın
2. Adres çubuğuna yazın:
   ```
   http://localhost:5000
   ```
3. Giriş sayfası göründüğünde başarı!

## ✅ ADIM 5: İlk Testini Yapma

### 5.1 Google Hesabıyla Giriş

1. "Google ile Giriş Yap" butonuna tıklayın
2. Google hesabınızı seçin
3. Uygulamaya izin verdiğinizde, sonraki sayfaya yönlendirileceksiniz

### 5.2 Video Yükleme Testi

1. "Video Yükle Sayfasına Git" butonuna tıklayın
2. Küçük bir test videosu seçin (MP4 formatında)
3. Başlık ve açıklama ekleyin
4. "Yükle" butonuna tıklayın
5. Yükleme tamamlandığında video ID göreceksiniz

## 🔧 Sorun Giderme

### Sorun: "ModuleNotFoundError: No module named 'google'"

**Çözüm:**
```bash
# Sanal ortamın aktif olduğundan emin olun
# Ve bağımlılıkları yeniden yükleyin
pip install -r requirements.txt
```

### Sorun: "FileNotFoundError: client_secret.json"

**Çözüm:**
1. `client_secret.json` dosyasının proje ana klasöründe olduğundan emin olun
2. Dosya adının tam olarak `client_secret.json` olduğunu kontrol edin

### Sorun: "KeyError: 'GOOGLE_CLIENT_ID'"

**Çözüm:**
1. `.env` dosyasını oluşturduğunuzdan emin olun
2. Tüm gerekli değişkenlerin dolu olduğunu kontrol edin
3. Flask uygulamasını yeniden başlatın

### Sorun: "The redirect URI provided is invalid"

**Çözüm:**
1. Google Cloud Console'a gidin
2. Kimlik Bilgileri > OAuth 2.0 İstemcisini seçin
3. Yetkili yönlendirme URI'lerine `http://localhost:5000/oauth2callback` ekleyin

### Sorun: 403 Forbidden - YouTube API Hatası

**Çözüm:**
1. YouTube Data API'nin etkinleştirildiğini kontrol edin
2. Hesabın test kullanıcısı olarak eklendiğini kontrol edin
3. Quota limitini kontrol edin (API > Quotas)

## 📝 Sık Sorulan Sorular

### S: Uygulamayı başka bir bilgisayarda çalıştırmak istiyorum?

C: Aşağıdaki dosyaları kopyalayın ve `.env` dosyasını düzenleyin:
- app.py, templates/, static/, requirements.txt
- client_secret.json (bu gizli!)
- .env (değerleri güncelleyin)

### S: Production'a nasıl dağıtırım?

C: Bkz. README.md dosyasının "Production Ortamı" bölümü.

### S: Oturumum açılırsa, verilerim silinir mi?

C: Evet, oturumu kapatıldığında tüm session veriler silinir.

### S: Maksimum dosya boyutu ne?

C: 5 GB (0,000 MB)

## 📞 Destek

Sorunlar yaşıyorsanız:
1. README.md dosyasını kontrol edin
2. Google Cloud Console ayarlarını tekrar kontrol edin
3. Konsol hata mesajını okuyun

---

**Başarılı kurulum için iyi şanslar!** 🎉

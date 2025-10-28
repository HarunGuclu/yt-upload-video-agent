"""
YouTube Video Yükle Sistemi - Flask Uygulaması
Bu uygulama, kullanıcıların Google OAuth 2.0 ile kimlik doğrulaması yaparak
kendi YouTube kanallarına video yüklemelerini sağlar.
"""

import os
import json
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# .env dosyasından ortam değişkenlerini yükle
load_dotenv()

# Flask uygulaması başlat
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'guzli-anahtar-degistir')

# Google OAuth 2.0 Yapılandırması
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://127.0.0.1:5000/oauth2callback')
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly'
]


# Uploads klasörü
UPLOADS_FOLDER = 'uploads'
if not os.path.exists(UPLOADS_FOLDER):
    os.makedirs(UPLOADS_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5000  # 5GB


def kimli_degil_kontrol(f):
    """
    Oturum açmış olup olmadığını kontrol eden decorator.
    Kullanıcı oturum açmadıysa giriş sayfasına yönlendir.
    """
    @wraps(f)
    def oturumu_kontrol_et(*args, **kwargs):
        if 'credentials' not in session:
            return redirect(url_for('giris'))
        return f(*args, **kwargs)
    return oturumu_kontrol_et


def oauth_akisi_olustur():
    """
    Google OAuth 2.0 akışını oluştur.

    Returns:
        Flow: Google OAuth flow nesnesi
    """
    return Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )


@app.route('/')
def index():
    """Ana sayfa - oturum durumuna göre yönlendir"""
    if 'credentials' in session:
        return redirect(url_for('video_yukle'))
    return redirect(url_for('giris'))


@app.route('/giris', methods=['GET', 'POST'])
def giris():
    """
    Giriş sayfası ve Google OAuth başlatma.
    Kullanıcıyı Google hesabıyla kimlik doğrulamaya yönlendir.
    """
    if request.method == 'POST':
        # Google OAuth flow'unu başlat
        flow = oauth_akisi_olustur()
        authorization_url, state = flow.authorization_url()

        # State'i session'da sakla
        session['oauth_state'] = state

        return redirect(authorization_url)

    return render_template('giris.html')


@app.route('/oauth2callback')
def callback():
    """
    Google OAuth callback endpoint.
    Kullanıcı izin verdikten sonra buraya yönlendirilir.
    Credentials'ı session'da sakla.
    """
    # State kontrolü (CSRF koruması)
    state = session.get('oauth_state')
    if not state:
        return "Güvenlik hatası: State bulunamadı", 400

    # OAuth flow'unu yeniden oluştur
    flow = oauth_akisi_olustur()
    flow.fetch_token(authorization_response=request.url)

    # Credentials'ı al
    credentials = flow.credentials

    # Credentials'ı session'da sakla (JSON formatında)
    credentials_dict = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'expiry': credentials.expiry.isoformat() if credentials.expiry else None
    }
    session['credentials'] = credentials_dict

    # Kullanıcı bilgilerini al
    youtube = build('youtube', 'v3', credentials=credentials)
    channels = youtube.channels().list(part='snippet', mine=True).execute()

    if channels['items']:
        kullanici_adi = channels['items'][0]['snippet']['title']
        session['kullanici_adi'] = kullanici_adi

    return redirect(url_for('video_yukle_basarili'))


@app.route('/video-yukle-basarili')
def video_yukle_basarili():
    """Başarılı giriş sonrası mesaj göster"""
    if 'credentials' not in session:
        return redirect(url_for('giris'))

    return render_template('giris_basarili.html', kullanici_adi=session.get('kullanici_adi', 'Kullanıcı'))


@app.route('/video-yukle')
@kimli_degil_kontrol
def video_yukle():
    """Video yükleme sayfası"""
    return render_template('video_yukle.html')


@app.route('/sonuc')
@kimli_degil_kontrol
def sonuc():
    """Video yükleme sonuç sayfası"""
    return render_template('sonuc.html')


@app.route('/upload-video', methods=['POST'])
@kimli_degil_kontrol
def dosyayı_yukle():
    """
    Video dosyasını işle ve YouTube'a yükle.

    POST Parametreleri:
        - video_dosyasi: Video dosyası (multipart)
        - video_baslik: Video başlığı (isteğe bağlı)
        - video_aciklamasi: Video açıklaması (isteğe bağlı)
        - video_taglari: Video etiketleri (isteğe bağlı)

    Returns:
        JSON: Yükleme sonucu ve video ID'si
    """
    try:
        # Dosya kontrolü
        if 'video_dosyasi' not in request.files:
            return jsonify({'hata': 'Video dosyası seçilmedi'}), 400

        video_dosyasi = request.files['video_dosyasi']

        if video_dosyasi.filename == '':
            return jsonify({'hata': 'Dosya seçilmedi'}), 400

        # İzin verilen dosya türlerini kontrol et
        izin_verilen_uzantılar = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm'}
        dosya_uzantisi = os.path.splitext(video_dosyasi.filename)[1].lower()

        if dosya_uzantisi not in izin_verilen_uzantılar:
            return jsonify({'hata': f'Dosya türü desteklenmiyor. İzin verilen: {", ".join(izin_verilen_uzantılar)}'}), 400

        # Geçici dosya adı oluştur
        gecici_dosya_adi = f"temp_{int(datetime.now().timestamp())}_{video_dosyasi.filename}"
        dosya_yolu = os.path.join(app.config['UPLOAD_FOLDER'], gecici_dosya_adi)

        # Dosyayı kaydet
        video_dosyasi.save(dosya_yolu)

        # Video bilgilerini al
        video_baslik = request.form.get('video_baslik', 'Başlık Girilmedi')
        video_aciklamasi = request.form.get('video_aciklamasi', 'Açıklama girilmedi')
        video_taglari = request.form.get('video_taglari', '')

        # Etiketleri diziye dönüştür
        tag_listesi = [tag.strip() for tag in video_taglari.split(',') if tag.strip()] if video_taglari else []

        # Credentials'ı session'dan al
        credentials_dict = session['credentials']

        # Credentials nesnesini yeniden oluştur
        credentials = Credentials.from_authorized_user_info(credentials_dict, SCOPES)

        # YouTube API client'ı oluştur
        youtube = build('youtube', 'v3', credentials=credentials)

        # Video metadata'sını oluştur
        request_body = {
            'snippet': {
                'title': video_baslik,
                'description': video_aciklamasi,
                'tags': tag_listesi,
                'categoryId': '22'  # Varsayılan kategori: Diğer
            },
            'status': {
                'privacyStatus': 'public'  # Varsayılan olarak özel
            }
        }

        # Media dosyasını hazırla
        media = MediaFileUpload(dosya_yolu, chunksize=-1, resumable=True)

        # Video yükleme isteğini oluştur
        yükleme_isteği = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        )

        # Yüklemeyi gerçekleştir
        response = None
        while response is None:
            status, response = yükleme_isteği.next_chunk()

        video_id = response['id']

        # Geçici dosyayı sil (işlem başarılı olduktan sonra)
        try:
            # YouTube'a yükleme tamamlandıktan sonra dosyayı silmeye çalış
            # Başarısızsa, sistem daha sonra temizlemek için
            import time
            time.sleep(1)  # 1 saniye bekle
            os.remove(dosya_yolu)
        except PermissionError:
            # Dosya kilitli ise, yine de başarılı olarak döndür
            # Windows işletim sisteminde sık görülen bir durumdur
            print(f"Uyarı: Dosya hala kullanımda, daha sonra silinecek: {dosya_yolu}")
        except FileNotFoundError:
            # Dosya zaten silinmişse sorun yok
            pass
        except Exception as e:
            print(f"Dosya silme hatası: {e}")

        return jsonify({
            'basarili': True,
            'video_id': video_id,
            'video_linki': f'https://www.youtube.com/watch?v={video_id}'
        })

    except Exception as e:
        # Hata durumunda dosyayı temizle
        try:
            if 'dosya_yolu' in locals() and os.path.exists(dosya_yolu):
                os.remove(dosya_yolu)
        except:
            pass

        return jsonify({'hata': f'Yükleme hatası: {str(e)}'}), 500


@app.route('/cikis')
def cikis():
    """Oturumu kapat ve giriş sayfasına git"""
    session.clear()
    return redirect(url_for('giris'))


@app.route('/gizlilik')
def gizlilik():
    """Gizlilik politikası sayfası"""
    return render_template('gizlilik.html')


@app.errorhandler(404)
def sayfa_bulunamadi(e):
    """404 Hata Sayfası"""
    return render_template('hata.html', hata_kodu=404, mesaj='Sayfa bulunamadı'), 404


@app.errorhandler(500)
def sunucu_hatasi(e):
    """500 Hata Sayfası"""
    return render_template('hata.html', hata_kodu=500, mesaj='Sunucu hatası'), 500


if __name__ == '__main__':
    # Flask uygulamasını çalıştır
    # NOT: Production için Gunicorn veya buna benzer bir WSGI server kullanın
    app.run(debug=False, host='0.0.0.0', port=5000)

/*
   YouTube Video Yükleme Sistemi - JavaScript Dosyası
   Video yükleme formu işlevleri ve sürükle-bırak desteği
*/

// DOM Elemanlarını Seç
const formSunu = document.getElementById('yukle-formu');
const dropZone = document.getElementById('drop-zone');
const videoDosyasiInput = document.getElementById('video_dosyasi');
const dosyaBilgisiDiv = document.getElementById('dosya-bilgisi');
const dosyaAdiGoster = document.getElementById('dosya-adi-goster');
const dosyaBoyutuGoster = document.getElementById('dosya-boyutu-goster');
const iletisimMesaji = document.getElementById('durum-mesaji');
const iletisimCubugu = document.getElementById('ilerleme-cubugu');
const iletisimBari = document.getElementById('ilerleme-barı');
const yukleButonu = document.getElementById('yukle-btn');

// İzin Verilen Dosya Türleri
const izinVerilen = [
    'video/mp4',
    'video/quicktime',
    'video/x-msvideo',
    'video/x-matroska',
    'video/x-flv',
    'video/x-ms-wmv',
    'video/webm'
];

// Sürükle-Bırak Olaylarını Dinle
dropZone.addEventListener('click', () => {
    videoDosyasiInput.click();
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('dragover');

    // Bırakılan dosyaları al
    const dosyalar = e.dataTransfer.files;
    if (dosyalar.length > 0) {
        videoDosyasiInput.files = dosyalar;
        dosyaIslemesi(dosyalar[0]);
    }
});

// Dosya Seçim Olayı
videoDosyasiInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        dosyaIslemesi(e.target.files[0]);
    }
});

/**
 * Seçilen dosyayı işle ve doğrula
 * @param {File} dosya - Seçilen dosya
 */
function dosyaIslemesi(dosya) {
    // Dosya türünü kontrol et
    if (!izinVerilen.includes(dosya.type)) {
        mesajiGoster(
            `❌ Dosya türü desteklenmiyor: ${dosya.type}`,
            'hata'
        );
        videoDosyasiInput.value = '';
        dosyaBilgisiDiv.classList.remove('gosterilsin');
        return;
    }

    // Dosya boyutunu kontrol et (5GB)
    const maxBoyut = 5 * 1024 * 1024 * 1024; // 5GB
    if (dosya.size > maxBoyut) {
        mesajiGoster(
            '❌ Dosya çok büyük. Maximum 5GB olabilir.',
            'hata'
        );
        videoDosyasiInput.value = '';
        dosyaBilgisiDiv.classList.remove('gosterilsin');
        return;
    }

    // Dosya bilgisini göster
    dosyaBilgisiDiv.classList.add('gosterilsin');
    dosyaAdiGoster.textContent = `📹 ${dosya.name}`;
    dosyaBoyutuGoster.textContent = `Boyut: ${(dosya.size / (1024 * 1024)).toFixed(2)} MB`;

    mesajiGoster('✅ Dosya başarıyla seçildi. Başlık ve açıklama ekledikten sonra yükleyin.', 'bilgi');
}

/**
 * İstatistiksel mesaj göster
 * @param {string} metin - Gösterilecek metin
 * @param {string} tur - Mesaj türü: 'basarili', 'hata', 'bilgi'
 */
function mesajiGoster(metin, tur = 'bilgi') {
    iletisimMesaji.textContent = metin;
    iletisimMesaji.className = `durum-mesaji gosterilsin ${tur}`;

    // 5 saniye sonra mesajı gizle (hata veya başarı durumunda)
    if (tur !== 'bilgi') {
        setTimeout(() => {
            iletisimMesaji.classList.remove('gosterilsin');
        }, 5000);
    }
}

/**
 * İlerleme çubuğunun yüzdesini güncelle
 * @param {number} yuzde - İlerleme yüzdesi (0-100)
 */
function iletisimGuncelle(yuzde) {
    iletisimCubugu.classList.add('gosterilsin');
    iletisimBari.style.width = yuzde + '%';
}

/**
 * Form gönderme olayı
 */
formSunu.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Dosya kontrol et
    if (!videoDosyasiInput.files || videoDosyasiInput.files.length === 0) {
        mesajiGoster('❌ Lütfen video dosyası seçin.', 'hata');
        return;
    }

    // Yükleme düğmesini devre dışı bırak
    yukleButonu.disabled = true;
    yukleButonu.textContent = '⏳ Yükleniyor...';

    // İlerleme çubuğunu sıfırla
    iletisimGuncelle(0);
    mesajiGoster('📤 Video yükleme başladı...', 'bilgi');

    try {
        // FormData oluştur
        const formData = new FormData();
        formData.append('video_dosyasi', videoDosyasiInput.files[0]);
        formData.append('video_baslik', document.getElementById('video_baslik').value);
        formData.append('video_aciklamasi', document.getElementById('video_aciklamasi').value);
        formData.append('video_taglari', document.getElementById('video_taglari').value);
        formData.append('gizlilik_secenegi', document.querySelector('input[name="gizlilik_secenegi"]:checked').value);
        formData.append('video_tipi', document.querySelector('input[name="video_tipi"]:checked').value);

        // İlerleme takibi için XMLHttpRequest kullan
        const xhr = new XMLHttpRequest();

        // Upload ilerleme olayı
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const yuzde = Math.round((e.loaded / e.total) * 100);
                iletisimGuncelle(yuzde);

                // İlerleme mesajını güncelle
                if (yuzde < 100) {
                    mesajiGoster(`📤 Yükleniyor... %${yuzde}`, 'bilgi');
                }
            }
        });

        // Yükleme tamamlandı
        xhr.addEventListener('load', () => {
            if (xhr.status === 200) {
                try {
                    const sonuc = JSON.parse(xhr.responseText);

                    if (sonuc.basarili) {
                        // Session Storage'a video bilgilerini kaydet
                        sessionStorage.setItem('video_id', sonuc.video_id);
                        sessionStorage.setItem('video_linki', sonuc.video_linki);
                        sessionStorage.setItem('video_tipi', sonuc.video_tipi);
                        sessionStorage.setItem('gizlilik', sonuc.gizlilik);
                        if (sonuc.video_analiz) {
                            sessionStorage.setItem('video_analiz', JSON.stringify(sonuc.video_analiz));
                        }

                        // İlerleme çubuğunu %100 yap
                        iletisimGuncelle(100);
                        mesajiGoster('✅ Video başarıyla YouTube\'a yüklendi!', 'basarili');

                        // 2 saniye sonra sonuç sayfasına git
                        setTimeout(() => {
                            window.location.href = sonucUrl;
                        }, 2000);
                    } else {
                        mesajiGoster(`❌ Yükleme Hatası: ${sonuc.hata}`, 'hata');
                    }
                } catch (e) {
                    mesajiGoster('❌ Yanıt işlenirken hata oluştu.', 'hata');
                }
            } else {
                try {
                    const hata = JSON.parse(xhr.responseText);
                    mesajiGoster(`❌ Hata: ${hata.hata}`, 'hata');
                } catch (e) {
                    mesajiGoster('❌ Sunucu Hatası: ' + xhr.status, 'hata');
                }
            }

            // Yükleme düğmesini tekrar etkinleştir
            yukleButonu.disabled = false;
            yukleButonu.textContent = '⬆️ Yükle';

            // İlerleme çubuğunu gizle
            setTimeout(() => {
                iletisimCubugu.classList.remove('gosterilsin');
            }, 1500);
        });

        // Hata olayı
        xhr.addEventListener('error', () => {
            mesajiGoster('❌ Yükleme sırasında hata oluştu. Lütfen tekrar deneyin.', 'hata');

            // Yükleme düğmesini tekrar etkinleştir
            yukleButonu.disabled = false;
            yukleButonu.textContent = '⬆️ Yükle';

            // İlerleme çubuğunu gizle
            iletisimCubugu.classList.remove('gosterilsin');
        });

        // Yükleme isteğini gönder
        xhr.open('POST', uploadUrl); // HTML’den gelen değişkeni kullan
        xhr.send(formData);

       


    } catch (hata) {
        mesajiGoster(`❌ Hata: ${hata.message}`, 'hata');
        yukleButonu.disabled = false;
        yukleButonu.textContent = '⬆️ Yükle';
        iletisimCubugu.classList.remove('gosterilsin');
    }
});

// Sayfanın yüklenmesinden sonra, eğer varsa başarılı mesajını göster
document.addEventListener('DOMContentLoaded', () => {
    // Form varsayılan olarak temiz
    formSunu.reset();
    dosyaBilgisiDiv.classList.remove('gosterilsin');
});

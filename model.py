# HTTP istekleri (GET, POST vb.) yapmamızı sağlayan temel kütüphane
import requests

# Gelen yanıtı (response) işlemek ve JSON formatına çevirmek için kullanılır
import json

# API'den gelen Base64 formatındaki metin verisini gerçek bir resim dosyasına (.png) dönüştürmek için
import base64

# Hassas verileri (API Anahtarı gibi) ana kodun dışında tutmak için config dosyasından içe aktarıyoruz
from config import REVE_API_KEY

# API anahtarını değişkene atıyoruz (Güvenlik için doğrudan koda yazılmamalıdır)
REVE_API_KEY = REVE_API_KEY

# Oluşturulan görselin hangi isimle kaydedileceğini belirliyoruz
save_image = "sonuc.png"

# --- HTTP Header Yapılandırması ---
# Sunucuya kim olduğumuzu ve ne tür bir veri alışverişi yapacağımızı söyler
headers = {
    # 'Bearer' protokolü ile API anahtarımızı göndererek kimlik doğrulaması yapıyoruz
    "Authorization": f"Bearer {REVE_API_KEY}",

    # Sunucudan gelecek yanıtın JSON formatında olmasını beklediğimizi belirtiyoruz
    "Accept": "application/json",

    # Gönderdiğimiz isteğin gövdesinin (payload) JSON formatında olduğunu bildiriyoruz
    "Content-Type": "application/json"
}

# --- İstek Gövdesi (Payload) ---
# Yapay zekaya ne yapması gerektiğini söylediğimiz talimatlar listesi
payload = {
    # Yapay zekanın çizeceği sahneyi betimleyen metin (Prompt)
    "prompt": "a peaceful view of Mount Fuji",

    # Görselin boyut oranı (16:9 sinematik/geniş ekran demektir)
    "aspect_ratio": "16:9",

    # Kullanılacak yapay zeka modelinin sürümü
    "version": "latest"
}

# --- API İsteği ve Hata Yönetimi ---
try:
    # Belirtilen adrese POST isteği gönderiyoruz (Başlıklar ve veri ile birlikte)
    response = requests.post("https://api.reve.com/v1/image/create", headers=headers, json=payload)
    
    # Eğer sunucu 4xx veya 5xx gibi hata kodları dönerse burada hata fırlatılır
    response.raise_for_status()

    # Sunucudan gelen ham yanıtı Python sözlüğü (dict) yapısına çeviriyoruz
    result = response.json()
    
    # API'den gelen işlem bilgilerini konsola yazdırıyoruz
    print(f"İstek ID: {result['request_id']}")
    print(f"Harcanan Kredi: {result['credits_used']}")
    print(f"Kalan Kredi: {result['credits_remaining']}")

    # Eğer gelen verinin içinde 'image' anahtarı varsa görsel işleme başlıyoruz
    if result.get("image"):
        try:
            # Base64 formatındaki uzun metin dizisini ikili (binary) veri paketine çözüyoruz
            image_data = base64.b64decode(result["image"])

            # Belirlediğimiz dosya isminde yeni bir dosya açıyoruz ('wb' = write binary / ikili yazma modu)
            if save_image:
                with open(save_image, "wb") as img_file:
                    img_file.write(image_data) # İkili veriyi dosyaya yazarak resmi oluşturuyoruz

                print(f"Görsel şuraya kaydedildi: {save_image}")
        except Exception as e:
            # Görsel çözülürken veya kaydedilirken bir hata oluşursa yakalıyoruz
            print(f"Base64 görseli çözümleme başarısız: {e}")

    # İçerik politikası ihlali (uygunsuz içerik vb.) kontrolü
    if result.get('content_violation'):
        print("Uyarı: İçerik politikası ihlali tespit edildi!")
    else:
        print("Görsel başarıyla oluşturuldu!")

# Ağ bağlantısı, zaman aşımı veya geçersiz URL gibi HTTP hatalarını yakalar
except requests.exceptions.RequestException as e:
    print(f"İstek başarısız oldu: {e}")

# Sunucudan gelen veri JSON formatında değilse (beklenmedik bir yanıt) bu hata çalışır
except json.JSONDecodeError as e:
    print(f"Yanıt ayrıştırılamadı (JSON hatası): {e}")

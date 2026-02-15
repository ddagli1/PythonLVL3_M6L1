# HTTP istekleri (POST, GET vb.) göndermek için kullanılan kütüphane
import requests

# JSON verilerini okumak, yazmak ve işlemek için kullanılan standart kütüphane
import json

# API'den gelen metin tabanlı (Base64) görsel verisini resim dosyasına (.png) çevirmek için
import base64

# API anahtarı gibi gizli kalması gereken verileri 'config.py' dosyasından içe aktarır
from config import REVE_API_KEY

# İçe aktarılan API anahtarını yerel bir değişkene atar
REVE_API_KEY = REVE_API_KEY

# --- Global HTTP Başlıkları (Headers) ---
# API sunucusuna kimlik doğrulaması ve veri tipi bilgilerini gönderir
headers = {
    # Bearer Token yöntemi ile yetkilendirme sağlar
    "Authorization": f"Bearer {REVE_API_KEY}",
    # Sunucudan JSON formatında yanıt beklediğimizi belirtir
    "Accept": "application/json",
    # Sunucuya gönderdiğimiz verinin JSON formatında olduğunu bildirir
    "Content-Type": "application/json"
}

def generate_reve_image(prompt, aspect_ratio="16:9", version="latest", save_json="reve_output.json", save_image="reve_image.png"):
    """
    REVE API kullanarak metinden görsel oluşturan ana fonksiyon.
    :param prompt: Görselin açıklaması
    :param aspect_ratio: Görselin boyutu (örneğin 1:1, 16:9)
    :param version: Kullanılacak model sürümü
    :param save_json: Yanıtın kaydedileceği JSON dosya adı
    :param save_image: Görselin kaydedileceği dosya adı
    """

    # API'ye gönderilecek veri paketini (body) hazırlar
    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "version": version
    }

    try:
        # Belirtilen uç noktaya (endpoint) POST isteği atar
        response = requests.post(
            "https://api.reve.com/v1/image/create",
            headers=headers,
            json=payload
        )
        # Eğer HTTP kodu 400 veya 500 serisindeyse hata fırlatır
        response.raise_for_status()

        # Sunucudan gelen ham yanıtı Python sözlüğüne dönüştürür
        result = response.json()

        # --- JSON Yanıtını Kaydetme ---
        # Eğer bir dosya adı verilmişse, API'den gelen tüm ham veriyi dosyaya yazar
        if save_json:
            with open(save_json, "w") as f:
                # indent=4 parametresi dosyanın daha okunabilir (girintili) olmasını sağlar
                json.dump(result, f, indent=4)

        # Kullanıcıyı işlem detayları hakkında bilgilendirir
        print(f"Request ID: {result.get('request_id')}")
        print(f"Kullanılan kredi: {result.get('credits_used')}")
        print(f"Kalan kredi: {result.get('credits_remaining')}")

        # --- Görsel İşleme ---
        # Yanıt içerisinde 'image' anahtarı (Base64 verisi) varsa işleme başlar
        if result.get("image"):
            try:
                # Metin formatındaki görsel verisini ikili (binary) veriye geri döndürür
                image_data = base64.b64decode(result["image"])

                # Belirtilen dosya isminde yeni bir dosya oluşturur ve veriyi içine yazar
                if save_image:
                    with open(save_image, "wb") as img_file:
                        img_file.write(image_data)

                print(f"Görsel şuraya kaydedildi: {save_image}")
            except Exception as e:
                # Base64 dönüşümü sırasında oluşabilecek hataları yakalar
                print(f"Base64 görseli çözümleme başarısız: {e}")

        # --- Güvenlik Filtresi Kontrolü ---
        # API'nin içerik politikasına takılıp takılmadığını kontrol eder
        if result.get("content_violation"):
            print("Uyarı: İçerik politikası ihlali tespit edildi")
        else:
            print("Görsel başarıyla oluşturuldu")

        # İşlem sonucunu fonksiyonun çağrıldığı yere döndürür
        return result

    # İnternet hatası, timeout veya hatalı URL durumlarını yakalar
    except requests.exceptions.RequestException as e:
        print(f"İstek başarısız oldu: {e}")
        return None
    # Sunucudan gelen veri beklenen JSON formatında değilse yakalar
    except json.JSONDecodeError as e:
        print(f"Yanıt ayrıştırılamadı: {e}")
        return None

# --- Uygulama Kısmı ---
# Fonksiyonu bir örnek prompt ile çağırıyoruz
result = generate_reve_image("A serene mountain with a bear")

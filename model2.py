import requests
import json
import base64
from config import REVE_API_KEY

REVE_API_KEY = REVE_API_KEY

headers = {
    "Authorization": f"Bearer {REVE_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def generate_reve_image(prompt, aspect_ratio="16:9", version="latest", save_json="reve_output.json",save_image="reve_image.png"):
    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "version": version
    }

    try:
        response = requests.post(
            "https://api.reve.com/v1/image/create",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        result = response.json()

        # JSON yanıtını kaydet
        if save_json:
            with open(save_json, "w") as f:
                json.dump(result, f, indent=4)

        print(f"Request ID: {result.get('request_id')}")
        print(f"Kullanılan kredi: {result.get('credits_used')}")
        print(f"Kalan kredi: {result.get('credits_remaining')}")

        # Base64 görseli PNG'ye dönüştür
        if result.get("image"):
            try:
                image_data = base64.b64decode(result["image"])

                if save_image:
                    with open(save_image, "wb") as img_file:
                        img_file.write(image_data)

                print(f"Görsel şuraya kaydedildi: {save_image}")
            except Exception as e:
                print(f"Base64 görseli çözümleme başarısız: {e}")

        if result.get("content_violation"):
            print("Uyarı: İçerik politikası ihlali tespit edildi")
        else:
            print("Görsel başarıyla oluşturuldu")

        return result

    except requests.exceptions.RequestException as e:
        print(f"İstek başarısız oldu: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Yanıt ayrıştırılamadı: {e}")
        return None


# Fonksiyon çağrımı örneği
result = generate_reve_image("A serene mountain with a bear")

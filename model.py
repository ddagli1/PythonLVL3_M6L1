# HTTP istekleri yapmak için kullanılır (POST, GET vs.)
import requests

# JSON verisiyle çalışmak için (response.json() vb.)
import json

# Base64 formatındaki görüntüyü gerçek binary image'a çevirmek için
import base64
from config import REVE_API_KEY

REVE_API_KEY = REVE_API_KEY
save_image="sonuc.png"


# HTTP header'ları: Header yanlışsa API seni direkt reddeder.
headers = {
    # API kimlik doğrulaması
    "Authorization": f"Bearer {REVE_API_KEY}",

    # Sunucuya "JSON bekliyorum" diyorsun
    "Accept": "application/json",

    # Sunucuya "JSON gönderiyorum" diyorsun
    "Content-Type": "application/json"
}

# API'ye gönderilecek istek gövdesi (body). Prompt ne kadar netse, çıkan görüntü o kadar kontrol edilebilir olur.
# “Serene” gibi soyut kelimeler modelin keyfine kalır.
payload = {
    # Görselin ne olacağını tarif eden prompt
    "prompt": "a peaceful view of Mount Fuji",

    # Görsel oranı (16:9 = widescreen)
    "aspect_ratio": "16:9",

    # Modelin hangi versiyonu kullanılacak
    "version": "latest"
}


# Make the API request
try:
    response = requests.post("https://api.reve.com/v1/image/create", headers=headers, json=payload)
    response.raise_for_status()  # Raises an HTTPError for bad responses

    # Parse the response
    result = response.json()
    print(f"Request ID: {result['request_id']}")
    print(f"Credits used: {result['credits_used']}")
    print(f"Credits remaining: {result['credits_remaining']}")
    if result.get("image"):
            try:
                image_data = base64.b64decode(result["image"])

                if save_image:
                    with open(save_image, "wb") as img_file:
                        img_file.write(image_data)

                print(f"Görsel şuraya kaydedildi: {save_image}")
            except Exception as e:
                print(f"Base64 görseli çözümleme başarısız: {e}")

    if result.get('content_violation'):
        print("Warning: Content policy violation detected")
    else:
        print("Image generated successfully!")
        # The base64 image data is in result['image']
    


except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except json.JSONDecodeError as e:
    print(f"Failed to parse response: {e}")	

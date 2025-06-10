import requests
from bs4 import BeautifulSoup
from instagrapi import Client
import random
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips

# Instagram hesap bilgileri
INSTAGRAM_USERNAME = 'kulanıcı adıı'
INSTAGRAM_PASSWORD = 'şifre'

# Instagram client
insta_client = Client()

# Pinterest'ten fotoğrafları çekme
def fetch_pinterest_images(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        images = soup.find_all('img', {'src': True})
        image_urls = []
        for img in images:
            src = img['src']
            if '236x' in src:
                image_urls.append(src.replace('236x', 'originals'))
        return image_urls
    else:
        print("Pinterest sayfasına erişilemedi, status code:", response.status_code)
        return None

# Rastgele bir görseli indirme
def download_image(image_url):
    img_response = requests.get(image_url)
    if img_response.status_code == 200:
        image_path = 'downloaded_image.jpg'
        with open(image_path, 'wb') as f:
            f.write(img_response.content)
        return image_path
    else:
        print("Görsel indirilemedi, status code:", img_response.status_code)
        return None

# Kitaptan rastgele bir alıntı seçme
def get_random_quote():
    with open('c:/Users/USER/Desktop/wordpress_sites/emil.cioran.txt.txt', 'r', encoding='utf-8') as file:
        quotes = file.readlines()
    return random.choice(quotes).strip()

# Reels videosu oluşturma
def create_reels_video(image_paths, quotes, duration=5):
    clips = []
    for image_path, quote in zip(image_paths, quotes):
        image_clip = ImageClip(image_path).set_duration(duration)
        text_clip = TextClip(quote, fontsize=24, color='white', font='Arial-Bold', size=image_clip.size)
        text_clip = text_clip.set_position(('center', 'bottom')).set_duration(duration)
        final_clip = CompositeVideoClip([image_clip, text_clip])
        clips.append(final_clip)
    video = concatenate_videoclips(clips, method="compose")
    video_path = "reels_video.mp4"
    video.write_videofile(video_path, codec='libx264', fps=24)
    return video_path

# Ana fonksiyon
def main():
    try:
        insta_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        url = 'https://tr.pinterest.com/nichauschomen/cioran/'  # Değiştirmeniz gerekebilir
        image_urls = fetch_pinterest_images(url)
        if image_urls:
            image_paths = []
            quotes = []
            for _ in range(2):  # İki kez paylaşım yapmak için
                image_url = random.choice(image_urls)
                image_path = download_image(image_url)
                if image_path:
                    quote = get_random_quote()
                    image_paths.append(image_path)
                    quotes.append(quote)
                    caption = quote
                    insta_client.photo_upload(image_path, caption)
                    print("Gönderi başarıyla Instagram'da paylaşıldı!")
                else:
                    print("Görsel indirilemedi, gönderi başarısız oldu.")
            
            if image_paths:
                video_path = create_reels_video(image_paths, quotes)
                insta_client.video_upload(video_path, caption="Cioran Alıntıları")
                print("Reels video başarıyla Instagram'da paylaşıldı!")
        else:
            print("Görseller alınamadı, gönderi başarısız oldu.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == '__main__':
    main()

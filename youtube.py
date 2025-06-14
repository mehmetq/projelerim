import requests
import random
import os
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Pixabay API Anahtarı
API_KEY = 'api'

# YouTube API Kimlik doğrulaması için kapsamlar
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# 1. Adım: Pixabay'dan rastgele video indirme
def get_random_pixabay_video():
    url = f'https://pixabay.com/api/videos/?key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if 'hits' in data:
        videos = data['hits']
        random_video = random.choice(videos)
        video_url = random_video['videos']['medium']['url']
        video_title = random_video['tags'].replace(' ', '_')
        
        # Video indirme işlemi
        video_data = requests.get(video_url).content
        video_filename = f'{video_title}.mp4'
        with open(video_filename, 'wb') as video_file:
            video_file.write(video_data)
        
        print(f'Video indirildi: {video_filename}')
        return video_filename
    else:
        print("Video bulunamadı!")
        return None

# 2. Adım: YouTube API ile Kimlik Doğrulama
def authenticate_youtube():
    creds = None
    if os.path.exists('C:/Users/saydu/OneDrive/Desktop/erişilemez/token.json'):
        creds = Credentials.from_authorized_user_file('C:/Users/saydu/OneDrive/Desktop/erişilemez/token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('C:/Users/saydu/OneDrive/Desktop/erişilemez/client_secret_424025243232-m60hc7n6m5r6c9pljt7alq5vs39l965n.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('youtube', 'v3', credentials=creds)

# 3. Adım: YouTube'a video yükleme
def upload_video_to_youtube(youtube, file_name):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Pixabay Video",
                "description": "Automatically uploaded video from Pixabay.",
                "tags": ["Pixabay","Video"],
                "categoryId": "22"  # Kategori: 'Eğlence' (isteğe bağlı)
            },
            "status": {
                "privacyStatus": "public"  # Video herkese açık olacak
            }
        },
        media_body=MediaFileUpload(file_name)
    )
    response = request.execute()
    print(f"Video yüklendi: https://www.youtube.com/watch?v={response['id']}")

# 4. Adım: Botun döngü şeklinde çalışması (her 30 dakikada bir)
def main():
    youtube = authenticate_youtube()
    
    while True:
        video_filename = get_random_pixabay_video()
        
        if video_filename:
            upload_video_to_youtube(youtube, video_filename)
        
        print("5 saniye bekleniyor...")
        time.sleep(5)  # 5 saniye bekle

if __name__ == "__main__":
    main()

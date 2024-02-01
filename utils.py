import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import os

def parse_youtube_url(url):
    # URL'yi parçala
    parsed_url = urlparse(url)
    
    # YouTube domainine ve video ID'sine bak
    if parsed_url.netloc == 'www.youtube.com' or parsed_url.netloc == 'youtube.com':
        if parsed_url.path == '/watch':
            # URL'den video ID'sini al
            video_id = parse_qs(parsed_url.query)['v'][0]
            return True
        else:
            # Geçersiz YouTube URL'si
            return None
    elif parsed_url.netloc == 'youtu.be':
        # Kısa YouTube URL'si durumu
        video_id = parsed_url.path[1:]  # Başındaki /'yi kaldır
        return video_id
    else:
        # YouTube dışı URL
        return None   
    
def input_type_control(path):
    if path.endswith(('.mp3', '.ogg', '.wav')):
        print("Ses dosyası bulundu.")
        return 0
    elif path.endswith(('.mp4', '.webm')):
        print("video dosyası bulundu.")
        return 1
    else:
        if parse_youtube_url(path):
            print("youtube videosu.")
            return 2
        else:
            print("Geçersiz Url.")
            return None
        
def create_folder_if_not_exist(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
def load_text(file_path):
    with open(file_path, 'r') as file:
        return file.read()
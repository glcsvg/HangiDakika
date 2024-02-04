import os
import subprocess
import uuid
import openai
import zeyrek
from fuzzywuzzy import fuzz
import nltk
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import os


nltk.download("punkt")

class VideoProcessor:
    """
    Video dosyalarını işlemek için kullanılan sınıf.
    Bu sınıf, video dosyalarından ses çıkarma, transkript oluşturma ve
    morfolojik analiz gibi işlevleri içerir.
    """
    def __init__(self, openai_api_key):
        """
        VideoProcessor sınıfının kurucu metodudur. OpenAI API anahtarını alır.

        Args:
            openai_api_key (str): OpenAI API kullanımı için gerekli olan API anahtarı.
        """
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key


    
    def create_folder_if_not_exist(self,folder_path):
        """
        Verilen yolda bir klasör oluşturur eğer klasör mevcut değilse.
        
        Parameters:
        - folder_path: Klasörün oluşturulacağı yol (string).
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


    def generate_random_filename(self):
        """
        Benzersiz bir dosya adı oluşturur.

        Parameters:
        - extension: Oluşturulan dosya adının uzantısı (string). Örneğin, '.mp3'.

        Returns:
        - filename: Benzersiz dosya adı ve uzantısı ile birlikte (string).
        """
        random_uuid = uuid.uuid4()  # Benzersiz bir UUID oluştur
        filename = str(random_uuid)  # UUID'yi string'e çevir ve uzantıyı ekle
        return filename
    

    def extract_audio_mp3(self, input_video):
        """
        Verilen video dosyasından sesi çıkarır ve MP3 formatında kaydeder.

        Args:
            input_video (str): Sesin çıkarılacağı video dosyasının yolu.

        Returns:
            str: Oluşturulan MP3 dosyasının yolu.
        """
        output_folder = "./morpho"
        self.create_folder_if_not_exist(output_folder)
        randomfilename = self.generate_random_filename()
        output_audio_path = os.path.join(output_folder, f"{randomfilename}temp32.mp3")

        command = [
            "ffmpeg",
            "-i", input_video,
            "-vn",  # Sadece sesi çıkar
            "-acodec", "libmp3lame",  # MP3 formatında kodlama
            "-ab", "32k",  # Bit hızı 32 kbps
            output_audio_path
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Ses dosyası başarıyla oluşturuldu: {output_audio_path}")
            return output_audio_path
        except subprocess.CalledProcessError as e:
            print(f"Ses dosyası çıkarılırken bir hata oluştu: {e}")
            return None
    
    def get_video_transcript(self, input_video, language="tr"):
        """
        Verilen video dosyasından sesi çıkarır, ses dosyasını transkribe eder ve
        elde edilen transkripsiyonu döndürür.

        Args:
            input_video (str): Transkribe edilecek video dosyasının yolu.
            language (str): Transkripsiyonun yapılacağı dil. Varsayılan olarak Türkçe ('tr').

        Returns:
            dict: Transkripsiyon sonucunu içeren sözlük.
        """
        audio_path = self.extract_audio_mp3(input_video)
        if not audio_path:
            print("Ses dosyası çıkarılamadı.")
            return None

        try:
            file = open(audio_path, "rb")
            transcription_response = openai.Audio.transcribe("whisper-1", file,response_format="verbose_json",language="tr")
            return transcription_response
        except Exception as e:
            print(f"Transkripsiyon sırasında bir hata oluştu: {e}")
            return None
        

    def morpho_analysis(self, input_path):
        """
        Verilen transkripsiyon metninin morfolojik analizini gerçekleştirir ve
        her segmentin başlangıç ve bitiş zamanlarını içerir.

        Args:
            transcription (dict): `get_video_transcript` metodundan elde edilen transkripsiyon.
                                   Transkripsiyon, zaman damgaları ve metin içeren segmentlerden oluşur.

        Returns:
            list: Morfolojik analiz sonuçlarını ve zaman damgalarını içeren liste.
                  Her bir liste elemanı bir sözlük olup, 'start', 'end', 'text' ve 'analysis'
                  anahtarlarına sahiptir.
        """
        analyzer = zeyrek.MorphAnalyzer()
        morpho_results = []

        transcription = self.get_video_transcript(input_path)
        for segment in transcription['segments']:
            text = str(segment.get('text', ''))
            start = str(segment.get('start', 0))  # Segmentin başlangıç zamanı
            end = str(segment.get('end', 0))  # Segmentin bitiş zamanı
            analyzed_text = analyzer.lemmatize(text)
            morpho_results.append({
                'start': start,
                'end': end,
                'text': text,
                'analysis': analyzed_text
            })
        return morpho_results
    

    def word_finder_with_morpho_analysis(self, word, input_video, language="tr", threshold=65):
        """
        Verilen kelimenin video transkripsiyonundaki morfolojik analiz sonuçları üzerinden arar.
        Ayrıca, her eşleşmenin önceki ve sonraki metinlerini de içerir.

        Args:
            word (str): Aranacak kelime veya ifade.
            input_video (str): Aramanın yapılacağı video dosyasının yolu.
            language (str): Transkripsiyonun yapılacağı dil. Varsayılan olarak Türkçe ('tr').
            threshold (int): Eşleşme için minimum benzerlik oranı. Varsayılan değer 65'tir.

        Returns:
            list: Kelimenin morfolojik analiz sonuçları üzerinden benzerlik oranına göre bulunduğu
                  segmentlerin listesi. Her segment, 'previous_text', 'current_text', 'next_text',
                  'start', 'end', ve 'similarity' anahtarlarına sahiptir.
        """
        # Morfolojik analizi elde ediyoruz.
       
    
        morpho_results = self.morpho_analysis(input_video)
        
        found_segments = []
        for i, result in enumerate(morpho_results):
            # Morfolojik analiz sonucunu düz metne çeviriyoruz.
            analyzed_text = " ".join([t[0] for t in result['analysis']])
            similarity = fuzz.partial_ratio(word.lower(), result["text"].lower())
            print(result["text"])
            if similarity >= threshold:
                previous_text = morpho_results[i - 1]['text'] if i > 0 else ""
                next_text = morpho_results[i + 1]['text'] if i < len(morpho_results) - 1 else ""
                found_segments.append({
                    'kelime': word,
                    'previous_text': previous_text,
                    'current_text': result['text'],
                    'next_text': next_text,
                    'start': result['start'],
                    'similarity': similarity
                })
        if not found_segments:
            return "Kelime Bulunamadı"
        
        return found_segments
    

    def translate_transcription(self, input_video, target_language):
        """
        Video transkripsiyonunu belirli bir dile çevirir.

        Args:
            input_video (str): Çevirisi yapılacak video dosyasının yolu.
            target_language (str): Hedef dil.

        Returns:
            str: Çevrilen transkripsiyon metni.
        """
        # Morfolojik analizi yap
    
        morpho_results = self.morpho_analysis(input_video)
        
        # Morfolojik analiz sonuçlarını bir metin haline getir
        documents_text = " ".join([segment['text'] for segment in morpho_results])
        
        # OpenAI API kullanarak çeviri yap
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "You are an AI assistant that translates in multiple languages"},
            {"role": "assistant", "content": "data is stored in dataframe {start:'', end:'', text:''} and you just give me a translated json document"},
            {"role": "assistant", "content": str(documents_text)},
            {"role": "user", "content": "Translate the document I gave you into " + target_language}
        ]
        )
        
        # Çeviri sonucunu döndür
        translated_text = response.choices[0].message["content"] if response.choices else "Translation failed."
        return translated_text
    

    def get_subtext(self,input_video):
        """
        Verilen video dosyasının transkripsiyonundan bölümlere ayrılmış özet bilgileri çıkarır.
        
        Bu fonksiyon, videoyu 6 dakikalık bölümlere ayırır ve her bölüm için konu, başlangıç, bitiş
        zamanları ve anahtar kelimeleri tespit eder. OpenAI'nin GPT-3.5 modeli kullanılarak, 
        transkripsiyon metni üzerinden bu bilgiler çıkarılır ve Türkçe olarak sunulur.
        
        Args:
            input_video (str): Analiz edilecek video dosyasının yolu.
        
        Returns:
            list: Her bir bölüm için çıkarılan bilgileri içeren liste. Her bir liste elemanı, 
                bir bölümün konusu, başlangıç ve bitiş zamanları ile anahtar kelimelerini içeren 
                bir sözlük yapısındadır.
                
        Örnek Çıktı Yapısı:
            [
                {
                    'KONU': 'Giriş bölümü',
                    'BAŞLANGIÇ': '00:00',
                    'BİTİŞ': '06:00',
                    'ANAHTAR KELİMELER': ['giriş', 'özet', 'ana fikir']
                },
                ...
            ]
        """
        # Transkripsiyonu ve morfolojik analizi elde et
        documents = self.morpho_analysis(input_video)
        
        # OpenAI API ile transkripsiyonun özetini oluştur
        prompt = """
        Language: Turkish

        You are a database computer.You need to convert them to minutes. For example: start: 126 to start: 02.06. You have to answer only in Turkish language
        Divide the video into 6-minute parts and give the topic, beginning, end and keywords of the relevant parts.
        You only need to provide the following information.

        KONU:
        BAŞLANGIÇ:
        BİTİŞ:
        ANAHTAR KELİMELER:



        """

        query = """

        KONU:
        BAŞLANGIÇ:
        BİTİŞ:
        ANAHTAR KELİMELER:

        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
            {"role": "system", "content": prompt},
            {"role": "assistant", "content": "data is stored in JSON {start:'', end:'', text:''} and start and end times are given in seconds. You need to convert them to minutes. For example: start: 126 to start: 02.06.  Provide start time codes in minitues and seconds, also end time in minutes and seconds. Explain in Turkish"},
            {"role": "assistant", "content": str(documents)},
            {"role": "user", "content": query}
        ]
        )
        
        # Elde edilen özeti işle ve çıktıyı hazırla
        subtext = response.choices[0].message["content"]
        entries = subtext.strip().split("\n\n")
        parsed_entries = []
        for entry in entries:
            lines = entry.strip().split("\n")
            entry_dict = {line.split(": ", 1)[0]: line.split(": ", 1)[1] for line in lines}
            parsed_entries.append(entry_dict)
        print(parsed_entries)
        return parsed_entries
    

    def clip(input_file, output_file, start_time, end_time):
        """
        Verilen giriş dosyasının belirtilen zaman aralığını kesip yeni bir çıktı dosyasına kaydeder.

        Args:
            input_file (str): Kesilecek orijinal dosyanın yolu. Ses (.mp3, .wav) veya video (.mp4, .avi, .mov) formatında olabilir.
            output_file (str): Kesilen segmentin kaydedileceği dosyanın yolu.
            start_time (int): Kesilmek istenen segmentin başlangıç zamanı (milisaniye cinsinden).
            end_time (int): Kesilmek istenen segmentin bitiş zamanı (milisaniye cinsinden).

        Returns:
            None

        Raises:
            ValueError: Desteklenmeyen dosya türü durumunda (sadece ses veya video dosyaları desteklenir).

        Example:
            clip("input.mp4", "output.mp4", 5000, 10000)
            # input.mp4 dosyasının 5 saniye ile 10 saniye arasındaki segmentini output.mp4 olarak kaydeder.

        """
        file_extension = os.path.splitext(input_file)[1].lower()

        if file_extension in (".mp3", ".wav"):
            # Ses dosyası ise
            audio = AudioSegment.from_file(input_file)
            cropped_audio = audio[start_time:end_time]
            cropped_audio.export(output_file, format=file_extension[1:])
        elif file_extension in (".mp4", ".avi", ".mov"):
            # Video dosyası ise
            video = VideoFileClip(input_file)
            cropped_video = video.subclip(start_time / 1000, end_time / 1000)  # Milisaniyeden saniyeye çevirme
            cropped_video.write_videofile(output_file, codec="libx264")
        else:
            raise ValueError("Desteklenmeyen dosya türü")


import json
import subprocess
import os
import nltk
import pandas as pd
import string
from fuzzywuzzy import fuzz
import zeyrek
import openai
import uuid
import ast
nltk.download("punkt")

# openai.api_key = "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"
openai.api_key = "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"

def create_folder_if_not_exist(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

#pip install python-Levenshtein
#pip install PyArrow
# class Video:
#     def __init__(self, path):
#         self.raw_audio_path = path
#         self.input_video_path = self.extract_audio_mp3(self.raw_audio_path)
#         self.transcript = self.get_video_transcript(self.input_video_path)
#         self.documents = self.get_documents(self.transcript)
        
#     def get_video_transcript(self,path):
#         audio_3k = self.extract_audio_mp3(self.input_video_path)
#         file = open(audio_3k, "rb")
#         transcription = openai.Audio.transcribe("whisper-1", file,response_format="verbose_json",language="tr")
#         return transcription
    
#     def extract_audio_mp3(self,input_video):
#         #temp_file = tempfile.mkdtemp()
#         #print("input",input_video.split('/'))
#         output_folder = "./morpho"
#         create_folder_if_not_exist(output_folder)
#         #output_prefix = os.path.join(temp_file, f"{input_video.split('/')[-1]}temp")
#         #output_prefix = os.path.join(output_folder, f"{input_video.split('/')[-1]}temp")
#         #output_audio = f"{output_prefix}_.mp3"
#         #print(input_video.split('/')[-1].split('.')[0])
#         output_audio_path = os.path.join(output_folder, f"{input_video.split('/')[-1]}temp32_.mp3")
#         #print(output_audio_path)
        
        
#         command = [
#             "ffmpeg",
#             "-i", input_video,
#             "-vn",  # Video olmadan sadece ses çıkar
#             "-acodec", "libmp3lame",  # MP3 formatında ses çıkar
#             "-ab", "32k",  # Bit hızı 32kbps
#             output_audio_path
#         ]
#         subprocess.run(command)
#         return  output_audio_path

#     def get_documents(self,transcription):
#         df = pd.DataFrame(transcription["segments"])
#         df = df.drop(columns=["seek", "temperature", "avg_logprob", "compression_ratio", "no_speech_prob","tokens","id"])
#         df['start'] = df['start'].astype('int32')
#         df['end'] = df['end'].astype('int32')
#         documents = df.to_dict("records")
#         return documents
        
def generate_random_filename():
    random_uuid = uuid.uuid4()  # Generate a random UUID
    filename = str(random_uuid)  # Convert UUID to string
    return filename

def extract_audio_mp3(input_video):
    #temp_file = tempfile.mkdtemp()
    #print("input",input_video.split('/'))
    output_folder = "./morpho"
    create_folder_if_not_exist(output_folder)
    #output_prefix = os.path.join(temp_file, f"{input_video.split('/')[-1]}temp")
    #output_prefix = os.path.join(output_folder, f"{input_video.split('/')[-1]}temp")
    #output_audio = f"{output_prefix}_.mp3"
    #print(input_video.split('/')[-1].split('.')[0])
    # output_audio_path = os.path.join(output_folder, f"{input_video.split('/')[-1]}temp32_.mp3")
    #print(output_audio_path)
    randomfilename = generate_random_filename()
    output_audio_path = os.path.join(output_folder, f"{randomfilename}temp32.mp3")
    
    
    command = [
        "ffmpeg",
        "-i", input_video,
        "-vn",  # Video olmadan sadece ses çıkar
        "-acodec", "libmp3lame",  # MP3 formatında ses çıkar
        "-ab", "32k",  # Bit hızı 32kbps
        output_audio_path
    ]
    subprocess.run(command,check=True)
    return  output_audio_path

def get_video_transcript (input_path):
    
    audio_3k = extract_audio_mp3(input_path)
    file = open(audio_3k, "rb")
    transcription = openai.Audio.transcribe("whisper-1", file,response_format="verbose_json",language="tr")
    return transcription

def morpho_analysis(input_path):
    #video = Video(input_path)
    transcription = get_video_transcript(input_path)
    df = pd.DataFrame(transcription["segments"])
    df = df.drop(columns=["seek", "temperature", "avg_logprob", "compression_ratio", "no_speech_prob","tokens","id"])
    df['start'] = df['start'].astype('int32')
    df['end'] = df['end'].astype('int32')
    documents = df.to_dict("records")
    
    #documents = video.documents
    analyzer = zeyrek.MorphAnalyzer()
    new_documents = []

    for document in documents:
        text = document['text']
        lemmatized_text = analyzer.lemmatize(text)
        #print(lemmatized_text)
        new_document = {'start': document['start'], 'end': document['end'], 'text': lemmatized_text}
        new_documents.append(new_document)
    return new_documents,documents

#morpoloji
def word_finder(kelime, input_path):
    new_documents, _ = morpho_analysis(input_path)

    if len(kelime) < 2:
        return "Yetersiz karakter girdiniz."

    bulunan_sonuclar = []  # Bulunan sonuçları saklamak için boş bir liste

    for i, belge in enumerate(new_documents):
        # 'text' anahtarının list içinde tuple'lar formunda olup olmadığını kontrol edin ve gerekirse dönüştürün
        if isinstance(belge["text"], list):
            # Sadece tuple'ların ilk elemanını (kelimeyi) alıp birleştirin
            belge["text"] = " ".join([t[0] for t in belge["text"]])

        eslesme_orani = fuzz.partial_ratio(kelime, belge["text"].lower())
        if eslesme_orani >= 65:
            if i > 0:
                previous_text = new_documents[i - 1]["text"]
                if isinstance(previous_text, list):
                    previous_text = " ".join([t[0] for t in previous_text])
            else:
                previous_text = ""

            if i < len(new_documents) - 1:
                next_text = new_documents[i + 1]["text"]
                if isinstance(next_text, list):
                    next_text = " ".join([t[0] for t in next_text])
            else:
                next_text = ""

            # Sonuçları bir sözlük olarak ekleyin
            bulunan_sonuclar.append({
                "kelime": kelime,
                "eslesme_orani": eslesme_orani,
                "previous_text": previous_text,
                "current_text": belge["text"],
                "next_text": next_text,
                "start": belge["start"],
            })

    if not bulunan_sonuclar:
        return "Kelime bulunamadı."

    return bulunan_sonuclar


    # if all(belge["start"] != 2148 for belge in new_documents):
    #     return "Aradığınız kelime bulunmamaktadır."

    
# input_path = '/home/dell/Desktop/aa/backup/parla.mp4'
# bulunana_kelimeler = word_finder('tarih',input_path)
# print(bulunana_kelimeler)


# language = 'deutch' ################input

# def translate(input_path,language):
#     x,documents = morpho_analysis(input_path)
#     response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo-16k",
#     messages=[
#         {"role": "system", "content": "You are an AI assistant that translates in multiple languages"},
#         {"role": "assistant", "content": "data is stored in dataframe {start:'', end:'', text:''} and you just give me a translated json document"},
#         {"role": "assistant", "content": str(documents)},
#         {"role": "user", "content": "Translate the document I gave you into " + language}
#     ]
#     )
#     timecode = response["choices"][0]["message"]["content"]
#     cleaned_timecode = timecode.replace("\\", "")
#     dataList=cleaned_timecode.replace('"'," ")
#     json_data = json.dumps(dataList, ensure_ascii=False)
#     print(json_data)
#     return json_data
    
def translate(input_path,language):
    x,documents = morpho_analysis(input_path)
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are an AI assistant that translates in multiple languages"},
        {"role": "assistant", "content": "data is stored in dataframe {start:'', end:'', text:''} and you just give me a translated json document"},
        {"role": "assistant", "content": str(documents)},
        {"role": "user", "content": "Translate the document I gave you into " + language}
    ],
    response_format= { "type":"json_object" }
    )
    timecode = response["choices"][0]["message"]["content"]
    # cleaned_timecode = timecode.replace("\", "")
    # r = timecode = response["choices"][0]["message"]["content"]
    return timecode

#translated_metin = translate(input_path)
#print(translated_metin)

def get_subtext(input_path):
    x ,documents = morpho_analysis(input_path)
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
    subtext = response["choices"][0]["message"]["content"]
    
    # Split input data by empty lines
    entries = subtext.strip().split("\n\n")

    # Initialize an empty list to store parsed entries
    parsed_entries = []

    # Parse each entry
   # Split the input data by empty lines to get individual entries
    entries = subtext.strip().split("\n\n")

# Initialize an empty list to store parsed entries
    parsed_entries = []

# Parse each entry
    for entry in entries:
        # Split the entry by lines to get key-value pairs
        lines = entry.strip().split("\n")
        # Initialize variables to store values for each entry
        konu = None
        başlangıç = None
        bitiş = None
        anahtar_kelimeler = None
        # Loop through key-value pairs and extract values
        for line in lines:
            key, value = line.split(": ", 1)
            if key == "KONU":
                konu = value
            elif key == "BAŞLANGIÇ":
                başlangıç = value
            elif key == "BİTİŞ":
                bitiş = value
            elif key == "ANAHTAR KELİMELER":
                anahtar_kelimeler = value.split(", ")
        # Append the values for the current entry to the parsed entries list
        parsed_entries.append([konu, başlangıç, bitiş, anahtar_kelimeler])

        #print(subtext)

    return parsed_entries

# subtext = get_subtext(input_path)
# print(subtext)
word_finder("vatan","C:\\Users\\burak\\Desktop\\AAHackathon\\20240202_3_62382596_97343597_Preview.mp4")
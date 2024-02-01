from fastapi import FastAPI, UploadFile, File
from typing import List
import tempfile
import os
import math
import glob
import openai
import toml
from utils import parse_youtube_url,input_type_control,create_folder_if_not_exist
from pydantic import BaseModel
from moviepy.editor import AudioFileClip,VideoFileClip
from pytube import YouTube
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI
with open('config.toml', 'r') as f:
    config = toml.load(f)
openai.api_key  = config['OPENAI']['key']


# class CropRequest(BaseModel):
#     start_minute: int
#     end_minute: int

# def crop_video(raw_video, start_minute, end_minute, output_path):
#     start_ms = int(start_minute) * 60   # Convert minute to seconds
#     end_ms = int(end_minute) * 60 
#     croped_video = raw_video.subclip(start_ms, end_ms)
    
#     #shutil.copy(file_path, output_path)

# def crop_audio(raw_audio, start_minute, end_minute, output_path):
#     start_ms = int(start_minute) * 60   # Convert minute to seconds
#     end_ms = int(end_minute) * 60 
#     croped_audio = raw_audio.subclip(start_ms, end_ms)
#     croped_audio.write_audiofile(f"segment_audio/{output_path}_{str(start_ms)}-{str(end_ms)}part.mp3",
#                                  bitrate = "32k")
#         # Close reader objects
#     if hasattr(croped_audio, 'reader'):
#             croped_audio.reader.close_proc()
#     #shutil.copy(file_path, output_path)

# @app.post("/crop/")
# async def crop_media_route(crop_request: CropRequest, media_file: UploadFile = File(...)):

#     # Dosyanın uzantısına göre kırpma işlemi yap
#     file_extension = input_type_control(media_file.filename)
#     output_path = "cropped_media_file." + file_extension
    
#     print("file_extension",file_extension)

#     # if file_extension == 0:
#     #     with media_file.file as file_obj:
#     #         raw_audio = AudioFileClip(file_obj)
#     #         crop_audio(raw_audio, crop_request.start_minute, crop_request.end_minute, output_path)
#     # # elif file_extension == 1:
#     #     raw_video = VideoFileClip(media_file.filename)
#     #     raw_video_audio  = raw_video.audio 
#     #     crop_video(raw_video, crop_request.start_minute, crop_request.end_minute, output_path)
#     # else:
#     #     return {"error": "Unsupported file format"}

#     # # Kırpılmış dosyayı yanıt olarak döndür
#     # return FileResponse(output_path, media_type="audio/mpeg" if file_extension == 0 else "video/mp4")



@app.post("/translate/")
async def translate_file(file: UploadFile = File(...)):
    input_type = input_type_control(file.filename)
    # Save the uploaded file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Split the video into segments
    output_folder = tempfile.mkdtemp()
    segment_time_seconds = 90 ####################################### 90 test için burası dk*60 olacak
    split_for_translate(input_type,tmp_path, segment_time_seconds, output_folder)
    # Translate the segments
    translates = []
    files = glob.glob(f"{output_folder}/*.mp3")
    #print("files......",files)
    for file_path in sorted(files):  # Process only the first 2 files for testing
        #print("Processing file.........",file_path)
        transcription = get_openai_transcript(file_path)
        prompt = transcription["text"].encode('utf-16').decode('utf-16')
        response = call_translate_openai_api(prompt)
        translates.append(response)
        
    translated_file_name = f"Translated/{file.filename.split('/')[-1]}_translated.txt"
    folder_path = "Translated"
    create_folder_if_not_exist(folder_path)
    translated_file_name = os.path.join(folder_path, os.path.basename(file.filename) + "_translated.txt")
    print("name",translated_file_name)
        
    with open(translated_file_name, "w") as output_file:
        for resp in translates:
            output_file.write(resp + "\n")


    # Delete the temporary files and folder
    os.unlink(tmp_path)
    for file in files:
        os.unlink(file)
    os.rmdir(output_folder)

    return translates

def get_openai_transcript(file_path):
    with open(file_path, "rb") as file:
        transcription = openai.Audio.transcribe("whisper-1", file)
    return transcription

# def call_translate_openai_api(prompt):
#     response = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=prompt,
#         max_tokens=500,
#         n=1,
#         stop=None,
#         temperature=0.1,
#     )
#     return response.choices[0]['text']
def split_for_translate(type, input_video, segment_time_seconds, output_folder):
    # Video klibini yükle
    if type == 0:
        audio = AudioFileClip(input_video)
    elif type == 1:   
        video = VideoFileClip(input_video)
        audio = video.audio 
    
     # Calculate the total duration of the audio clip
    total_duration = audio.duration
    # Calculate the number of segments based on the segment time
    num_segments = math.ceil(total_duration / segment_time_seconds)
    print("bölünen video sayısı",num_segments)
    
    # Output file prefix
    output_prefix = os.path.join(output_folder, "output_segment")
    
     # Iterate over each segment and write to file
    for i in range(num_segments):
        start_time = i * segment_time_seconds
        end_time = min((i + 1) * segment_time_seconds, total_duration)
        
        # Extract the subclip
        subclip = audio.subclip(start_time, end_time)
        
        # Output file name
        output_file = f"{output_prefix}_{i + 1:03d}.mp3"
        print("outfilw",output_file)
        # Write the subclip to file
        subclip.write_audiofile(output_file, codec="mp3",bitrate = '32k')
    
    # Close the audio clip
    audio.close()

def call_translate_openai_api(chunk):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will come across a Turkish sentence, and your task is to translate it into English."
            },
            {"role": "user", "content": f"sentences{chunk}."},
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.1,
    )
    return response.choices[0]['message']['content']

# def split_video(input_video, segment_time_seconds, output_folder):
#     output_prefix = os.path.join(output_folder, "output_segment")
#     output_format = "mp3"
#     output_file_pattern = f"{output_prefix}_%03d.{output_format}"
    
#     ffmpeg_command = [
#         "ffmpeg", "-i", input_video,
#         "-c", "copy", "-f", "segment",
#         "-segment_time", str(segment_time_seconds),
#         "-reset_timestamps", "1",
#         "-segment_format", output_format,
#         output_file_pattern
#     ]

#     subprocess.run(ffmpeg_command)

class InputType(BaseModel):
    path: str
    start_minute: int
    end_minute: int
    
# def crop_video(type,start_minute: int, end_minute: int, path: str):
#     start_time = start_minute * 60
#     end_time = end_minute * 60
#     if type == 0:
#         audio = AudioFileClip(path)
#         cropped_audio = audio.subclip(start_time, end_time)
#     elif type == 1:
#         video = VideoFileClip(path)
#         cropped_video = video.subclip(start_time, end_time)


def crop_audio(start_minute: int, end_minute: int, path: str):
    start_time = int(start_minute * 60)
    end_time = int(end_minute * 60)
    audio = AudioFileClip(path)
    cropped_audio = audio.subclip(start_time, end_time)
    return cropped_audio

def crop_video(start_minute: int, end_minute: int, path: str):
    start_time = int(start_minute * 60)
    end_time = int(end_minute * 60)
    video = VideoFileClip(path)
    cropped_video = video.subclip(start_time, end_time)
    return cropped_video

def download_segment_audio(cropped_audio,output_file_prefix):
        create_folder_if_not_exist('segment_audio_api')
        cropped_audio.write_audiofile(f"segment_audio_api/{output_file_prefix}_part.mp3", bitrate = '32k')
        # Close reader objects
        if hasattr(cropped_audio, 'reader'):
            cropped_audio.reader.close_proc()
            
def download_segment_video(croped_video,output_file_prefix):
        create_folder_if_not_exist('segment_video_api')
        croped_video.write_videofile(f"segment_video_api/{output_file_prefix}_part.mp4", codec="libx264",bitrate = '32k')
        croped_video.reader.close()
        croped_video.audio.reader.close_proc()
  
def download_youtube_video(url):
        """YouTube'dan video indirir."""
        filename = str(uuid.uuid4()) + '.mp4'
        yt = YouTube(url)
        yt.streams.filter(file_extension="mp4").first().download(filename=filename)
        return filename 
@app.post("/crop-media/")
async def crop_media(item: InputType):
    item_type = input_type_control(item.path)
    if item_type == 0:
        cropped_audio = crop_audio(item.start_minute, item.end_minute, item.path)
        output_path = f"{item.path.split('/')[-1]}"
        download_segment_audio(cropped_audio,output_path)
    elif item_type == 1:
        croped_video = crop_video(item.start_minute, item.end_minute, item.path)
        output_path = f"{item.path.split('/')[-1]}"
        download_segment_video(croped_video,output_path)
    elif item_type == 2:
        down_yt_path = tempfile.mkdtemp()
        try:
            downloaded_video_path = download_youtube_video(item.path)
            croped_video = crop_video(item.start_minute, item.end_minute, downloaded_video_path)
            output_path = f"{item.path.split('/')[-1]}"
            download_segment_video(croped_video, output_path)
        finally:
            shutil.rmtree(down_yt_path) 
       
    else:
        raise HTTPException(status_code=400, detail="YouTube videosu doğrudan kesilemez.")
    return {"message": "İşlem başarılı", "output_path": output_path}

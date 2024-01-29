from moviepy.editor import VideoFileClip
from pytube import YouTube
import openai
import os

# API Anahtarını Ortam Değişkeninden Al
openai.api_key = os.getenv("")


def extract_audio(input_video_path, output_audio_path, bitrate="32k"):
    """Video dosyasından ses dosyasını çıkarır."""
    try:
        video_clip = VideoFileClip(input_video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(output_audio_path, bitrate=bitrate)
    finally:
        video_clip.close()


def download_video(url, filename):
    """YouTube'dan video indirir."""
    yt = YouTube(url)
    yt.streams.filter(file_extension="mp4").first().download(filename=filename)


def transcribe_audio(file_path):
    """Ses dosyasını transkribe eder."""
    with open(file_path, "rb") as file:
        transcription = openai.Audio.transcribe("whisper-1", file)
        return transcription["text"].encode("utf-8").decode("utf-8")


def main():
    url = "https://www.youtube.com/watch?v=2gPiiHnXhZw"
    filename = "gezeravci.mp4"
    input_video_path = "c:\\Users\\muham\\Desktop\\AA_Hackathon\\gezeravci.mp4"
    output_audio_path = "c:\\Users\\muham\\Desktop\\AA_Hackathon\\gezeravci.mp3"

    extract_audio(input_video_path, output_audio_path)
    download_video(url, filename=filename)
    transcribed_text = transcribe_audio(output_audio_path)

    with open("transcription.txt", "w", encoding="utf-8") as text_file:
        text_file.write(transcribed_text)


if __name__ == "__main__":
    main()

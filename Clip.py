from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import os



def clip(input_file, output_file, start_time, end_time):
    file_extension = os.path.splitext(input_file)[1].lower()

    if file_extension in (".mp3", ".wav"):
        # Ses dosyası ise
        audio = AudioSegment.from_file(input_file)
        cropped_audio = audio[start_time:end_time]
        cropped_audio.export(output_file, format=file_extension[1:])
    elif file_extension in (".mp4", ".avi", ".mov"):
        # Video dosyası ise
        video = VideoFileClip(input_file)
        cropped_video = video.subclip(start_time, end_time)
        cropped_video.write_videofile(output_file, codec="libx264")
    else:
        print("Desteklenmeyen dosya türü")


"""# Kullanım örneği:
input_file = "C:\\Users\\CAN\\Desktop\\AA_Hackathon\\Project1\\Clip\\gezeravci.mp3"  # veya "ses.wav"
output_file = "clip.mp3"  # Çıktı dosyasının adı
start_time = 1000  # Başlangıç süresi (milisaniye)
end_time = 3000  # Bitiş süresi (milisaniye)

clip(input_file, output_file, start_time, end_time)"""

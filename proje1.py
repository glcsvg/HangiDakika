from moviepy.editor import AudioFileClip,VideoFileClip
from pytube import YouTube
from utils import input_type_control
import uuid

class Audio:
    def __init__(self,path):
        self.raw_audio_path = path
        self.raw_audio = AudioFileClip(self.raw_audio_path)
        self.file_part = 0
        self.bitrate = "32k"
        self.output_file_prefix = self.raw_audio_path.split('/')[-1]
        self.file_part = 0
        
    def get_segment_audio(self,start,end):
        start_ms = int(start) * 60   # Convert minute to seconds
        end_ms = int(end) * 60 
        cropped_audio = self.raw_audio.subclip(start_ms, end_ms)
        
        return cropped_audio
        
    def download_segment_audio(self,cropped_audio):
        cropped_audio.write_audiofile(f"segment_audio/{self.output_file_prefix}_{self.file_part}_part.mp3", bitrate = self.bitrate)
        # Close reader objects
        if hasattr(cropped_audio, 'reader'):
            cropped_audio.reader.close_proc()
        self.file_part += 1
     
class Video():
    def __init__(self,path):
        self.raw_audio_path = path
        self.raw_video_clip = VideoFileClip(self.raw_audio_path)
        self.raw_video_audio  = self.raw_video_clip.audio 
        #self.raw_video_clip.close() 
        self.file_part = 0
        self.bitrate = "32k"
        self.output_file_prefix = self.raw_audio_path.split('/')[-1]
        
    def get_segment_video(self,start,end):
        start_ms = int(start) * 60   # Convert minute to seconds
        end_ms = int(end) * 60 
        croped_video = self.raw_video_clip.subclip(start_ms, end_ms)
        return croped_video
    
    def download_segment_video(self,croped_video):
        # Kırpılmış videoyu kaydet
        croped_video.write_videofile(f"segment_video/{self.output_file_prefix}_{self.file_part}.mp4", codec="libx264")
        # Belleği serbest bırak
        croped_video.reader.close()
        croped_video.audio.reader.close_proc()
        
class YoutubeUrl:
    def __init__(self,url):
        self.raw_url= url
        #self.down_yt_path = self.download_youtube_video(url)
        #print(self.down_yt_path)
        self.down_yt_path = './566f5223-dc1c-4197-9480-fffdf46f3ae7.mp4'
        self.raw_video_clip = VideoFileClip(self.down_yt_path)
        self.raw_audio = self.raw_video_clip.audio
        #self.raw_video_clip.close()
        self.output_file_prefix = self.down_yt_path.split('/')[-1]
        self.file_part = 0
        
    def get_segment_video(self,start,end):
        start_ms = int(start) * 60   # Convert minute to seconds
        end_ms = int(end) * 60 
        croped_video = self.raw_video_clip.subclip(start_ms, end_ms)
        return croped_video
    
    def download_segment_video(self,croped_video):
        # Kırpılmış videoyu kaydet
        print("kaydet",f"segment_video/{self.output_file_prefix}_{self.file_part}.mp4")
        croped_video.write_videofile(f"segment_video/{self.output_file_prefix}_{self.file_part}.mp4", codec="libx264")
        # Belleği serbest bırak
        croped_video.reader.close()
        croped_video.audio.reader.close_proc()
        
    def download_youtube_video(self,url):
        """YouTube'dan video indirir."""
        filename = str(uuid.uuid4()) + '.mp4'
        yt = YouTube(url)
        yt.streams.filter(file_extension="mp4").first().download(filename=filename)
        return filename
            

# örnek  
#data_list = ['https://www.youtube.com/watch?v=7U7SGYPcdiM'] #youtube test
data_list = ['./cb_uzun.mp3']
#data_list = ['./raw/aaexam.mp4']

### 0 audio file  / 1 video file / 2 url

for i in data_list:
    type = input_type_control(i)
    if type == 0:
        audio_obj = Audio(i)
        croped_audio = audio_obj.get_segment_audio(10,12)
        audio_obj.download_segment_audio(croped_audio)
    elif type  == 1:
        video_obj = Video(i)
        croped_video_audio = video_obj.get_segment_video(1,2)
        video_obj.download_segment_video(croped_video_audio)
    elif type  == 2:
        url_obj = YoutubeUrl(i)
        croped_video_audio = url_obj.get_segment_video(1,2)
        url_obj.download_segment_video(croped_video_audio)


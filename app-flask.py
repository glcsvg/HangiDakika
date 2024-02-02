from flask import Flask, request, jsonify
import toml
import openai
import subprocess
import os
#from moviepy.editor import AudioFileClip, VideoFileClip
import tempfile
import shutil
import glob

app = Flask(__name__)

# Load configuration from config.toml
with open('config.toml', 'r') as f:
    config = toml.load(f)

def create_folder_if_not_exist(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
# Set OpenAI API key
openai.api_key = config['OPENAI']['key']

# def get_openai_transcript(file):
#     with open(file, "rb") as f:
#         transcription = openai.Audio.transcribe("whisper-1", f)
#     return transcription

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

# def answer_question(input_video):
#     type = 1
#     if type == 0:
#         audio = AudioFileClip(input_video)
#     elif type == 1:
#         video = VideoFileClip(input_video)
#         audio = video.audio

#     temp_file = tempfile.mkdtemp()

#     output_prefix = os.path.join(temp_file, "temp")
#     output_file = f"{output_prefix}.mp3"
#     audio.write_audiofile(output_file, codec="mp3", bitrate='32k')

#     output_folder = './answer'
#     transcriptions = []
#     answers = []
#     files = glob.glob(f"{temp_file}/*.mp3")
#     print(files)

def extract_audio_with_ffmpeg(input_video):
    #temp_file = tempfile.mkdtemp()
    #print("input",input_video.split('/'))
    #output_folder = "./out"
    #output_prefix = os.path.join(temp_file, f"{input_video.split('/')[-1]}temp")
    #output_prefix = os.path.join(output_folder, f"{input_video.split('/')[-1]}temp")
    #output_audio = f"{output_prefix}_.mp3"
    #print(output_audio)
    output_folder = tempfile.mkdtemp()
    output_audio = os.path.join(output_folder, f"{input_video.split('/')[-1]}temp_.mp3")
    
    command = [
        "ffmpeg",
        "-i", input_video,
        "-vn",  # Video olmadan sadece ses çıkar
        "-acodec", "libmp3lame",  # MP3 formatında ses çıkar
        "-ab", "32k",  # Bit hızı 32kbps
        output_audio
    ]
    subprocess.run(command)
    # files = glob.glob(f"{temp_file}/*.mp3")
    # print("TEMPFİLE dosyaları",files)
    
    # MP3 dosyasını 90 saniyelik parçalara bölme işlemi
    # segment_output_folder = os.path.join(output_folder, "segments")
    # #os.makedirs(segment_output_folder)
    # print("segment_output_folder",segment_output_folder)
    #segment_prefix = os.path.join(segment_output_folder, f"{input_video.split('/')[-1]}segment")
    
    segment_output_folder = tempfile.mkdtemp()
    segment_prefix = os.path.join(segment_output_folder, f"{input_video.split('/')[-1]}segment")
   
    command = [
        "ffmpeg",
        "-i", output_audio,
        "-f", "segment",
        "-segment_time", "90",  #############şuan 90
        "-c", "copy",
        "-map", "0",
        "-reset_timestamps", "1",
        "-segment_format", "mp3",
        f"{segment_prefix}%03d.mp3"
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    files_in_folder = os.listdir(segment_output_folder)
    files = [os.path.join(segment_output_folder, file) for file in files_in_folder]

    return  files, output_folder, segment_output_folder

def get_whisper_transription(files):
    transcriptions = []
    for chunk_file in sorted(files):
        with open(chunk_file, "rb") as f:
            transcription = openai.Audio.transcribe("whisper-1", f)
            transcription["text"].encode('utf-16').decode('utf-16')
            transcriptions.append(transcription)
    return transcriptions

def translate_(input_video):
    files, output_folder, segment_output_folder = extract_audio_with_ffmpeg(input_video)
    print("files    ..........",files)
    #print(files)
    transcriptions = get_whisper_transription(files)
    translates = []
    for transc in transcriptions:
        prompt =f"""
                - if there is 'Altyazı: M.K.' remove this word from senteces
                {transc["text"].encode('utf-8').decode('utf-8')}
                """ 
        response = call_translate_openai_api(prompt)
        translates.append(response)
    # for chunk_file in sorted(files):
    #     #print("chunk_file..............................",chunk_file)
    #     transcription = get_openai_transcript(chunk_file)
    #     prompt = f"""
    #       {transcription["text"].encode('utf-16').decode('utf-16')}
    #     """
    #     response = call_translate_openai_api(prompt)
    #                      #print(result["text"])
    #       #transcription = openai.Audio.translations("whisper-1", chunk_file, response_format="verbose_json")

    #     transcriptions.append(transcription)
    #   translates.append(response)
    translated_file_name = f"Translated/{input_video.split('/')[-1]}_translated.txt"
    print("translated_file_name",translated_file_name)
    folder_path = "Translated"
    create_folder_if_not_exist(folder_path)
    #translated_file_name = os.path.join(folder_path, os.path.basename(file.filename) + "_translated.txt")
        
    with open(translated_file_name, "w") as output_file:
        for resp in translates:
            output_file.write(resp + "\n")
            
    shutil.rmtree(output_folder)
    shutil.rmtree(segment_output_folder)

@app.route('/translate', methods=['POST'])
def translate_process():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    print("file.filename",file.filename)
    # Save uploaded file
    filename = os.path.join(tempfile.gettempdir(), file.filename)
    print("filanemane",filename)
    file.save(filename)
    answer = translate_(filename)
    return jsonify({'answer': answer})

@app.route("/")
def index():
    return "ana sayfa"


if __name__ =="__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
from edited import VideoProcessor

app = Flask(__name__)
CORS(app)

vp = VideoProcessor(openai_api_key="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")  # OpenAI API anahtarınızı buraya girin


@app.route("/api/keywordanalysis", methods=["POST"])
def keyword_analysis():
    # İstekten JSON veriyi alın
    data = request.json

    # JSON verisinde video path ve keyword var mı diye kontrol edin
    if "video_path" not in data or "keyword" not in data:
        return jsonify({"error": "Video path and keyword are required"}), 400

    # Video path ve keywordyu alın
    video_path = data["video_path"]
    keyword = data["keyword"]

    # Video path ve keywordyu kullanarak işlemleri gerçekleştirin

    # İşlemler sonucunda dönecek veriyi hazırlayın
    #sonuc = {"video_path":video_path,"keyword":keyword} 
    sonuc=vp.word_finder_with_morpho_analysis(word=keyword,input_video=video_path)

    return jsonify(sonuc), 200


@app.route("/api/topics", methods=["POST"])
def topics():
    # İstekten JSON veriyi alın
    data = request.json

    # JSON verisinde video path ve keyword var mı diye kontrol edin
    if "video_path" not in data:
        return jsonify({"error": "Video path are required"}), 400

    # Video path ve keywordyu alın
    video_path = data["video_path"]
    

    # Video path ve keywordyu kullanarak işlemleri gerçekleştirin

    # İşlemler sonucunda dönecek veriyi hazırlayın
    sonuc = vp.get_subtext(video_path)

    return jsonify(sonuc), 200

@app.route("/api/clipping", methods=["POST"])
def clipping():
    # POST isteği ile gelen verileri alın
    data = request.get_json()

    # Gerekli parametreleri çıkarın
    input_file = data.get("input_file")
    output_file = data.get("output_file")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    # Kırpma işlemini çağırın
    vp.clip(input_file, output_file, start_time, end_time)

    return jsonify({"message": "Dosya başarıyla kesildi."})


@app.route("/api/translate", methods=["POST"])
def multiTranslate():
    # POST isteği ile gelen verileri alın
    data = request.get_json()

    # Gerekli parametreleri çıkarın
    path = data.get("path")
    lang = data.get("lang")
   

    # Translate
    sonuc = vp.translate_transcription(path, lang)

    return jsonify(sonuc,{"message": "Dosya başarıyla çevrildi"})


if __name__ == "__main__":
    app.run()
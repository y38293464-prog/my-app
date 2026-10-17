from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app) 

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "الرجاء إدخال الرابط"}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', info.get('entries', [{}])[0].get('url'))
            return jsonify({"success": True, "download_link": video_url})
    except Exception as e:
        return jsonify({"success": False, "error": "حدث خطأ أثناء جلب المقطع، تأكد من الرابط."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, render_template, request, send_file, jsonify
from pytubefix import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    quality = request.form.get('quality') # '360p', '720p', etc.
    format_type = request.form.get('format')

    try:
        yt = YouTube(url)
        if format_type == 'mp3':
            stream = yt.streams.filter(only_audio=True).first()
        else:
            # Selected quality ke hisaab se stream dhundna
            stream = yt.streams.filter(res=quality, file_extension='mp4', progressive=True).first()
            # Agar 1080p ya specific quality nahi milti toh highest available le lo
            if not stream:
                stream = yt.streams.get_highest_resolution()
        
        file_path = stream.download(output_path="downloads")
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    if not os.path.exists('downloads'): os.makedirs('downloads')
    app.run(debug=True)

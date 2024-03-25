from flask import Flask, request, jsonify, render_template
from pytube import YouTube

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')

    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if not stream:
            return jsonify({'error': 'No video available for download'}), 400

        # Get the direct download link of the video
        download_link = stream.url

        # Return a redirect to the direct download link
        return jsonify({'download_link': download_link}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)

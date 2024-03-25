from flask import Flask, request, Response, render_template
import requests
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')

    try:
        # Get YouTube video object
        yt = YouTube(video_url)

        # Get the first stream available
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first()

        if not stream:
            return 'No video available for download'

        # Fetch the direct video URL
        video_url = stream.url

        # Make a request to the direct video URL
        response = requests.get(video_url, stream=True)

        if response.status_code != 200:
            return 'Failed to fetch video', response.status_code

        # Stream video data back to the client
        def generate():
            for chunk in response.iter_content(chunk_size=1024):
                yield chunk

        return Response(generate(), content_type='video/mp4', direct_passthrough=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)

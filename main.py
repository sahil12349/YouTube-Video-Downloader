from flask import Flask, request,render_template,jsonify
from pytubefix import YouTube
from pytubefix.cli import on_progress

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #this file will be render 

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get('url')
    #checks if url follow this format no then goto else statemnet


    if not video_url.startswith('https://www.youtube.com/shorts/'):
        return jsonify(success=False, message="Invalid URL")
    # if url is correct then this code will run

    try:
        yt= YouTube(video_url, on_progress_callback=on_progress)
        stream =yt.streams.filter(progressive=True, file_extension='mp4').first()


        if stream:
            download_url = stream.url
            title = yt.title
            thumbnail_url = yt.thumbnail_url
            return jsonify(success=True,download_url=download_url,title=title,thumbnail_url=thumbnail_url)
        else:
            return jsonify(success=False, message="Not Available")
    except Exception as e: #exception handleing
        return jsonify(success=False,message=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
    
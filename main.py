from flask import Flask, request, render_template, jsonify
import yt_dlp
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get('url')
    
    # Regex patterns for YouTube URLs
    patterns = [
        r'https://www\.youtube\.com/shorts/([^/?]+)',
        r'https://www\.youtube\.com/watch\?v=([^&/?]+)',
        r'https://youtu\.be/([^/?]+)'
    ]

    # Check if the URL matches any of the patterns
    video_id = None
    for pattern in patterns:
        match = re.match(pattern, video_url)
        if match:
            video_id = match.group(1)
            break

    if not video_id:
        return jsonify(success=False, message="Invalid URL")

    video_url = f'https://www.youtube.com/watch?v={video_id}'  # Use the full URL format

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'skip_download': True,  # Skip the download, only get the link
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            formats = info_dict.get('formats', [])
            
            # Filter formats to get the best audio-only format
            audio_formats = [f for f in formats if f.get('acodec') is not None]
            if not audio_formats:
                return jsonify(success=False, message="No audio formats found")

            # Sort by 'abr' (audio bitrate), handle None values by treating them as 0
            best_audio = sorted(audio_formats, key=lambda x: x.get('abr', 0) or 0, reverse=True)[0]
            mp3_url = best_audio.get('url')

        # Get the thumbnail URL
        thumbnail_url = info_dict.get('thumbnail', '')

        return jsonify(success=True, download_url=mp3_url, title=info_dict.get('title'), thumbnail=thumbnail_url)
    except Exception as e:
        return jsonify(success=False, message=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)

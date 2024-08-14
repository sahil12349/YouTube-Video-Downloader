import yt_dlp

def get_youtube_video_details(youtube_link):
    try:
        # Setup yt-dlp options
        ydl_opts = {
            'quiet': True,  # Suppress output
            'noplaylist': True,  # Only process a single video
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information
            info_dict = ydl.extract_info(youtube_link, download=False)
            
            return info_dict
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage:
youtube_link = input("Enter the YouTube link: ")
video_details = get_youtube_video_details(youtube_link)
print("Video Details:", video_details)

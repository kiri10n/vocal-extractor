from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv
from pytube import YouTube
import moviepy.editor as mp

load_dotenv()

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_KEY = os.environ["API_KEY"]

def download_video(url, output_directory, video_file_name):
    yt = YouTube(url)
    ys = yt.streams.filter(only_audio=False).first()
    video_output_path = os.path.join(output_directory, video_file_name)
    ys.download(output_path=output_directory, filename=video_file_name)
    return video_output_path

def video_to_mp3(video_path, mp3_path):
    audio_clip = mp.AudioFileClip(video_path)
    audio_clip.write_audiofile(mp3_path)

def main():
    ###
    ### settings start
    ###
    youtube_url = "https://www.youtube.com/watch?v=ji99kh-GzTQ"
    output_directory = "downloads"
    file_name = "attitude"
    ###
    ### settings end
    ### 

    os.makedirs(output_directory, exist_ok=True)

    if file_name == "":
        print("ファイル名を設定してください．")
        exit()

    video_file_name = file_name + ".mp4"
    audio_file_name = file_name + ".mp3"

    try:
        video_output_path = download_video(youtube_url, output_directory, video_file_name)
        mp3_output_path = os.path.join(output_directory, audio_file_name)
        video_to_mp3(video_output_path, mp3_output_path)
        print(f"Video downloaded and converted to MP3: {mp3_output_path}")

    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

if __name__ == "__main__":
    main()
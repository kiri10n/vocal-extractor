from apiclient.discovery import build
import os
from dotenv import load_dotenv
from pytube import YouTube
import moviepy.editor as mp

def download_video(url, output_directory):
    yt = YouTube(url)
    ys = yt.streams.filter(only_audio=False).first()
    video_output_path = os.path.join(output_directory, "video.mp4")
    ys.download(output_path=output_directory, filename="video.mp4")
    return video_output_path

def video_to_mp3(video_path, mp3_path):
    audio_clip = mp.AudioFileClip(video_path)
    audio_clip.write_audiofile(mp3_path)

def main():
    youtube_url = "https://www.youtube.com/watch?v=-H_k7iwrWVY"
    output_directory = "downloads"
    os.makedirs(output_directory, exist_ok=True)
    video_output_path = download_video(youtube_url, output_directory)
    mp3_output_path = os.path.join(output_directory, "audio.mp3")
    video_to_mp3(video_output_path, mp3_output_path)
    print(f"Video downloaded and converted to MP3: {mp3_output_path}")

if __name__ == "__main__":
    main()
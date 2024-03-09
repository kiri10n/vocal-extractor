from apiclient.discovery import build
import os
from dotenv import load_dotenv
from pytube import YouTube
import moviepy.editor as mp

load_dotenv()

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_KEY = os.environ["API_KEY"]

def download_video(url, output_directory):
    yt = YouTube(url)
    ys = yt.streams.filter(only_audio=False).first()
    video_output_path = os.path.join(output_directory, "video.mp4")
    ys.download(output_path=output_directory, filename="video.mp4")
    return video_output_path

def video_to_mp3(video_path, mp3_path):
    audio_clip = mp.AudioFileClip(video_path)
    audio_clip.write_audiofile(mp3_path)

def search_videos_by_keyword(service, **kwargs):
    results = service.search().list(**kwargs).execute()

    videos = []
    for search_result in results.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    return videos

def main():
    ###
    ### settings start
    ###
    output_directory = "downloads"
    search_words = "Official Music Video OR Official Video"
    channel_id = "@officialdism1338"
    ###
    ### settings end
    ### 

    os.makedirs(output_directory, exist_ok=True)

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=YOUTUBE_API_KEY)

    try:
        search_response = search_videos_by_keyword(
            youtube,
            q=search_words,
            channelId=channel_id,
            type="video",
            part="id,snippet",
            maxResults=50
        )

        for video in search_response:
            print("Title:", video["snippet"]["title"])
            print("Video ID:", video["id"]["videoId"])
            print("Published At:", video["snippet"]["publishedAt"])
            print("Description:", video["snippet"]["description"])
            print("------------------------------------")

    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

    video_output_path = download_video(youtube_url, output_directory)
    mp3_output_path = os.path.join(output_directory, "audio.mp3")
    video_to_mp3(video_output_path, mp3_output_path)
    print(f"Video downloaded and converted to MP3: {mp3_output_path}")

if __name__ == "__main__":
    main()
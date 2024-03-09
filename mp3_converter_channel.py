from apiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv
from pytube import YouTube
import moviepy.editor as mp
import tqdm

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

def download_mp4_mp3(video, output_directory):
    youtube_url = "https://www.youtube.com/watch?v=" + video["id"]["videoId"]
    video_file_name = video["snippet"]["title"][:50] + ".mp4"
    audio_file_name = video["snippet"]["title"][:50] + ".mp3"

    video_output_path = download_video(youtube_url, output_directory, video_file_name)
    mp3_output_path = os.path.join(output_directory, audio_file_name)
    video_to_mp3(video_output_path, mp3_output_path)

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
    search_words = "Music|Video"
    channel_id = "UC9M4B-fqveLyWPGNdSkam7g"
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

        print("次の動画の音声をダウンロードしますか？")

        for video in search_response:
            print("Title:", video["snippet"]["title"][:50])
            # print("Video ID:", video["id"]["videoId"])
            # print("Published At:", video["snippet"]["publishedAt"])
            # print("Description:", video["snippet"]["description"])
            # print("------------------------------------")
        
        # ユーザーに続行するかどうかを尋ねる
        while True:
            user_input = input("(すべてダウンロード/個別にダウンロード/やめる - 1/2/3): ").lower()
            if user_input == "1":
                # メイン処理を再度実行するか、あるいは新しい処理を追加する必要がある場合はここに記述します。
                for _ in tqdm(map(download_mp4_mp3, search_response, output_directory), total=len(search_response)):
                    pass
                break
            elif user_input == "2":
                for video in search_response:
                    print("次の動画をダウンロードしますか？")
                    print("Title:", video["snippet"]["title"][:50])
                    user_input = input("(はい/いいえ/ダウンロードをやめる - y/n/q): ").lower()
                    if user_input == "y":
                        download_mp4_mp3(video, output_directory)
                    elif user_input == "n":
                        pass
                    elif user_input == "q":
                        exit()
                    else:
                        print("正しい入力をしてください。")
                        continue
                break
            elif user_input == "3":
                print("プログラムを終了します。")
                break
            else:
                print("正しい入力をしてください。")

    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

if __name__ == "__main__":
    main()
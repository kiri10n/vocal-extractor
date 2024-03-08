from apiclient.discovery import build
import os
from dotenv import load_dotenv

def main():
    load_dotenv()

    videoId = 'TaFJ0ycvQIg'
    YOUTUBE_API_KEY = os.environ["API_KEY"]

    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    videos_response = youtube.videos().list(
        part='snippet,statistics',
        id='{},'.format(videoId)
    ).execute()
    # snippet
    snippetInfo = videos_response["items"][0]["snippet"]
    # 動画タイトル
    title = snippetInfo['title']
    # チャンネル名
    channeltitle = snippetInfo['channelTitle']
    print(channeltitle)
    print(title)

if __name__ == "__main__":
    main()
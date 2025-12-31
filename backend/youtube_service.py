import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    print("WARNING: YOUTUBE_API_KEY not set!")


def get_curated_videos(search_query: str) -> list:
    """
    Search YouTube for high-quality, long-form educational videos.
    
    Args:
        search_query: Specific search query from Gemini
    
    Returns:
        List of curated video objects or empty list on failure
    """
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        
        response = youtube.search().list(
            q=search_query,
            part="snippet",
            type="video",
            videoDuration="long",  # Videos > 20 minutes only
            order="relevance",
            maxResults=2
        ).execute()
        
        videos = []
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            videos.append({
                "title": item["snippet"]["title"],
                "url": f"https://youtu.be/{video_id}",
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                "channel": item["snippet"]["channelTitle"]
            })
        
        return videos
    
    except Exception as e:
        print(f"YouTube API error: {e}")
        return []

import urllib.parse
import re
import requests


def search_youtube_videos(query: str, max_results: int = 3) -> list:
    """
    Search YouTube videos without API using web scraping.
    Returns actual video data with thumbnails.
    """
    try:
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        
        videos = []
        seen_ids = set()
        
        # Pattern to find video data in YouTube's response
        # Look for videoId followed by title
        pattern = r'"videoId":"([a-zA-Z0-9_-]{11})","thumbnail".*?"title":\{"runs":\[\{"text":"([^"]+)"\}\].*?"longBylineText":\{"runs":\[\{"text":"([^"]+)"'
        
        matches = re.findall(pattern, html)
        
        for match in matches:
            video_id, title, channel = match
            if video_id not in seen_ids and len(videos) < max_results:
                seen_ids.add(video_id)
                # Decode unicode escapes
                title = title.encode().decode('unicode_escape') if '\\u' in title else title
                channel = channel.encode().decode('unicode_escape') if '\\u' in channel else channel
                videos.append({
                    "video_id": video_id,
                    "title": title,
                    "thumbnail": f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg",
                    "channel": channel,
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                })
        
        # Fallback: simpler pattern
        if not videos:
            simple_pattern = r'"videoId":"([a-zA-Z0-9_-]{11})"'
            video_ids = list(dict.fromkeys(re.findall(simple_pattern, html)))  # Remove duplicates, keep order
            
            for video_id in video_ids[:max_results]:
                if video_id not in seen_ids:
                    seen_ids.add(video_id)
                    videos.append({
                        "video_id": video_id,
                        "title": query,
                        "thumbnail": f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg",
                        "channel": "YouTube",
                        "url": f"https://www.youtube.com/watch?v={video_id}"
                    })
        
        return videos
        
    except Exception as e:
        print(f"YouTube scraping error: {e}")
        return []


def get_curated_videos(query: str) -> list:
    """
    Get curated YouTube videos for a search query.
    """
    return search_youtube_videos(query, max_results=3)

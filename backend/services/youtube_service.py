import urllib.parse
import re
import requests


def search_youtube_videos(query: str, max_results: int = 3) -> list:
    """
    Search YouTube for full course videos (not shorts).
    Filters for longer educational content.
    """
    try:
        # Add "full course" to query for better results
        search_query = f"{query} full course tutorial"
        encoded_query = urllib.parse.quote_plus(search_query)
        
        # Use sp=EgIQAQ%253D%253D to filter for videos only (no shorts, no playlists)
        url = f"https://www.youtube.com/results?search_query={encoded_query}&sp=EgIQAQ%253D%253D"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        html = response.text
        
        videos = []
        seen_ids = set()
        
        # Pattern to find video data with duration info
        pattern = r'"videoId":"([a-zA-Z0-9_-]{11})","thumbnail".*?"title":\{"runs":\[\{"text":"([^"]+)"\}\].*?"longBylineText":\{"runs":\[\{"text":"([^"]+)"'
        
        matches = re.findall(pattern, html)
        
        # Keywords to skip (shorts, clips, etc.)
        skip_keywords = ['#shorts', 'short', 'clip', 'tiktok', 'reels', '60 sec', '1 min', 'quick']
        
        # Keywords that indicate good content
        good_keywords = ['course', 'tutorial', 'full', 'complete', 'beginner', 'learn', 'hour', 'bootcamp']
        
        for match in matches:
            video_id, title, channel = match
            
            if video_id in seen_ids:
                continue
                
            # Decode unicode
            title_decoded = title.encode().decode('unicode_escape') if '\\u' in title else title
            channel_decoded = channel.encode().decode('unicode_escape') if '\\u' in channel else channel
            title_lower = title_decoded.lower()
            
            # Skip shorts and clips
            if any(skip in title_lower for skip in skip_keywords):
                continue
            
            # Prioritize videos with good keywords
            has_good_keyword = any(good in title_lower for good in good_keywords)
            
            seen_ids.add(video_id)
            videos.append({
                "video_id": video_id,
                "title": title_decoded,
                "thumbnail": f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg",
                "channel": channel_decoded,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "priority": 1 if has_good_keyword else 0
            })
        
        # Sort by priority (good keywords first) and take top results
        videos.sort(key=lambda x: x.get('priority', 0), reverse=True)
        
        # Remove priority field and return
        result = []
        for v in videos[:max_results]:
            del v['priority']
            result.append(v)
        
        return result
        
    except Exception as e:
        print(f"YouTube scraping error: {e}")
        return []


def get_curated_videos(query: str) -> list:
    """Get curated YouTube videos - full courses only."""
    return search_youtube_videos(query, max_results=3)

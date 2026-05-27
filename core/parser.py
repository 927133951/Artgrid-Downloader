import requests
import re
class ArtgridParser:
    API_BASE = "https://artgrid.io/api"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://artgrid.io/",
        "Origin": "https://artgrid.io",
    }
    @staticmethod
    def extract_story_id(url):
        match = re.search(r'artgrid\.io/story/(\d+)', url)
        if match:
            return match.group(1)
        return None
    @staticmethod
    def get_story_details(story_id, page=1):
        url = f"{ArtgridParser.API_BASE}/story/details"
        params = {"storyId": story_id, "page": page}
        try:
            resp = requests.get(url, params=params, headers=ArtgridParser.HEADERS, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception:
            return None
    @staticmethod
    def get_clip_details(clip_id):
        url = f"{ArtgridParser.API_BASE}/clip/details"
        params = {"clipId": clip_id}
        try:
            resp = requests.get(url, params=params, headers=ArtgridParser.HEADERS, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception:
            return None
    @staticmethod
    def convert_playlist_to_2160p(m3u8_url):
        return m3u8_url.replace("_playlist_", "_2160p_")
    @staticmethod
    def parse_all_clips(story_id, progress_callback=None):
        all_clips = []
        story_title = ""
        page = 1
        while True:
            if progress_callback:
                progress_callback(f"正在获取第 {page} 页视频数据...")
            data = ArtgridParser.get_story_details(story_id, page)
            if not data:
                break
            if not story_title:
                story_title = data.get("name", "")
            clips = data.get("clips", [])
            if not clips:
                break
            all_clips.extend(clips)
            total_count = data.get("totalClipCount", 0)
            if len(all_clips) >= total_count:
                break
            page += 1
        result = []
        for idx, clip in enumerate(all_clips):
            playlist_url = clip.get("clipPath", "")
            ts_url = ArtgridParser.convert_playlist_to_2160p(playlist_url) if playlist_url else ""
            clip_info = {
                "id": clip.get("id"),
                "name": clip.get("clipName", "未命名"),
                "m3u8_url": ts_url,
                "thumbnail": clip.get("thumbnailUrl", ""),
                "resolution": f"{clip.get('width', '?')}x{clip.get('height', '?')}",
                "quality": clip.get("highQualityFormat", ""),
                "tags": [t.get("name", "") for t in clip.get("tags", [])],
                "filmMaker": clip.get("filmMakerDisplayName", ""),
                "story_name": story_title,
                "clip_index": idx + 1,
            }
            result.append(clip_info)
        return result

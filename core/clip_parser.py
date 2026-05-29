import os
import re
import json
import requests
from curl_cffi import requests as cffi_requests
class ClipParser:
    API_BASE = "https://artgrid.io/api"
    API_HEADERS = {
        "Accept": "application/json",
        "Referer": "https://artgrid.io/",
        "Origin": "https://artgrid.io",
        "searchengine": "",
    }
    DOWNLOAD_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://artgrid.io/",
        "Origin": "https://artgrid.io",
        "Accept": "*/*",
    }
    @staticmethod
    def extract_clip_id(url):
        match = re.search(r'artgrid\.io/clip/(\d+)', url)
        if match:
            return match.group(1)
        return None
    @staticmethod
    def get_clip_info_from_api(clip_id, clip_url=""):
        url = f"{ClipParser.API_BASE}/clip/details"
        params = {"clipId": clip_id}
        headers = dict(ClipParser.API_HEADERS)
        if clip_url:
            headers["Referer"] = clip_url
        try:
            resp = cffi_requests.get(url, params=params, headers=headers, impersonate='chrome', timeout=30)
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception:
            return None
    @staticmethod
    def get_m3u8_url(clip_info):
        playlist_url = clip_info.get("clipPath", "")
        if playlist_url:
            if "_playlist_" in playlist_url:
                return playlist_url.replace("_playlist_", "_2160p_")
            return playlist_url
        return ""
    @staticmethod
    def parse_m3u8_segments(m3u8_url):
        from core.downloader import M3U8Downloader
        return M3U8Downloader.parse_m3u8_segments(m3u8_url)
    @staticmethod
    def parse_clip_url(url, progress_callback=None):
        if progress_callback:
            progress_callback("正在提取片段ID...")
        clip_id = ClipParser.extract_clip_id(url)
        if not clip_id:
            if progress_callback:
                progress_callback("无法从URL中提取片段ID")
            return None, [], {}
        if progress_callback:
            progress_callback(f"片段ID: {clip_id}，正在获取片段信息...")
        clip_info = ClipParser.get_clip_info_from_api(clip_id, url)
        if not clip_info:
            if progress_callback:
                progress_callback("获取片段信息失败，请检查URL或网络连接")
            return None, [], {}
        m3u8_url = ClipParser.get_m3u8_url(clip_info)
        if not m3u8_url:
            if progress_callback:
                progress_callback("未找到M3U8播放链接")
            return None, [], {}
        if progress_callback:
            progress_callback(f"正在解析M3U8播放列表...")
        segments = ClipParser.parse_m3u8_segments(m3u8_url)
        if not segments:
            playlist_url = m3u8_url.replace("_2160p_", "_playlist_")
            if playlist_url != m3u8_url:
                if progress_callback:
                    progress_callback("尝试备用解析...")
                segments = ClipParser.parse_m3u8_segments(playlist_url)
        if progress_callback:
            progress_callback(f"解析完成，共找到 {len(segments)} 个TS分片")
        return m3u8_url, segments, clip_info
    @staticmethod
    def download_segments(segments, output_path, progress_callback=None):
        from core.downloader import M3U8Downloader
        if not M3U8Downloader.check_ffmpeg():
            if progress_callback:
                progress_callback("错误：未检测到ffmpeg，请安装ffmpeg并添加到系统PATH")
            return False
        total = len(segments)
        if progress_callback:
            progress_callback(f"共 {total} 个分片，开始下载...")
        buffer = bytearray()
        for i, seg_url in enumerate(segments):
            for retry in range(3):
                try:
                    resp = requests.get(seg_url, headers=ClipParser.DOWNLOAD_HEADERS, timeout=120)
                    if resp.status_code == 200:
                        buffer.extend(resp.content)
                        pct = int((i + 1) / total * 100)
                        if progress_callback:
                            progress_callback(f"下载中: {pct}% ({i+1}/{total})")
                        break
                    elif retry == 2:
                        if progress_callback:
                            progress_callback(f"分片 {i+1} 下载失败: HTTP {resp.status_code}")
                        return False
                except requests.exceptions.RequestException as e:
                    if retry == 2:
                        if progress_callback:
                            progress_callback(f"分片 {i+1} 出错: {str(e)[:80]}")
                        return False
        size_mb = len(buffer) / 1024 / 1024
        if progress_callback:
            progress_callback(f"分片下载完成: {size_mb:.1f}MB，正在保存...")
        ts_data = bytes(buffer)
        temp_ts_path = M3U8Downloader.write_temp_ts(ts_data, progress_callback)
        if temp_ts_path is None:
            if progress_callback:
                progress_callback("临时文件写入失败")
            return False
        final_path = M3U8Downloader.get_unique_path(output_path)
        if final_path != output_path:
            if progress_callback:
                progress_callback(f"检测到同名文件，自动重命名为: {os.path.basename(final_path)}")
        dest_dir = os.path.dirname(final_path)
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir, exist_ok=True)
            except:
                pass
        if M3U8Downloader.ffmpeg_convert_shell(temp_ts_path, final_path, progress_callback):
            M3U8Downloader.try_remove_file(temp_ts_path)
            return True
        if M3U8Downloader.ffmpeg_convert_detached(temp_ts_path, final_path, progress_callback):
            M3U8Downloader.try_remove_file(temp_ts_path)
            return True
        if M3U8Downloader.convert_in_project_then_move(temp_ts_path, final_path, progress_callback):
            M3U8Downloader.try_remove_file(temp_ts_path)
            return True
        M3U8Downloader.try_remove_file(temp_ts_path)
        if progress_callback:
            progress_callback("所有保存方式均失败")
        return False
    @staticmethod
    def generate_clip_filename(clip_info, url=""):
        name = clip_info.get("name", clip_info.get("clipName", ""))
        if not name and url:
            match = re.search(r'artgrid\.io/clip/\d+/(.+)$', url)
            if match:
                name = match.group(1).replace('-', '_')
        if not name:
            name = "未命名"
        safe_name = re.sub(r'[\\/:*?"<>|,;!@#$%^&\+=\[\]{}\'`~]', '_', name)
        safe_name = re.sub(r'[_\s]+', '_', safe_name)
        safe_name = safe_name.strip('_')
        if not safe_name:
            safe_name = f"clip_{clip_info.get('id', 'unknown')}"
        filename = f"{safe_name}.mp4"
        return filename

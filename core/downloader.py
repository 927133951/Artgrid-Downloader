import os
import re
import json
import subprocess
import sys
import shutil
import time
import requests
class M3U8Downloader:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://artgrid.io/",
        "Origin": "https://artgrid.io",
        "Accept": "*/*",
    }
    @staticmethod
    def generate_filename(clip_info):
        name = clip_info.get("name", "未命名")
        safe_name = re.sub(r'[\\/:*?"<>|,;!@#$%^&\+=\[\]{}\'`~]', '_', name)
        safe_name = re.sub(r'[_\s]+', '_', safe_name)
        safe_name = safe_name.strip('_')
        if not safe_name:
            safe_name = f"video_{clip_info.get('clip_index', 1)}"
        filename = f"{safe_name}.mp4"
        return filename
    @staticmethod
    def sanitize_path(save_dir, filename):
        save_dir = os.path.normpath(save_dir)
        output_path = os.path.join(save_dir, filename)
        output_path = os.path.normpath(output_path)
        return output_path
    @staticmethod
    def get_unique_path(output_path):
        if not os.path.exists(output_path):
            return output_path
        base, ext = os.path.splitext(output_path)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        new_path = f"{base}_{timestamp}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter = 2
        while os.path.exists(f"{base}_{timestamp}_{counter}{ext}"):
            counter += 1
        return f"{base}_{timestamp}_{counter}{ext}"
    @staticmethod
    def get_project_temp_dir():
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        temp_dir = os.path.join(base_dir, "temp")
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir
    @staticmethod
    def check_ffmpeg():
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True, text=True, timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW,
                env=os.environ.copy()
            )
            return result.returncode == 0
        except Exception:
            return False
    @staticmethod
    def parse_m3u8_segments(m3u8_url):
        try:
            resp = requests.get(m3u8_url, headers=M3U8Downloader.HEADERS, timeout=30)
            if resp.status_code != 200:
                return []
            content = resp.text
            if '#EXT-X-STREAM-INF' in content:
                lines = content.strip().split('\n')
                best_url = None
                best_bandwidth = -1
                base_url = m3u8_url.rsplit('/', 1)[0] + '/'
                current_bw = 0
                for line in lines:
                    line = line.strip()
                    if line.startswith('#EXT-X-STREAM-INF:'):
                        bw_match = re.search(r'BANDWIDTH=(\d+)', line)
                        if bw_match:
                            current_bw = int(bw_match.group(1))
                    elif line and not line.startswith('#'):
                        if current_bw > best_bandwidth:
                            best_bandwidth = current_bw
                            if line.startswith('http'):
                                best_url = line
                            else:
                                best_url = base_url + line
                        current_bw = 0
                if best_url:
                    return M3U8Downloader.parse_m3u8_segments(best_url)
                return []
            segments = []
            base_url = m3u8_url.rsplit('/', 1)[0] + '/'
            lines = content.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith('http'):
                        segments.append(line)
                    else:
                        segments.append(base_url + line)
            return segments
        except Exception:
            return []
    @staticmethod
    def download_segments_to_memory(m3u8_url, progress_callback=None):
        if progress_callback:
            progress_callback("正在解析视频分片列表...")
        segments = M3U8Downloader.parse_m3u8_segments(m3u8_url)
        if not segments:
            playlist_url = m3u8_url.replace("_2160p_", "_playlist_")
            if playlist_url != m3u8_url:
                if progress_callback:
                    progress_callback("尝试备用解析...")
                segments = M3U8Downloader.parse_m3u8_segments(playlist_url)
        if not segments:
            if progress_callback:
                progress_callback("解析失败：未找到视频分片")
            return None
        total = len(segments)
        if progress_callback:
            progress_callback(f"共 {total} 个分片，开始下载...")
        buffer = bytearray()
        for i, seg_url in enumerate(segments):
            for retry in range(3):
                try:
                    resp = requests.get(seg_url, headers=M3U8Downloader.HEADERS, timeout=120)
                    if resp.status_code == 200:
                        buffer.extend(resp.content)
                        pct = int((i + 1) / total * 100)
                        if progress_callback:
                            progress_callback(f"下载中: {pct}% ({i+1}/{total})")
                        break
                    elif retry == 2:
                        if progress_callback:
                            progress_callback(f"分片 {i+1} 下载失败: HTTP {resp.status_code}")
                        return None
                except requests.exceptions.RequestException as e:
                    if retry == 2:
                        if progress_callback:
                            progress_callback(f"分片 {i+1} 出错: {str(e)[:80]}")
                        return None
        size_mb = len(buffer) / 1024 / 1024
        if progress_callback:
            progress_callback(f"分片下载完成: {size_mb:.1f}MB，正在保存...")
        return bytes(buffer)
    @staticmethod
    def write_temp_ts(ts_data, progress_callback=None):
        temp_dir = M3U8Downloader.get_project_temp_dir()
        temp_ts = os.path.join(temp_dir, f"temp_{os.getpid()}.ts")
        try:
            with open(temp_ts, 'wb') as f:
                f.write(ts_data)
            return temp_ts
        except PermissionError:
            pass
        except Exception:
            pass
        try:
            cmd = f'python -c "import sys; open(r\'{temp_ts}\', \'wb\').write(open(r\'{temp_ts.replace(".ts", ".bin")}\', \'rb\').read())"'
            bin_path = temp_ts.replace(".ts", ".bin")
            with open(bin_path, 'wb') as f:
                f.write(ts_data)
            return bin_path
        except:
            pass
        return None
    @staticmethod
    def ffmpeg_convert_shell(temp_ts_path, output_path, progress_callback=None):
        try:
            cmd = f'ffmpeg -y -i "{temp_ts_path}" -c copy -movflags +faststart -bsf:a aac_adtstoasc "{output_path}"'
            result = subprocess.run(
                cmd, shell=True,
                capture_output=True, text=True, timeout=300,
                env=os.environ.copy()
            )
            if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                size_mb = os.path.getsize(output_path) / 1024 / 1024
                if progress_callback:
                    progress_callback(f"保存成功: {size_mb:.1f}MB -> {os.path.basename(output_path)}")
                return True
            else:
                err = result.stderr[-300:] if result.stderr else ''
                if progress_callback:
                    progress_callback(f"ffmpeg失败: {err}")
        except Exception as e:
            if progress_callback:
                progress_callback(f"ffmpeg异常: {e}")
        return False
    @staticmethod
    def ffmpeg_convert_detached(temp_ts_path, output_path, progress_callback=None):
        try:
            DETACHED = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            cmd = [
                "ffmpeg", "-y",
                "-i", temp_ts_path,
                "-c", "copy",
                "-movflags", "+faststart",
                "-bsf:a", "aac_adtstoasc",
                output_path
            ]
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                creationflags=DETACHED,
                env=os.environ.copy()
            )
            try:
                _, stderr = proc.communicate(timeout=300)
            except subprocess.TimeoutExpired:
                proc.kill()
                if progress_callback:
                    progress_callback("ffmpeg超时")
                return False
            if proc.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                size_mb = os.path.getsize(output_path) / 1024 / 1024
                if progress_callback:
                    progress_callback(f"保存成功: {size_mb:.1f}MB -> {os.path.basename(output_path)}")
                return True
            else:
                err = stderr.decode('utf-8', errors='replace')[-300:] if stderr else ''
                if progress_callback:
                    progress_callback(f"ffmpeg(detached)失败: {err}")
        except Exception as e:
            if progress_callback:
                progress_callback(f"ffmpeg(detached)异常: {e}")
        return False
    @staticmethod
    def shell_copy_to_target(src_path, dst_path, progress_callback=None):
        try:
            dst_dir = os.path.dirname(dst_path)
            if not os.path.exists(dst_dir):
                subprocess.run(
                    f'mkdir "{dst_dir}"',
                    shell=True, capture_output=True, timeout=10,
                    env=os.environ.copy()
                )
            result = subprocess.run(
                f'copy /Y "{src_path}" "{dst_path}"',
                shell=True, capture_output=True, text=True, timeout=60,
                env=os.environ.copy()
            )
            if result.returncode == 0 and os.path.exists(dst_path):
                size_mb = os.path.getsize(dst_path) / 1024 / 1024
                if progress_callback:
                    progress_callback(f"保存成功(copy): {size_mb:.1f}MB -> {os.path.basename(dst_path)}")
                return True
        except Exception as e:
            if progress_callback:
                progress_callback(f"copy失败: {e}")
        return False
    @staticmethod
    def powershell_copy_to_target(src_path, dst_path, progress_callback=None):
        try:
            dst_dir = os.path.dirname(dst_path)
            if not os.path.exists(dst_dir):
                subprocess.run(
                    f'powershell -Command "New-Item -ItemType Directory -Force -Path \'{dst_dir}\'"',
                    shell=True, capture_output=True, timeout=10,
                    env=os.environ.copy(),
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            ps_cmd = f"Copy-Item -Path '{src_path}' -Destination '{dst_path}' -Force"
            result = subprocess.run(
                f'powershell -Command "{ps_cmd}"',
                shell=True, capture_output=True, text=True, timeout=60,
                env=os.environ.copy(),
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0 and os.path.exists(dst_path):
                size_mb = os.path.getsize(dst_path) / 1024 / 1024
                if progress_callback:
                    progress_callback(f"保存成功(PS): {size_mb:.1f}MB -> {os.path.basename(dst_path)}")
                return True
        except Exception as e:
            if progress_callback:
                progress_callback(f"PowerShell失败: {e}")
        return False
    @staticmethod
    def convert_in_project_then_move(temp_ts_path, output_path, progress_callback=None):
        temp_dir = M3U8Downloader.get_project_temp_dir()
        temp_mp4 = os.path.join(temp_dir, f"temp_{os.getpid()}.mp4")
        if M3U8Downloader.ffmpeg_convert_shell(temp_ts_path, temp_mp4):
            if M3U8Downloader.shell_copy_to_target(temp_mp4, output_path, progress_callback):
                M3U8Downloader.try_remove_file(temp_mp4)
                return True
            if M3U8Downloader.powershell_copy_to_target(temp_mp4, output_path, progress_callback):
                M3U8Downloader.try_remove_file(temp_mp4)
                return True
            try:
                shutil.copy2(temp_mp4, output_path)
                if os.path.exists(output_path):
                    size_mb = os.path.getsize(output_path) / 1024 / 1024
                    if progress_callback:
                        progress_callback(f"保存成功: {size_mb:.1f}MB -> {os.path.basename(output_path)}")
                    M3U8Downloader.try_remove_file(temp_mp4)
                    return True
            except:
                pass
            M3U8Downloader.try_remove_file(temp_mp4)
        return False
    @staticmethod
    def try_remove_file(filepath):
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception:
            pass
    @staticmethod
    def download_ts(m3u8_url, output_path, progress_callback=None):
        if not M3U8Downloader.check_ffmpeg():
            if progress_callback:
                progress_callback("错误：未检测到ffmpeg，请安装ffmpeg并添加到系统PATH")
            return False
        ts_data = M3U8Downloader.download_segments_to_memory(m3u8_url, progress_callback)
        if ts_data is None:
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
                subprocess.run(
                    f'mkdir "{dest_dir}"',
                    shell=True, capture_output=True, timeout=10,
                    env=os.environ.copy()
                )
        temp_ts_path = M3U8Downloader.write_temp_ts(ts_data, progress_callback)
        if temp_ts_path is None:
            if progress_callback:
                progress_callback("临时文件写入失败")
            return False
        if M3U8Downloader.ffmpeg_convert_shell(temp_ts_path, final_path, progress_callback):
            M3U8Downloader.try_remove_file(temp_ts_path)
            return True
        if progress_callback:
            progress_callback("直接转换失败，尝试项目目录中转...")
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

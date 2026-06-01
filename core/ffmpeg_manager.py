import os
import sys
import hashlib
import shutil
import subprocess
FFMPEG_MD5 = "3614d254f8014fd8997b539383ede5fc"
FFMPEG_SIZE = 99264000
def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get_ffmpeg_target_path():
    return os.path.join(get_app_dir(), "ffmpeg.exe")
def get_ffmpeg_source_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, "bin", "ffmpeg.exe")
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin", "ffmpeg.exe")
def verify_ffmpeg(filepath):
    if not os.path.exists(filepath):
        return False
    try:
        if os.path.getsize(filepath) != FFMPEG_SIZE:
            return False
    except OSError:
        return False
    try:
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                md5.update(chunk)
        return md5.hexdigest().lower() == FFMPEG_MD5.lower()
    except Exception:
        return False
def test_ffmpeg_works(filepath):
    try:
        result = subprocess.run(
            [filepath, "-version"],
            capture_output=True, text=True, timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW,
            env=os.environ.copy()
        )
        return result.returncode == 0
    except Exception:
        return False
def extract_ffmpeg(progress_callback=None):
    target = get_ffmpeg_target_path()
    if os.path.exists(target) and verify_ffmpeg(target) and test_ffmpeg_works(target):
        if progress_callback:
            progress_callback("FFmpeg已就绪，无需重复释放")
        return True
    if os.path.exists(target):
        if progress_callback:
            progress_callback("检测到FFmpeg文件异常，正在重新释放...")
        try:
            os.remove(target)
        except Exception:
            pass
    else:
        if progress_callback:
            progress_callback("首次运行，正在释放FFmpeg组件...")
    source = get_ffmpeg_source_path()
    if not os.path.exists(source):
        if progress_callback:
            progress_callback("内置FFmpeg资源未找到，请重新下载完整程序包")
        return False
    try:
        shutil.copy2(source, target)
    except PermissionError:
        try:
            subprocess.run(
                f'copy /Y "{source}" "{target}"',
                shell=True, capture_output=True, timeout=30,
                env=os.environ.copy()
            )
        except Exception:
            pass
    except Exception:
        pass
    if not os.path.exists(target):
        if progress_callback:
            progress_callback("FFmpeg释放失败")
        return False
    if progress_callback:
        progress_callback("正在校验FFmpeg完整性...")
    if not verify_ffmpeg(target):
        try:
            os.remove(target)
        except Exception:
            pass
        if progress_callback:
            progress_callback("FFmpeg完整性校验失败，文件可能已损坏")
        return False
    if not test_ffmpeg_works(target):
        if progress_callback:
            progress_callback("FFmpeg功能测试失败")
        return False
    if progress_callback:
        progress_callback("FFmpeg组件释放完成，功能正常")
    return True
def get_ffmpeg_path():
    target = get_ffmpeg_target_path()
    if os.path.exists(target) and test_ffmpeg_works(target):
        return target
    source = get_ffmpeg_source_path()
    if os.path.exists(source):
        return source
    return "ffmpeg"

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow
from core.ffmpeg_manager import extract_ffmpeg
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    ffmpeg_ok = extract_ffmpeg()
    if not ffmpeg_ok:
        QMessageBox.warning(None, "FFmpeg组件异常",
            "FFmpeg组件释放失败或校验未通过，视频下载功能可能无法正常使用。\n"
            "请尝试以管理员权限运行本程序，或重新下载完整程序包。")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()

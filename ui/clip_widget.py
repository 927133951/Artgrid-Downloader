import os
import re
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar, QCheckBox, QMessageBox,
    QAbstractItemView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from core.clip_parser import ClipParser
from core.downloader import M3U8Downloader
class ClipParseThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    def __init__(self, url):
        super().__init__()
        self.url = url
    def run(self):
        m3u8_url, segments, clip_info = ClipParser.parse_clip_url(
            self.url, progress_callback=self.progress.emit
        )
        if not m3u8_url:
            self.error.emit("解析失败：未找到视频下载链接，请检查URL是否正确或网络连接是否正常")
            return
        clip_name = clip_info.get("clipName", clip_info.get("name", "未命名"))
        tags = clip_info.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        elif isinstance(tags, list):
            tags = [t.get("name", str(t)) if isinstance(t, dict) else str(t) for t in tags]
        clip_data = {
            "name": clip_name,
            "resolution": "2160p",
            "quality": "高",
            "tags": tags,
            "m3u8_url": m3u8_url,
        }
        self.finished.emit([clip_data])
class ClipDownloadThread(QThread):
    progress = pyqtSignal(str)
    overall_progress = pyqtSignal(int)
    finished = pyqtSignal(int, int, int)
    def __init__(self, clips, save_dir):
        super().__init__()
        self.clips = clips
        self.save_dir = save_dir
    def run(self):
        total = len(self.clips)
        success_count = 0
        skip_count = 0
        for i, clip in enumerate(self.clips):
            filename = ClipParser.generate_clip_filename(clip)
            m3u8_url = clip.get("m3u8_url", "")
            if not m3u8_url:
                self.progress.emit(f"[{i+1}/{total}] 跳过（无下载链接）: {filename}")
                skip_count += 1
                continue
            output_path = M3U8Downloader.sanitize_path(self.save_dir, filename)
            if os.path.exists(output_path):
                self.progress.emit(f"[{i+1}/{total}] 检测到同名文件，将自动重命名下载: {filename}")
            else:
                self.progress.emit(f"[{i+1}/{total}] 准备下载: {filename}")
            self.overall_progress.emit(int(i / total * 100))
            def progress_cb(msg):
                self.progress.emit(f"[{i+1}/{total}] {msg}")
            result = M3U8Downloader.download_ts(m3u8_url, output_path, progress_callback=progress_cb)
            if result:
                success_count += 1
            self.overall_progress.emit(int((i + 1) / total * 100))
        self.progress.emit(f"下载完成！成功: {success_count}, 跳过: {skip_count}, 总计: {total}")
        self.overall_progress.emit(100)
        self.finished.emit(success_count, skip_count, total)
class ClipWidget(QWidget):
    log_signal = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clips = []
        self.check_states = {}
        self.download_thread = None
        self.parse_thread = None
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(10)
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("请输入Artgrid片段页面URL，例如: https://artgrid.io/clip/6613774/outdoor-activity-adventure-sport-unique-experience-desolate-landscape")
        input_layout.addWidget(self.url_input)
        self.parse_btn = QPushButton("解 析")
        self.parse_btn.setObjectName("parseBtn")
        self.parse_btn.setFixedWidth(100)
        self.parse_btn.clicked.connect(self.on_parse)
        input_layout.addWidget(self.parse_btn)
        layout.addLayout(input_layout)
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        self.select_all_btn = QPushButton("全选")
        self.select_all_btn.setObjectName("selectAllBtn")
        self.select_all_btn.clicked.connect(self.on_select_all)
        control_layout.addWidget(self.select_all_btn)
        self.deselect_all_btn = QPushButton("取消全选")
        self.deselect_all_btn.setObjectName("deselectAllBtn")
        self.deselect_all_btn.clicked.connect(self.on_deselect_all)
        control_layout.addWidget(self.deselect_all_btn)
        self.count_label = QLabel("共 0 个视频，已选 0 个")
        self.count_label.setObjectName("subtitleLabel")
        control_layout.addWidget(self.count_label)
        control_layout.addStretch()
        self.download_btn = QPushButton("下载选中")
        self.download_btn.setObjectName("downloadBtn")
        self.download_btn.setFixedWidth(120)
        self.download_btn.clicked.connect(self.on_download)
        self.download_btn.setEnabled(False)
        control_layout.addWidget(self.download_btn)
        layout.addLayout(control_layout)
        self.save_dir_label = QLabel("")
        self.save_dir_label.setObjectName("subtitleLabel")
        layout.addWidget(self.save_dir_label)
        self._update_save_dir_label()
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["选择", "序号", "视频名称", "分辨率", "画质", "标签"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 40)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 60)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(True)
        layout.addWidget(self.table)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
    def _get_save_dir(self):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        save_dir = os.path.join(base_dir, "downloads")
        os.makedirs(save_dir, exist_ok=True)
        return save_dir
    def _update_save_dir_label(self):
        save_dir = self._get_save_dir()
        self.save_dir_label.setText(f"保存目录: {save_dir}")
    def _update_count_label(self):
        total = len(self.clips)
        selected = sum(1 for v in self.check_states.values() if v)
        self.count_label.setText(f"共 {total} 个视频，已选 {selected} 个")
    def on_parse(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "提示", "请输入Artgrid片段页面URL")
            return
        if "artgrid.io/clip/" not in url:
            QMessageBox.warning(self, "提示", "请输入正确的Artgrid片段页面URL\n格式: https://artgrid.io/clip/数字/名称")
            return
        self.parse_btn.setEnabled(False)
        self.parse_btn.setText("解析中...")
        self.table.setRowCount(0)
        self.clips = []
        self.check_states = {}
        self._update_count_label()
        self.log_signal.emit(f"开始解析片段: {url}")
        self.parse_thread = ClipParseThread(url)
        self.parse_thread.progress.connect(self.log_signal.emit)
        self.parse_thread.finished.connect(self.on_parse_finished)
        self.parse_thread.error.connect(self.on_parse_error)
        self.parse_thread.start()
    def on_parse_finished(self, clips):
        self.clips = clips
        self.parse_btn.setEnabled(True)
        self.parse_btn.setText("解 析")
        self.download_btn.setEnabled(len(clips) > 0)
        self._update_count_label()
        self.populate_table()
        self.log_signal.emit(f"解析完成，共 {len(clips)} 个视频")
    def on_parse_error(self, msg):
        self.parse_btn.setEnabled(True)
        self.parse_btn.setText("解 析")
        self.log_signal.emit(f"错误: {msg}")
        QMessageBox.critical(self, "解析失败", msg)
    def populate_table(self):
        self.table.setRowCount(len(self.clips))
        for i, clip in enumerate(self.clips):
            self.table.setRowHeight(i, 42)
            check_widget = QWidget()
            check_layout = QHBoxLayout(check_widget)
            check_layout.setContentsMargins(0, 0, 0, 0)
            check_layout.setAlignment(Qt.AlignCenter)
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            self.check_states[i] = True
            row_idx = i
            checkbox.stateChanged.connect(lambda state, idx=row_idx: self.on_check_changed(idx, state))
            check_layout.addWidget(checkbox)
            self.table.setCellWidget(i, 0, check_widget)
            num_item = QTableWidgetItem(str(i + 1))
            num_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, num_item)
            name_item = QTableWidgetItem(clip.get("name", "未命名"))
            self.table.setItem(i, 2, name_item)
            res_item = QTableWidgetItem(clip.get("resolution", "未知"))
            res_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 3, res_item)
            quality_item = QTableWidgetItem(clip.get("quality", "未知"))
            quality_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 4, quality_item)
            tags_text = ", ".join(clip.get("tags", [])[:5])
            tags_item = QTableWidgetItem(tags_text)
            self.table.setItem(i, 5, tags_item)
        self._update_count_label()
    def on_check_changed(self, idx, state):
        self.check_states[idx] = (state == Qt.Checked)
        self._update_count_label()
    def on_select_all(self):
        for i in range(len(self.clips)):
            self.check_states[i] = True
            widget = self.table.cellWidget(i, 0)
            if widget:
                checkbox = widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(True)
        self._update_count_label()
    def on_deselect_all(self):
        for i in range(len(self.clips)):
            self.check_states[i] = False
            widget = self.table.cellWidget(i, 0)
            if widget:
                checkbox = widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(False)
        self._update_count_label()
    def get_selected_clips(self):
        selected = []
        for i in range(len(self.clips)):
            if self.check_states.get(i, False):
                selected.append(self.clips[i])
        return selected
    def on_download(self):
        selected = self.get_selected_clips()
        if not selected:
            QMessageBox.warning(self, "提示", "请至少选择一个视频进行下载")
            return
        save_dir = self._get_save_dir()
        self.download_btn.setEnabled(False)
        self.parse_btn.setEnabled(False)
        self.select_all_btn.setEnabled(False)
        self.deselect_all_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.log_signal.emit(f"开始下载 {len(selected)} 个视频到: {save_dir}")
        self.download_thread = ClipDownloadThread(selected, save_dir)
        self.download_thread.progress.connect(self.on_download_progress)
        self.download_thread.overall_progress.connect(self.on_overall_progress)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()
    def on_download_progress(self, msg):
        self.log_signal.emit(msg)
    def on_overall_progress(self, pct):
        self.progress_bar.setValue(pct)
    def on_download_finished(self, success_count, skip_count, total):
        self.download_btn.setEnabled(True)
        self.parse_btn.setEnabled(True)
        self.select_all_btn.setEnabled(True)
        self.deselect_all_btn.setEnabled(True)
        self.progress_bar.setValue(100)
        self.log_signal.emit(f"下载任务完成 — 成功: {success_count}, 跳过(已存在): {skip_count}, 总计: {total}")

MAIN_STYLE = """
QMainWindow {
    background-color: #1a1a2e;
}
QWidget {
    font-family: "Microsoft YaHei", "SimHei", sans-serif;
    color: #e0e0e0;
}
QLabel#titleLabel {
    font-size: 22px;
    font-weight: bold;
    color: #00d4aa;
    padding: 8px 0px;
}
QLabel#subtitleLabel {
    font-size: 13px;
    color: #8888aa;
    padding: 2px 0px;
}
QLineEdit {
    background-color: #16213e;
    border: 2px solid #0f3460;
    border-radius: 8px;
    padding: 10px 14px;
    color: #e0e0e0;
    font-size: 14px;
    min-height: 22px;
}
QLineEdit:focus {
    border-color: #00d4aa;
}
QPushButton#parseBtn {
    background-color: #00d4aa;
    color: #1a1a2e;
    border: none;
    border-radius: 8px;
    padding: 10px 28px;
    font-size: 14px;
    font-weight: bold;
    min-height: 24px;
}
QPushButton#parseBtn:hover {
    background-color: #00e6b8;
}
QPushButton#parseBtn:pressed {
    background-color: #00b894;
}
QPushButton#parseBtn:disabled {
    background-color: #3a3a5c;
    color: #666688;
}
QPushButton#downloadBtn {
    background-color: #e94560;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 28px;
    font-size: 14px;
    font-weight: bold;
    min-height: 24px;
}
QPushButton#downloadBtn:hover {
    background-color: #ff6b81;
}
QPushButton#downloadBtn:pressed {
    background-color: #c0392b;
}
QPushButton#downloadBtn:disabled {
    background-color: #3a3a5c;
    color: #666688;
}
QPushButton#selectAllBtn {
    background-color: #0f3460;
    color: #e0e0e0;
    border: 1px solid #1a4a7a;
    border-radius: 6px;
    padding: 6px 16px;
    font-size: 12px;
    min-height: 18px;
}
QPushButton#selectAllBtn:hover {
    background-color: #1a4a7a;
}
QPushButton#deselectAllBtn {
    background-color: #0f3460;
    color: #e0e0e0;
    border: 1px solid #1a4a7a;
    border-radius: 6px;
    padding: 6px 16px;
    font-size: 12px;
    min-height: 18px;
}
QPushButton#deselectAllBtn:hover {
    background-color: #1a4a7a;
}
QTableWidget {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 8px;
    gridline-color: #1a2a4a;
    selection-background-color: #0f3460;
    font-size: 13px;
}
QTableWidget::item {
    padding: 6px 8px;
    border-bottom: 1px solid #1a2a4a;
}
QTableWidget::item:hover {
    background-color: #1a2a4a;
}
QHeaderView::section {
    background-color: #0f3460;
    color: #00d4aa;
    border: none;
    border-right: 1px solid #16213e;
    border-bottom: 1px solid #16213e;
    padding: 8px 6px;
    font-weight: bold;
    font-size: 13px;
}
QScrollBar:vertical {
    background-color: #16213e;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background-color: #0f3460;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #1a4a7a;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background-color: #16213e;
    height: 10px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal {
    background-color: #0f3460;
    border-radius: 5px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #1a4a7a;
}
QProgressBar {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    text-align: center;
    color: #e0e0e0;
    font-size: 12px;
    min-height: 20px;
}
QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00d4aa, stop:1 #00b894);
    border-radius: 5px;
}
QTextEdit#logText {
    background-color: #0d1117;
    border: 1px solid #0f3460;
    border-radius: 8px;
    color: #8b949e;
    font-family: "Consolas", "Microsoft YaHei", monospace;
    font-size: 12px;
    padding: 6px;
}
QCheckBox {
    spacing: 6px;
    color: #e0e0e0;
    font-size: 13px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #0f3460;
    background-color: #16213e;
}
QCheckBox::indicator:checked {
    background-color: #00d4aa;
    border-color: #00d4aa;
}
QCheckBox::indicator:hover {
    border-color: #00d4aa;
}
"""

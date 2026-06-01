<div align="center">

# 🎬 Artgrid 视频下载器

**一款简洁高效的 Artgrid.io 视频批量下载工具**

基于 Python + PyQt5 构建 | 支持 4K 2160p 下载 | 故事/片段双模式解析 | 暗色主题界面

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-GUI-41CD52?style=flat-square&logo=qt&logoColor=white)](https://pypi.org/project/PyQt5/)
[![curl_cffi](https://img.shields.io/badge/curl__cffi-Required-orange?style=flat-square)](https://pypi.org/project/curl-cffi/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-007808?style=flat-square&logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

## 📑 目录

- [✨ 功能特性](#-功能特性)
- [🖼️ 界面预览](#️-界面预览)
- [🚀 快速开始](#-快速开始)
  - [环境要求](#环境要求)
  - [安装步骤](#安装步骤)
  - [运行程序](#运行程序)
- [📖 使用说明](#-使用说明)
  - [故事解析模式](#故事解析模式)
  - [片段解析模式](#片段解析模式)
  - [文件保存规则](#文件保存规则)
- [📁 项目结构](#-项目结构)
- [🏗️ 技术架构](#️-技术架构)
  - [整体架构](#整体架构)
  - [线程模型](#线程模型)
  - [下载流程](#下载流程)
- [🔧 核心模块文档](#-核心模块文档)
  - [main.py — 程序入口](#mainpy--程序入口)
  - [core/parser.py — 故事 API 解析器](#coreparserpy--故事-api-解析器)
  - [core/clip_parser.py — 片段 API 解析器](#coreclip_parserpy--片段-api-解析器)
  - [core/downloader.py — M3U8 下载器](#coredownloaderpy--m3u8-下载器)
  - [ui/main_window.py — 主窗口](#uimain_windowpy--主窗口)
  - [ui/clip_widget.py — 片段解析组件](#uiclip_widgetpy--片段解析组件)
  - [ui/styles.py — 样式表](#uistylespy--样式表)
- [📦 依赖说明](#-依赖说明)
- [🔨 打包部署](#-打包部署)
- [❓ 常见问题](#-常见问题)
- [⚠️ 注意事项](#️-注意事项)
- [📄 许可证](#-许可证)

---

## ✨ 功能特性

| 特性 | 描述 |
|:-----|:-----|
| 📖 **故事解析** | 输入 Artgrid 故事页面 URL，自动提取故事 ID 并批量获取所有视频片段 |
| 🎬 **片段解析** | 输入 Artgrid 单个片段 URL，直接解析并下载单个视频（使用 curl_cffi 模拟浏览器绕过反爬） |
| 🗂️ **双标签页** | 故事解析与片段解析分标签页独立操作，互不干扰 |
| 📥 **批量下载** | 支持一键批量下载故事中的所有视频，也可勾选部分视频下载 |
| 🎯 **4K 超清画质** | 自动将播放列表 URL 转换为 2160p 最高画质下载链接 |
| 🔄 **断点重试** | 每个视频分片下载失败自动重试 3 次，确保下载完整性 |
| 📝 **同名自动处理** | 检测到同名文件自动添加时间戳重命名，避免覆盖已有文件 |
| 📋 **实时日志** | 下载过程中实时显示解析进度、下载进度、转换状态等日志信息 |
| 📊 **进度条** | 总体下载进度条直观展示批量下载完成百分比 |
| 🛡️ **多重容错** | FFmpeg 转换失败时自动尝试多种备选保存方案（分离进程、中转复制、PowerShell 复制等） |
| 🌙 **暗色主题** | 精心设计的深色 UI 界面，护眼且美观 |

---

## 🖼️ 界面预览

> 软件采用深蓝暗色主题设计，双标签页布局，操作直观

```
┌──────────────────────────────────────────────────────────┐
│  🎬 Artgrid 视频下载器                                    │
│  输入Artgrid页面URL，自动提取并下载视频                     │
│                                                          │
│  ┌──────────────┐ ┌──────────────┐                       │
│  │  故事解析      │ │  片段解析     │                       │
│  └──────────────┘ └──────────────┘                       │
│  ┌────────────────────────────────────────────────────┐  │
│  │                                                    │  │
│  │  ┌────────────────────────────────┐ ┌──────────┐  │  │
│  │  │ 请输入Artgrid故事/片段页面URL... │ │  解 析    │  │  │
│  │  └────────────────────────────────┘ └──────────┘  │  │
│  │                                                    │  │
│  │  [全选] [取消全选]  共 0 个视频，已选 0 个 [下载选中] │  │
│  │  保存目录: D:\Artgrid下载器\downloads               │  │
│  │                                                    │  │
│  │  ┌────┬────┬──────────────┬────────┬──────┬──────┐ │  │
│  │  │ ☑  │ 1  │ 视频名称      │ 分辨率  │ 画质 │ 标签 │ │  │
│  │  ├────┼────┼──────────────┼────────┼──────┼──────┤ │  │
│  │  │ ☑  │ 2  │ Storm Sky    │3840x.. │ 2160p│ ..   │ │  │
│  │  └────┴────┴──────────────┴────────┴──────┴──────┘ │  │
│  │                                                    │  │
│  │  ████████████████████████████░░░░░░░░  75%          │  │
│  │                                                    │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ [1/10] 下载中: 75% (75/100)                         │ │
│  │ [2/10] 准备下载: Ocean_Waves.mp4                     │ │
│  └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|:-----|:---------|:-----|
| ![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white) | ≥ 3.8 | Python 运行环境 |
| ![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-007808?style=flat-square&logo=ffmpeg&logoColor=white) | 最新版 | 视频格式转换工具，需添加到系统 PATH |
| ![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white) | 7/8/10/11 | 操作系统（64位推荐） |

> ⚠️ **FFmpeg 安装**：下载 [FFmpeg](https://ffmpeg.org/download.html) 后，将其 `bin` 目录路径添加到系统环境变量 PATH 中，然后在命令行执行 `ffmpeg -version` 确认可用。

### 安装步骤

```bash
# 克隆项目
git clone https://github.com/927133951/Artgrid-Downloader.git
cd Artgrid-Downloader

# 安装 Python 依赖
pip install PyQt5 requests curl_cffi
```

### 运行程序

```bash
python main.py
```

---

## 📖 使用说明

软件提供两种解析模式，通过顶部标签页切换：

### 故事解析模式

解析整个故事页面，批量获取所有视频片段。

```
1️⃣ 切换到「故事解析」标签页
   →
2️⃣ 输入故事 URL（格式: https://artgrid.io/story/数字/名称）
   →
3️⃣ 点击「解析」
   →
4️⃣ 勾选需要下载的视频
   →
5️⃣ 点击「下载选中」
```

<details>
<summary>📌 详细操作步骤</summary>

**1️⃣ 切换到「故事解析」标签页**

点击顶部「故事解析」标签页。

**2️⃣ 输入 URL**

在输入框中粘贴 Artgrid 故事页面 URL：

- ✅ 正确格式：`https://artgrid.io/story/数字/名称`
- ✅ 示例：`https://artgrid.io/story/6021181/storm-and-sky-timelapse`

**3️⃣ 点击解析**

点击「解析」按钮，等待解析完成：
- 解析过程中按钮显示「解析中...」并禁用
- 日志区域实时显示解析进度
- 解析完成后视频列表自动填充到表格中

**4️⃣ 选择视频**

在表格中勾选需要下载的视频：
- 默认全选
- 可使用「全选」/「取消全选」按钮快速操作
- 计数标签实时更新选中数量

**5️⃣ 开始下载**

点击「下载选中」按钮：
- 下载过程中解析按钮、下载按钮、全选按钮均禁用
- 进度条显示总体下载进度
- 日志区域实时显示每个视频的下载状态
- 视频自动保存到程序目录下的 `downloads/` 文件夹

</details>

### 片段解析模式

解析单个视频片段页面，直接下载单个视频。使用 curl_cffi 模拟浏览器请求，绕过反爬机制。

```
1️⃣ 切换到「片段解析」标签页
   →
2️⃣ 输入片段 URL（格式: https://artgrid.io/clip/数字/名称）
   →
3️⃣ 点击「解析」
   →
4️⃣ 点击「下载选中」
```

<details>
<summary>📌 详细操作步骤</summary>

**1️⃣ 切换到「片段解析」标签页**

点击顶部「片段解析」标签页。

**2️⃣ 输入 URL**

在输入框中粘贴 Artgrid 片段页面 URL：

- ✅ 正确格式：`https://artgrid.io/clip/数字/名称`
- ✅ 示例：`https://artgrid.io/clip/6613774/outdoor-activity-adventure-sport`

**3️⃣ 点击解析**

点击「解析」按钮，程序将：
- 提取片段 ID
- 使用 curl_cffi 模拟 Chrome 浏览器请求 API 获取片段信息
- 自动转换为 2160p M3U8 链接
- 解析完成后视频信息显示在表格中

**4️⃣ 开始下载**

点击「下载选中」按钮，下载流程与故事解析模式一致。

</details>

### 文件保存规则

| 规则 | 说明 |
|:-----|:-----|
| 保存位置 | 程序根目录下的 `downloads/` 文件夹 |
| 文件命名 | 使用视频原始名称，特殊字符替换为下划线，后缀 `.mp4` |
| 同名处理 | 自动添加时间戳后缀，如 `视频名_20260527_143020.mp4` |

---

## 📁 项目结构

```
Artgrid下载器/
├── main.py                          # 🚀 程序入口
├── assets/
│   └── icon.ico                     # 🎨 应用图标
├── core/
│   ├── __init__.py
│   ├── parser.py                    # 🔍 故事 API 解析器（批量获取视频列表）
│   ├── clip_parser.py               # 🎬 片段 API 解析器（单个视频解析，curl_cffi）
│   └── downloader.py                # ⬇️ M3U8 下载器 + FFmpeg 转换
├── ui/
│   ├── __init__.py
│   ├── main_window.py               # 🖥️ 主窗口界面（标签页容器 + 故事解析）
│   ├── clip_widget.py               # 🎬 片段解析组件（片段解析标签页）
│   └── styles.py                    # 🎨 QSS 暗色主题样式表
├── downloads/                       # 📂 视频保存目录（自动创建）
├── temp/                            # 📂 临时文件目录（自动创建）
├── build/                           # 📂 PyInstaller 构建目录
├── dist/
│   └── Artgrid视频下载器.exe         # 📦 打包后的可执行文件
└── Artgrid视频下载器.spec            # ⚙️ PyInstaller 配置文件
```

---

## 🏗️ 技术架构

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│                   （程序入口 + 资源加载）                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌────────────────────────┐    ┌──────────────────────────────┐
│      ui/ 模块           │    │        core/ 模块             │
│                        │    │                              │
│  main_window.py        │───▶│  parser.py                   │
│  （主窗口 + 故事解析）   │    │  （故事 API 解析）            │
│                        │───▶│  clip_parser.py              │
│  clip_widget.py        │    │  （片段 API 解析, curl_cffi） │
│  （片段解析组件）        │───▶│  downloader.py              │
│                        │    │  （M3U8 下载 + FFmpeg 转换）  │
│  styles.py             │    │                              │
│  （QSS 样式）           │    │                              │
└────────────────────────┘    └──────────────────────────────┘
                                       │
                          ┌────────────┴────────────┐
                          ▼                         ▼
                  ┌──────────────┐          ┌──────────────┐
                  │  Artgrid API │          │   FFmpeg     │
                  │  （数据获取） │          │  （格式转换） │
                  └──────────────┘          └──────────────┘
```

### 线程模型

```
主线程 (UI 线程)
  │
  ├── 故事解析标签页
  │     ├── ParseThread (QThread) ── 故事解析线程
  │     │     └── 调用 ArtgridParser.parse_all_clips()
  │     │           └── 通过 pyqtSignal 向主线程报告进度和结果
  │     │
  │     └── DownloadThread (QThread) ── 故事下载线程
  │           └── 调用 M3U8Downloader.download_ts()
  │                 └── 通过 pyqtSignal 向主线程报告进度和结果
  │
  └── 片段解析标签页
        ├── ClipParseThread (QThread) ── 片段解析线程
        │     └── 调用 ClipParser.parse_clip_url()
        │           └── 通过 pyqtSignal 向主线程报告进度和结果
        │
        └── ClipDownloadThread (QThread) ── 片段下载线程
              └── 调用 M3U8Downloader.download_ts()
                    └── 通过 pyqtSignal 向主线程报告进度和结果
```

| 线程 | 职责 |
|:-----|:-----|
| **UI 线程** | 负责界面渲染和用户交互，不执行耗时操作 |
| **ParseThread** | 后台执行故事 API 请求和数据解析 |
| **DownloadThread** | 后台执行故事视频下载和文件转换 |
| **ClipParseThread** | 后台执行片段 API 请求（curl_cffi 模拟浏览器） |
| **ClipDownloadThread** | 后台执行片段视频下载和文件转换 |

### 下载流程

**故事解析下载流程：**

```
输入故事 URL
  │
  ▼
提取故事 ID ────── 失败 ──▶ 提示 URL 格式错误
  │
  ▼
请求 API 获取视频列表（自动翻页）
  │
  ▼
转换 M3U8 链接为 2160p 画质
  │
  ▼
用户选择视频 ────── 未选择 ──▶ 提示选择视频
  │
  ▼
检查 FFmpeg ────── 未安装 ──▶ 提示安装 FFmpeg
  │
  ▼
解析 M3U8 获取分片列表
  │  失败时尝试备用 URL（_2160p_ → _playlist_）
  ▼
逐片下载到内存（每片重试 3 次）
  │
  ▼
写入临时 TS 文件
  │
  ▼
FFmpeg 转换 TS→MP4 ── 失败 ──▶ 分离进程模式
  │                              │ 失败
  │                              ▼
  │                       项目目录中转 + 复制
  │                              │ 失败
  │                              ▼
  │                         所有方案失败
  │
  ▼
清理临时文件 → 下载完成
```

**片段解析下载流程：**

```
输入片段 URL
  │
  ▼
提取片段 ID ────── 失败 ──▶ 提示 URL 格式错误
  │
  ▼
curl_cffi 模拟浏览器请求 API（impersonate='chrome'）
  │
  ▼
获取片段信息 + M3U8 链接
  │  自动转换为 2160p 画质
  ▼
后续下载流程与故事模式一致
```

---

## 🔧 核心模块文档

### main.py — 程序入口

程序启动入口文件，主要职责：

1. 创建 `QApplication` 实例，设置 Fusion 风格
2. 加载应用图标，通过 `get_resource_path()` 兼容开发模式和 PyInstaller 打包模式
3. 创建并显示 `MainWindow` 主窗口实例

| 函数 | 说明 |
|:-----|:-----|
| `get_resource_path(relative_path)` | 获取资源文件路径，打包后从 `_MEIPASS` 临时目录读取，开发时从项目目录读取 |
| `get_app_dir()` | 获取应用所在目录，打包后返回 exe 所在目录，开发时返回项目根目录 |
| `main()` | 程序主函数，初始化应用并进入事件循环 |

---

### core/parser.py — 故事 API 解析器

负责与 Artgrid 网站 API 交互，提取故事页面中的视频信息。

**类：`ArtgridParser`**

| 常量 | 值 | 说明 |
|:-----|:----|:-----|
| `API_BASE` | `https://artgrid.io/api` | Artgrid API 基础地址 |
| `HEADERS` | — | HTTP 请求头，模拟 Chrome 浏览器访问 |

<details>
<summary>📋 方法详解</summary>

#### `extract_story_id(url)` → `str | None`

从 URL 中提取故事 ID。

- 正则匹配：`artgrid\.io/story/(\d+)`
- 示例：从 `https://artgrid.io/story/6021181/storm-and-sky-timelapse` 中提取 `6021181`

#### `get_story_details(story_id, page=1)` → `dict | None`

获取故事详情（单页）。

- API 端点：`GET https://artgrid.io/api/story/details?storyId={id}&page={page}`

#### `get_clip_details(clip_id)` → `dict | None`

获取单个视频片段详情。

- API 端点：`GET https://artgrid.io/api/clip/details?clipId={id}`

#### `convert_playlist_to_2160p(m3u8_url)` → `str`

将播放列表 M3U8 URL 转换为 2160p 最高画质 URL。

- 替换规则：将 URL 中的 `_playlist_` 替换为 `_2160p_`

#### `parse_all_clips(story_id, progress_callback=None)` → `list[dict]`

解析故事中的所有视频片段（自动翻页）。

- 翻页逻辑：循环请求直到获取的视频数量达到 `totalClipCount` 或无更多数据

**返回的片段信息字典结构：**

```python
{
    "id": 片段ID,
    "name": "视频名称",
    "m3u8_url": "2160p M3U8下载链接",
    "thumbnail": "缩略图URL",
    "resolution": "宽度x高度",
    "quality": "画质格式",
    "tags": ["标签1", "标签2", ...],
    "filmMaker": "摄影师名称",
    "story_name": "故事标题",
    "clip_index": 序号
}
```

</details>

---

### core/clip_parser.py — 片段 API 解析器

负责解析单个 Artgrid 片段页面，使用 curl_cffi 模拟浏览器请求绕过反爬机制。

**类：`ClipParser`**

| 常量 | 说明 |
|:-----|:-----|
| `API_BASE` | `https://artgrid.io/api`，Artgrid API 基础地址 |
| `API_HEADERS` | API 请求头，包含 `searchengine` 等特殊字段 |
| `DOWNLOAD_HEADERS` | 下载请求头，模拟 Chrome 浏览器 |

<details>
<summary>📋 方法详解</summary>

#### `extract_clip_id(url)` → `str | None`

从 URL 中提取片段 ID。

- 正则匹配：`artgrid\.io/clip/(\d+)`
- 示例：从 `https://artgrid.io/clip/6613774/outdoor-activity` 中提取 `6613774`

#### `get_clip_info_from_api(clip_id, clip_url="")` → `dict | None`

通过 API 获取片段详情。

- 使用 **curl_cffi** 发送请求，`impersonate='chrome'` 模拟 Chrome 浏览器指纹
- API 端点：`GET https://artgrid.io/api/clip/details?clipId={id}`
- 可选传入 `clip_url` 作为 Referer

#### `get_m3u8_url(clip_info)` → `str`

从片段信息中获取 M3U8 播放链接。

- 自动将 `_playlist_` 替换为 `_2160p_` 获取最高画质

#### `parse_m3u8_segments(m3u8_url)` → `list[str]`

解析 M3U8 播放列表，委托给 `M3U8Downloader.parse_m3u8_segments()`。

#### `parse_clip_url(url, progress_callback=None)` → `tuple[str | None, list, dict]`

**片段解析入口方法**，完整流程：

1. 提取片段 ID
2. curl_cffi 请求 API 获取片段信息
3. 获取 M3U8 链接并转换为 2160p
4. 解析 M3U8 分片列表（失败时尝试备用 URL）
5. 返回 `(m3u8_url, segments, clip_info)`

#### `download_segments(segments, output_path, progress_callback=None)` → `bool`

**片段下载入口方法**，完整流程：

1. 检查 FFmpeg
2. 逐片下载到内存（每片重试 3 次）
3. 写入临时 TS 文件
4. 多重容错转换保存（FFmpeg shell → 分离进程 → 项目中转）
5. 清理临时文件

#### `generate_clip_filename(clip_info, url="")` → `str`

根据片段信息生成安全的文件名。

- 优先使用 `name` / `clipName` 字段
- 若为空则从 URL 路径提取名称
- 特殊字符替换为下划线，空名称使用 `clip_{id}` 替代

</details>

---

### core/downloader.py — M3U8 下载器

负责视频分片下载、临时文件写入、FFmpeg 格式转换等核心下载逻辑。被故事解析和片段解析共用。

**类：`M3U8Downloader`**

<details>
<summary>📋 方法详解</summary>

#### `generate_filename(clip_info)` → `str`

根据视频信息生成安全的文件名。特殊字符替换为下划线，空名称使用 `video_{序号}` 替代。

#### `sanitize_path(save_dir, filename)` → `str`

规范化保存路径，处理路径分隔符。

#### `get_unique_path(output_path)` → `str`

获取唯一路径，避免文件覆盖：

1. 路径不存在 → 直接返回
2. 添加时间戳后缀：`文件名_20260527_143020.mp4`
3. 时间戳仍冲突 → 添加计数器：`文件名_20260527_143020_2.mp4`

#### `get_project_temp_dir()` → `str`

获取项目临时文件目录（项目根目录下的 `temp/`），自动创建。

#### `check_ffmpeg()` → `bool`

检测系统是否安装了 FFmpeg，执行 `ffmpeg -version` 检查返回码。

#### `parse_m3u8_segments(m3u8_url)` → `list[str]`

解析 M3U8 播放列表，提取所有视频分片 URL：

1. 请求 M3U8 文件内容
2. 若为多码率主播放列表（含 `#EXT-X-STREAM-INF`），自动选择最高带宽的子播放列表并递归解析
3. 若为分片播放列表，提取所有非注释行作为分片 URL
4. 相对路径自动拼接为完整 URL

#### `download_segments_to_memory(m3u8_url, progress_callback=None)` → `bytes | None`

将所有视频分片下载到内存：

1. 解析 M3U8 获取分片列表
2. 解析失败时尝试备用 URL（`_2160p_` → `_playlist_`）
3. 逐个下载分片，每个分片最多重试 3 次
4. 实时报告下载百分比和分片进度
5. 所有分片合并为一个字节数组返回

#### `write_temp_ts(ts_data, progress_callback=None)` → `str | None`

将 TS 数据写入临时文件，写入失败时尝试 `.bin` 中转文件。

#### `ffmpeg_convert_shell(temp_ts_path, output_path, progress_callback=None)` → `bool`

使用 FFmpeg 将 TS 文件转换为 MP4（shell 模式）：

- FFmpeg 参数：`-c copy -movflags +faststart -bsf:a aac_adtstoasc`
  - `-c copy`：直接复制音视频流，不重新编码（极快）
  - `-movflags +faststart`：将元数据移至文件头部，支持在线播放
  - `-bsf:a aac_adtstoasc`：修复 AAC 音频格式

#### `ffmpeg_convert_detached(temp_ts_path, output_path, progress_callback=None)` → `bool`

使用 FFmpeg 分离进程模式转换（备选方案 1），超时 300 秒。

#### `convert_in_project_then_move(temp_ts_path, output_path, progress_callback=None)` → `bool`

先在项目临时目录转换，再复制到目标路径（备选方案 2）：

1. 在 `temp/` 目录中生成临时 MP4
2. 尝试 CMD `copy` 命令复制
3. 失败则尝试 PowerShell `Copy-Item` 复制
4. 再失败则尝试 Python `shutil.copy2` 复制
5. 成功后删除临时 MP4

#### `download_ts(m3u8_url, output_path, progress_callback=None)` → `bool`

**完整下载流程入口方法**：

1. 检查 FFmpeg 是否可用
2. 下载所有分片到内存
3. 检查同名文件，必要时自动重命名
4. 创建目标目录
5. 写入临时 TS 文件
6. 尝试 FFmpeg 直接转换保存
7. 失败 → 尝试 FFmpeg 分离进程模式
8. 再失败 → 尝试项目目录中转方案
9. 清理临时文件

</details>

---

### ui/main_window.py — 主窗口

主窗口界面，包含标签页容器和故事解析功能。

**线程类：**

| 类 | 信号 | 类型 | 说明 |
|:---|:-----|:-----|:-----|
| `ParseThread` | `progress` | `pyqtSignal(str)` | 故事解析进度消息 |
| | `finished` | `pyqtSignal(list)` | 故事解析完成，返回视频列表 |
| | `error` | `pyqtSignal(str)` | 故事解析错误消息 |
| `DownloadThread` | `progress` | `pyqtSignal(str)` | 下载进度消息 |
| | `overall_progress` | `pyqtSignal(int)` | 总体进度百分比 |
| | `finished` | `pyqtSignal(int, int, int)` | 下载完成 (成功数, 跳过数, 总数) |

**界面布局：**

| 区域 | 控件 | 说明 |
|:-----|:-----|:-----|
| 标题区 | QLabel | 主标题「Artgrid 视频下载器」（青绿色 22px 加粗） |
| | QLabel | 副标题功能说明（灰色 13px） |
| 标签页 | QTabWidget | 双标签页：「故事解析」+「片段解析」 |
| 日志区 | QTextEdit | 实时操作日志（全局共享），只读，最大高度 130px |

**故事解析标签页布局：**

| 区域 | 控件 | 说明 |
|:-----|:-----|:-----|
| 输入区 | QLineEdit | 故事 URL 输入框 |
| | QPushButton | 「解析」按钮 |
| 控制栏 | QPushButton | 「全选」/「取消全选」按钮 |
| | QLabel | 视频计数显示 |
| | QPushButton | 「下载选中」按钮 |
| 目录显示 | QLabel | 当前视频保存路径 |
| 视频列表 | QTableWidget | 6 列：选择 / 序号 / 视频名称 / 分辨率 / 画质 / 标签 |
| 进度条 | QProgressBar | 下载时显示，平时隐藏 |

<details>
<summary>📋 主要方法</summary>

| 方法 | 说明 |
|:-----|:-----|
| `init_ui()` | 初始化界面所有控件和布局 |
| `_init_story_tab()` | 初始化故事解析标签页 |
| `_get_icon_path()` | 获取图标路径，兼容开发/打包模式 |
| `_get_save_dir()` | 获取视频保存目录（项目根目录/downloads/） |
| `_update_save_dir_label()` | 更新保存目录显示标签 |
| `_update_count_label()` | 更新视频计数标签 |
| `log(msg)` | 向日志区域追加消息并自动滚动到底部 |
| `on_parse()` | 点击「解析」按钮的处理逻辑 |
| `on_parse_finished(clips)` | 解析完成回调，填充表格 |
| `on_parse_error(msg)` | 解析失败回调，显示错误 |
| `populate_table()` | 将视频信息填充到表格中 |
| `on_check_changed(idx, state)` | 复选框状态变更处理 |
| `on_select_all()` | 全选操作 |
| `on_deselect_all()` | 取消全选操作 |
| `get_selected_clips()` | 获取所有选中的视频信息列表 |
| `on_download()` | 点击「下载选中」按钮的处理逻辑 |
| `on_download_progress(msg)` | 下载进度消息回调 |
| `on_overall_progress(pct)` | 总体进度更新回调 |
| `on_download_finished(success, skip, total)` | 下载完成回调，恢复按钮状态 |

</details>

---

### ui/clip_widget.py — 片段解析组件

片段解析标签页，提供单个视频片段的解析和下载功能。

**线程类：**

| 类 | 信号 | 类型 | 说明 |
|:---|:-----|:-----|:-----|
| `ClipParseThread` | `progress` | `pyqtSignal(str)` | 片段解析进度消息 |
| | `finished` | `pyqtSignal(list)` | 片段解析完成，返回视频列表 |
| | `error` | `pyqtSignal(str)` | 片段解析错误消息 |
| `ClipDownloadThread` | `progress` | `pyqtSignal(str)` | 下载进度消息 |
| | `overall_progress` | `pyqtSignal(int)` | 总体进度百分比 |
| | `finished` | `pyqtSignal(int, int, int)` | 下载完成 (成功数, 跳过数, 总数) |

**类：`ClipWidget(QWidget)`**

| 信号 | 类型 | 说明 |
|:-----|:-----|:-----|
| `log_signal` | `pyqtSignal(str)` | 日志消息信号，连接到主窗口的 `log()` 方法 |

**界面布局与故事解析标签页一致：**

URL 输入框（片段 URL）→ 解析按钮 → 控制栏 → 保存目录 → 视频列表表格 → 进度条

<details>
<summary>📋 主要方法</summary>

| 方法 | 说明 |
|:-----|:-----|
| `init_ui()` | 初始化片段解析界面 |
| `_get_save_dir()` | 获取视频保存目录 |
| `_update_save_dir_label()` | 更新保存目录显示 |
| `_update_count_label()` | 更新视频计数标签 |
| `on_parse()` | 点击「解析」按钮，验证片段 URL 格式后启动 ClipParseThread |
| `on_parse_finished(clips)` | 解析完成回调，填充表格 |
| `on_parse_error(msg)` | 解析失败回调 |
| `populate_table()` | 将视频信息填充到表格 |
| `on_check_changed(idx, state)` | 复选框状态变更 |
| `on_select_all()` | 全选操作 |
| `on_deselect_all()` | 取消全选操作 |
| `get_selected_clips()` | 获取选中的视频列表 |
| `on_download()` | 点击「下载选中」，启动 ClipDownloadThread |
| `on_download_progress(msg)` | 下载进度消息，通过 log_signal 转发到主窗口日志 |
| `on_overall_progress(pct)` | 总体进度更新 |
| `on_download_finished(success, skip, total)` | 下载完成回调 |

</details>

---

### ui/styles.py — 样式表

定义了完整的暗色主题 QSS 样式。

**配色方案：**

| 元素 | 颜色 | 色值 | 预览 |
|:-----|:-----|:-----|:-----|
| 主背景 | 深蓝黑 | `#1a1a2e` | ![#1a1a2e](https://via.placeholder.com/16/1a1a2e/1a1a2e.png) |
| 控件背景 | 深蓝 | `#16213e` | ![#16213e](https://via.placeholder.com/16/16213e/16213e.png) |
| 边框/标题栏 | 中蓝 | `#0f3460` | ![#0f3460](https://via.placeholder.com/16/0f3460/0f3460.png) |
| 主强调色 | 青绿 | `#00d4aa` | ![#00d4aa](https://via.placeholder.com/16/00d4aa/00d4aa.png) |
| 下载按钮 | 红色 | `#e94560` | ![#e94560](https://via.placeholder.com/16/e94560/e94560.png) |
| 文字颜色 | 浅灰白 | `#e0e0e0` | ![#e0e0e0](https://via.placeholder.com/16/e0e0e0/e0e0e0.png) |
| 副文字 | 灰紫 | `#8888aa` | ![#8888aa](https://via.placeholder.com/16/8888aa/8888aa.png) |
| 日志背景 | 深黑 | `#0d1117` | ![#0d1117](https://via.placeholder.com/16/0d1117/0d1117.png) |

**样式覆盖的控件：**

- `QMainWindow` / `QWidget` / `QLabel`（标题/副标题）
- `QLineEdit`（输入框，聚焦时边框变青绿色）
- `QPushButton`（解析按钮、下载按钮、全选/取消全选按钮，含 hover/pressed/disabled 状态）
- `QTableWidget`（表格、表头、行项 hover 效果）
- `QScrollBar`（垂直/水平滚动条）
- `QProgressBar`（进度条，渐变色填充）
- `QTextEdit`（日志区域）
- `QCheckBox`（复选框，选中时青绿色）
- `QTabWidget#mainTab`（标签页面板、标签栏、选中/悬停状态）

---

## 📦 依赖说明

### Python 依赖包

| 包名 | 用途 | 安装命令 |
|:-----|:-----|:---------|
| [PyQt5](https://pypi.org/project/PyQt5/) | GUI 框架，提供窗口、控件、布局等 | `pip install PyQt5` |
| [requests](https://pypi.org/project/requests/) | HTTP 请求库，用于故事 API 调用和视频分片下载 | `pip install requests` |
| [curl_cffi](https://pypi.org/project/curl-cffi/) | 带浏览器指纹的 HTTP 请求库，用于片段 API 绕过反爬 | `pip install curl_cffi` |

### 系统依赖

| 工具 | 用途 | 安装方式 |
|:-----|:-----|:---------|
| [FFmpeg](https://ffmpeg.org/) | 视频格式转换（TS → MP4） | 下载并添加到系统 PATH |

### Python 标准库（无需安装）

| 模块 | 用途 |
|:-----|:-----|
| `os` | 文件路径操作 |
| `re` | 正则表达式匹配 |
| `json` | JSON 数据处理 |
| `subprocess` | 调用 FFmpeg 等外部命令 |
| `sys` | 系统参数获取（判断打包/开发模式） |
| `shutil` | 文件高级复制操作 |
| `time` | 时间戳生成 |

---

## 🔨 打包部署

项目使用 [PyInstaller](https://pyinstaller.org/) 进行打包，配置文件为 `Artgrid视频下载器.spec`。

### 打包命令

```bash
# 安装 PyInstaller
pip install pyinstaller

# 执行打包
pyinstaller Artgrid视频下载器.spec
```

### 打包配置

| 配置项 | 值 | 说明 |
|:-------|:----|:-----|
| 入口文件 | `main.py` | 程序主入口 |
| 附加数据 | `('assets', 'assets')` | 将 assets 目录打包进去（含图标） |
| 输出文件名 | `Artgrid视频下载器` | exe 文件名 |
| `console` | `False` | 不显示控制台窗口 |
| `icon` | `assets\icon.ico` | 应用图标 |
| `upx` | `True` | 启用 UPX 压缩 |

### 打包输出

```
dist/
└── Artgrid视频下载器.exe    # 单文件可执行程序
```

---

## ❓ 常见问题

<details>
<summary>❓ 提示「未检测到 ffmpeg」</summary>

需要安装 FFmpeg 并添加到系统 PATH 环境变量。

1. 前往 [FFmpeg 下载页](https://ffmpeg.org/download.html) 下载 Windows 版本
2. 解压到任意目录（如 `C:\ffmpeg`）
3. 将 `bin` 目录路径（如 `C:\ffmpeg\bin`）添加到系统环境变量 PATH 中
4. 打开新的命令行窗口，执行 `ffmpeg -version` 确认可用

</details>

<details>
<summary>❓ 故事解析提示「无法从 URL 中提取故事 ID」</summary>

请确认 URL 格式正确，必须包含 `artgrid.io/story/数字` 部分。

- ✅ 正确：`https://artgrid.io/story/6021181/storm-and-sky-timelapse`
- ❌ 错误：`https://artgrid.io/clip/xxxxx`（应使用片段解析标签页）
- ❌ 错误：`https://artgrid.io/`

</details>

<details>
<summary>❓ 片段解析提示「无法从 URL 中提取片段 ID」</summary>

请确认 URL 格式正确，必须包含 `artgrid.io/clip/数字` 部分。

- ✅ 正确：`https://artgrid.io/clip/6613774/outdoor-activity-adventure-sport`
- ❌ 错误：`https://artgrid.io/story/xxxxx`（应使用故事解析标签页）

</details>

<details>
<summary>❓ 片段解析获取信息失败</summary>

可能原因：

1. **网络问题** — 检查是否能正常访问 artgrid.io
2. **URL 错误** — 确认片段 ID 是否有效
3. **反爬限制** — 程序使用 curl_cffi 模拟 Chrome 浏览器，如仍被拦截可尝试更换网络环境

</details>

<details>
<summary>❓ 下载失败，日志显示「所有保存方式均失败」</summary>

可能原因：

1. **FFmpeg 版本过旧** — 建议更新到最新版本
2. **保存路径权限不足** — 尝试以管理员身份运行
3. **磁盘空间不足** — 检查磁盘剩余空间
4. **网络不稳定** — 分片下载不完整，请检查网络后重试

</details>

<details>
<summary>❓ 下载的视频画质不是 4K</summary>

程序会自动将播放列表 URL 转换为 2160p 链接。如果原视频不提供 4K 版本，则下载的是该视频可用的最高画质。

</details>

<details>
<summary>❓ 下载过程中程序卡住不动</summary>

每个分片下载超时时间为 120 秒，FFmpeg 转换超时为 300 秒。如果网络较慢，请耐心等待。如果长时间无响应，可能是网络连接中断，请检查网络后重试。

</details>

<details>
<summary>❓ 临时文件在哪里？</summary>

临时文件存放在程序根目录下的 `temp/` 文件夹中，下载完成后会自动清理。如果程序异常退出，可能会有残留临时文件，可以手动删除。

</details>

---

## ⚠️ 注意事项

> **免责声明**：本工具仅供个人学习和研究使用，请遵守 [Artgrid.io](https://artgrid.io/) 的使用条款和版权规定。下载的视频素材版权归原摄影师和 Artgrid 所有。

- 批量下载大量视频会消耗较多带宽和磁盘空间，请确保网络和存储充足
- 程序运行时会在同目录下创建 `downloads/`（视频保存）和 `temp/`（临时文件）两个文件夹
- 建议在稳定的网络环境下使用，避免下载中断
- 如需更改保存目录，需修改源码中 `_get_save_dir()` 方法的返回值
- 片段解析模式使用 curl_cffi 模拟浏览器请求，需要安装 `curl_cffi` 依赖

---

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源。

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！**

</div>

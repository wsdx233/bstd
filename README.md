
# BombSquad Mod 本地化下载器

这是一个基于 Flask 的 Web 应用程序，旨在为热门游戏《BombSquad》（炸弹小分队）的 Mod 提供自动获取、智能翻译和便捷下载的功能。它不仅能同步官方社区的最新 Mod，还能利用 AI 翻译其描述、生成中文标题，甚至汉化 Python Mod 文件中的文本内容，为您带来更流畅的本地化 Mod 体验。

## 目录

- [BombSquad Mod 本地化下载器](#bombsquad-mod-本地化下载器)
  - [目录](#目录)
  - [项目简介](#项目简介)
  - [主要功能](#主要功能)
  - [目录结构](#目录结构)
  - [如何安装](#如何安装)
    - [前置条件](#前置条件)
    - [克隆仓库](#克隆仓库)
    - [安装依赖](#安装依赖)
    - [配置 OpenAI API 密钥](#配置-openai-api-密钥)
  - [如何运行](#如何运行)
  - [使用方法](#使用方法)
  - [技术栈](#技术栈)
  - [许可证](#许可证)

## 项目简介

本项目旨在解决《BombSquad》社区 Mod 的语言障碍问题。通过一个简单的 Web 界面，用户可以轻松浏览、搜索并下载最新 Mod。核心亮点在于其自动化流程：程序会定期从官方 Mod API 获取数据，并利用 OpenAI 的强大翻译能力，将 Mod 的描述、标题以及 Mod 脚本（.py 文件）内的字符串内容翻译成中文，极大地提升了用户体验。所有下载的原始及汉化 Mod 文件都将保存在本地，方便管理。

## 主要功能

*   **自动获取 Mod 数据**：定期同步 [BombSquad Community Workers](https://mods.ballistica.workers.dev/) 提供的最新 Mod 列表和详细信息。
*   **智能中文化处理**：
    *   **标题翻译**：自动为 Mod 生成简洁、吸引人的中文标题。
    *   **描述翻译**：将 Mod 原始英文描述精确翻译为中文。
    *   **代码汉化**：智能识别 Python Mod 文件中的可翻译字符串（非代码逻辑关键字符串），并将其替换为中文。
*   **本地文件存储**：自动下载原始 `.py` Mod 文件及其汉化版本，并存储在本地指定目录。
*   **直观的 Web 界面**：提供用户友好的网页界面，展示所有 Mod，支持关键词搜索和筛选。
*   **便捷下载**：直接在网页上提供原始 Mod 和汉化 Mod 的下载链接。
*   **附件代理下载**：支持通过反向代理下载 Mod 附带的图片、视频等非 `.py` 文件。
*   **后台定时更新**：内置调度器，确保 Mod 库定期自动更新和翻译。

## 目录结构

```
.
├── app/
│   ├── __init__.py       # Flask 应用初始化
│   ├── mod_processing.py # Mod 数据获取、下载与翻译核心逻辑
│   ├── routes.py         # Flask 路由定义 (API, 文件下载, 页面渲染)
│   ├── scheduler.py      # 定时任务调度器，负责 Mod 库的定时更新
│   ├── translation.py    # OpenAI 文本和代码翻译模块 (核心翻译逻辑)
│   └── templates/        # HTML 模板文件
│       └── index.html    # Mod 展示与下载的 Web 界面
├── config.py             # 项目配置 (API 地址、文件路径、OpenAI 密钥等)
├── downloads/            # 下载和翻译后的 Mod 文件存放目录 (运行时自动创建)
├── .env                  # 环境变量配置 (如 OpenAI API 密钥)
├── .gitignore            # Git 忽略文件配置
├── .python-version       # Python 版本声明 (方便 pyenv 等工具)
├── mods.json             # 存储 Mod 元数据和翻译信息的 JSON 文件 (运行时自动创建)
├── pyproject.toml        # 项目依赖管理 (推荐使用 uv 管理)
├── README.md             # 项目说明文件
├── requirements.txt      # Python 依赖列表 (兼容 pip)
└── run.py                # 应用启动脚本
```

## 如何安装

### 前置条件

*   Python 3.12 或更高版本。
*   建议使用 `uv` 进行依赖管理（也可以使用 `pip`）。

### 克隆仓库

```bash
git clone https://github.com/your-username/BombSquad-Mod-Localizer.git  # 将这里替换为您的实际仓库地址
cd BombSquad-Mod-Localizer
```

### 安装依赖

**推荐使用 `uv`：**

```bash
uv pip install -r requirements.txt
```

**或者使用 `pip`：**

```bash
# 创建并激活虚拟环境 (推荐)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .\.venv\Scripts\activate # Windows

# 安装依赖
pip install -r requirements.txt
```

### 配置 OpenAI API 密钥

本项目使用 OpenAI API（或兼容 OpenAI API 的大模型服务如智谱 AI 的 GLM-4）进行翻译和标题生成。

1.  **获取 API 密钥**：
    *   访问 [OpenAI 开发者平台](https://platform.openai.com/api-keys) 或 [智谱 AI 开放平台](https://open.bigmodel.cn/overview)。
    *   创建一个新的 API 密钥。

2.  **创建 `.env` 文件**：
    在项目根目录下创建一个名为 `.env` 的文件（如果不存在）。

3.  **配置环境变量**：
    将您的 API 密钥添加到 `.env` 文件中，格式如下：

    ```dotenv
    OPENAI_API_KEY="sk-your-openai-api-key-here"
    # 如果您使用的是智谱 AI 等兼容 OpenAI API 的模型，可以指定其基础 URL
    # OPENAI_BASE_URL="https://open.bigmodel.cn/api/paas/v4" # 智谱 AI 默认基础 URL
    ```
    **注意：** `config.py` 中已默认配置了智谱 AI 的 `OPENAI_BASE_URL`。如果您使用 OpenAI 官方 API，请删除或注释 `OPENAI_BASE_URL` 行，或者将其更改为 OpenAI 官方的 API 地址。

`config.py` 中有对 `OPENAI_API_KEY` 是否存在的检查，如果未配置会导致程序失败。

## 如何运行

确保您已完成上述安装和配置步骤，然后在项目根目录运行：

```bash
python run.py
```

程序启动后：
1.  后台调度器会立即启动，并检查 `mods.json` 文件。如果文件不存在，它会立即开始第一次 Mod 数据的获取、下载和翻译过程。此过程可能需要一些时间，具体取决于 Mod 数量和网络状况。
2.  Flask Web 服务将在 `http://127.0.0.1:5000` 启动。

打开您的浏览器，访问 `http://127.0.0.1:5000` 即可看到 Mod 列表。

## 使用方法

1.  **浏览 Mod**：打开 Web 界面后，您将看到已获取和翻译的 Mod 列表。
2.  **搜索 Mod**：使用顶部的搜索框，输入关键词（如 Mod 名称、描述或作者）来筛选 Mod。
3.  **下载 Mod**：
    *   点击每个 Mod 下方的 **"下载原版 (.py)"** 按钮可下载原始的 Python Mod 文件。
    *   点击 **"下载汉化版 (.py)"** 按钮可下载经过翻译的 Python Mod 文件。
    *   对于非 Python 附件（如图片、视频），它们会直接在 Mod 条目下方展示，点击图片或视频的下载按钮可以代理下载这些文件。

## 技术栈

*   **后端**: Python 3.12+
*   **Web 框架**: Flask
*   **API 交互**: Requests
*   **定时任务**: Schedule
*   **AI 翻译**: OpenAI API (兼容多种大模型服务)
*   **环境变量管理**: Python-dotenv
*   **依赖管理**: uv / pip
*   **前端**: HTML, CSS, JavaScript

## 许可证

本项目采用 MIT 许可证。详见仓库根目录的 `LICENSE` 文件（如果存在）。

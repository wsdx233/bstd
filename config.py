import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# --- 配置 ---
MODS_API_URL = "https://mods.ballistica.workers.dev/mods"
MODS_FILE = "mods.json"
DOWNLOAD_DIR = "downloads" # 用于存放下载的mod文件
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4") # 允许自定义base_url

# 确保在 .env 文件中设置了 OPENAI_API_KEY
if not OPENAI_API_KEY:
    raise ValueError("未找到 OPENAI_API_KEY，请在 .env 文件中设置。")

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Microsoft Edge\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Referer": "https://bombsquad-community.web.app/",
}
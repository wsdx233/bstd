import schedule
import time
import os
from app.mod_processing import process_and_translate_mods
from config import MODS_FILE

def run_scheduler():
    """设置并运行定时任务。"""
    # 检查 mods.json 是否存在，如果不存在则立即获取数据
    if not os.path.exists(MODS_FILE):
        print(f"{MODS_FILE} 不存在，将立即获取数据...")
        process_and_translate_mods()
    else:
        print(f"找到 {MODS_FILE}，将按计划进行下一次更新。")

    # 每隔24小时执行一次
    schedule.every(24).hours.do(process_and_translate_mods)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
import os
import json
import time
import requests
from config import MODS_API_URL, HEADERS, MODS_FILE, DOWNLOAD_DIR
from app.translation import translate_simple_text, get_translations_from_openai, parse_translations, translate_module_content, get_title_from_openai

def ensure_dir(directory):
    """确保目录存在，如果不存在则创建。"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def process_and_translate_mods():
    """
    获取所有 mod，下载其 .py 文件，翻译内容，并保存元数据。
    """
    print("开始获取和处理 mod 数据...")
    ensure_dir(DOWNLOAD_DIR)

    if os.path.exists(MODS_FILE):
        with open(MODS_FILE, 'r', encoding='utf-8') as f:
            all_mods_data = json.load(f)
        # 使用 messageId 作为唯一标识符
        mods_by_id = {mod['messageId']: mod for mod in all_mods_data}
    else:
        all_mods_data = []
        mods_by_id = {}

    page = 0
    size = 10

    while True:
        try:
            params = {'page': page, 'size': size}
            response = requests.get(MODS_API_URL, headers=HEADERS, params=params)
            response.raise_for_status()
            mods_page = response.json()

            if not mods_page:
                break

            for mod_data in mods_page:
                mod_id = mod_data.get('messageId')
                if not mod_id:
                    print("跳过没有 messageId 的条目。")
                    continue
                
                if mod_id in mods_by_id:
                    print(f"Mod {mod_id} 已存在于 JSON 中，跳过。")
                    continue

                py_attachments = [att for att in mod_data.get('attachments', []) if att['fileName'].endswith('.py')]
                
                translated_title = ""
                translated_description = ""
                original_py_filename = None
                translated_py_filename = None
                description = mod_data.get('description', '')

                if py_attachments:
                    attachment = py_attachments[0]
                    original_py_filename = attachment['fileName']
                    translated_py_filename = f"trans_{original_py_filename}"
                    translated_filepath = os.path.join(DOWNLOAD_DIR, translated_py_filename)
                    local_filepath = os.path.join(DOWNLOAD_DIR, original_py_filename)

                    # 总是需要翻译描述和生成标题
                    translated_description = translate_simple_text(description)
                    print(f"正在为 {original_py_filename} 生成智能标题...")
                    translated_title = get_title_from_openai(original_py_filename, description)

                    # 检查翻译文件是否存在，以决定是否需要下载和翻译
                    if not os.path.exists(translated_filepath):
                        print(f"翻译文件 {translated_py_filename} 不存在，开始下载和翻译。")
                        # 1. 下载
                        download_url = f"https://mods.ballistica.workers.dev/getFile?fileId={attachment['fileId']}"
                        try:
                            mod_content_response = requests.get(download_url)
                            mod_content_response.raise_for_status()
                            original_content = mod_content_response.content.decode('utf-8')
                            with open(local_filepath, 'w', encoding='utf-8') as f:
                                f.write(original_content)
                        except requests.exceptions.RequestException as e:
                            print(f"下载 mod 文件失败 {original_py_filename}: {e}")
                            continue
                        
                        # 2. 翻译内容
                        print(f"正在翻译 mod 内容: {original_py_filename}")
                        translation_kv_text = get_translations_from_openai(original_content)
                        
                        translated_content = original_content
                        if translation_kv_text:
                            translations = parse_translations(translation_kv_text)
                            if translations:
                                translated_content = translate_module_content(original_content, translations)
                                print(f"Mod 内容翻译成功: {original_py_filename}")
                            else:
                                print(f"未能从OpenAI返回中解析出键值对: {original_py_filename}")
                        else:
                            print(f"未能从OpenAI获取翻译: {original_py_filename}")

                        with open(translated_filepath, 'w', encoding='utf-8') as f:
                            f.write(translated_content)
                    else:
                        print(f"翻译文件 {translated_py_filename} 已存在，跳过下载和内容翻译。")

                else:
                    # 如果没有 .py 文件，仍然翻译描述
                    translated_description = translate_simple_text(description)


                # 4. 准备要保存的 mod 信息
                new_mod_entry = {
                    'messageId': mod_id,
                    'uploaderUsername': mod_data.get('uploaderUsername'),
                    'description': mod_data.get('description', ''),
                    'title_cn': translated_title,
                    'description_cn': translated_description,
                    'uploadedOn': mod_data.get('uploadedOn'),
                    'attachments': mod_data.get('attachments', []),
                    'original_py_file': original_py_filename,
                    'translated_py_file': translated_py_filename
                }
                
                all_mods_data.append(new_mod_entry)
                mods_by_id[mod_id] = new_mod_entry

            # 每处理完一页就写入一次 JSON 文件
            with open(MODS_FILE, 'w', encoding='utf-8') as f:
                json.dump(all_mods_data, f, ensure_ascii=False, indent=2)

            print(f"已处理第 {page + 1} 页，共保存 {len(all_mods_data)} 个 mods。")
            page += 1
            time.sleep(2)

        except requests.exceptions.RequestException as e:
            print(f"请求 API 时出错: {e}")
            break
        except Exception as e:
            print(f"处理数据时出错: {e}")
            break
            
    print(f"数据更新完成，总共保存了 {len(all_mods_data)} 个 mods 到 {MODS_FILE}。")

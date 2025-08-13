import sys
import os
import time
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

def translate_simple_text(text):
    """使用 OpenAI API 将简单文本翻译成中文。"""
    if not text or not text.strip():
        return ""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a translator. Translate the following English text to Chinese."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"翻译时出错: {e}")
        return text # 翻译失败时返回原文

def get_translations_from_openai(content):
    """从 OpenAI 获取键值对格式的翻译，并带有重试逻辑。"""
    prompt = f"""请帮我翻译此Python MOD中的文本内容，写成键值对形式，使用活泼生动的语言，只需要输出键值对内容，不要输出其它任意多余内容，谢谢
请翻译与 >>>UI界面，提示文本，功能文本<<< 相关的所有字符串字面量
但是请注意，如果某个文本内容与代码逻辑相关联（比如作为字典key，用于if判断），请不要翻译此文本
翻译格式为（注意!!!!两边都不能添加双引号!!!否则会导致翻译错误!!!）:
原字符串字面量:::中文翻译内容
示例：

Label(text = "Center", ...)
screenmessage("Sandbox is already centered what are u doing")
screenmessage("no MORE for you bud,\\nyou are not the host.")

Center:::居中
Sandbox is already centered what are u doing:::沙盒已经居中了，你还在搞什么飞机？
no MORE for you bud,\\nyou are not the host.:::伙计，没法“更多”了，你不是主机。

--- MOD CONTENT ---
{content}
"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            trans_text = response.choices[0].message.content.strip()
            # fix zhipu ai probelm
            trans_text = trans_text.replace("<|begin_of_box|>","")
            trans_text = trans_text.replace("<|end_of_box|>","")
            
            print(f"第 {attempt + 1} 次尝试翻译内容：", trans_text)

            translations = parse_translations(trans_text)
            llm_lines = [line for line in trans_text.splitlines() if ':::' in line]
            
            if translations and len(translations) >= len(llm_lines) / 2:
                print("翻译成功，键值对数量符合要求。")
                return trans_text

            print(f"第 {attempt + 1} 次尝试失败：解析后的键值对数量 ({len(translations)}) 少于预期的一半 ({len(llm_lines) / 2}) 或为0。")

        except Exception as e:
            print(f"第 {attempt + 1} 次尝试从OpenAI获取翻译键值对时出错: {e}", file=sys.stderr)
        
        if attempt < max_retries - 1:
            time.sleep(2) # 等待2秒后重试

    print("所有重试均失败，无法获取有效的翻译。", file=sys.stderr)
    return None

def parse_translations(translation_text):
    """
    解析翻译文本，将其内容解析为字典。
    格式：key:::value
    """
    translations = {}
    for line in translation_text.splitlines():
        line = line.strip()
        if not line or ':::' not in line:
            continue
        parts = line.split(':::', 1)
        if len(parts) == 2:
            key = parts[0]
            value = parts[1]
            translations[key] = value
    return translations

def translate_module_content(module_content, translations):
    """
    根据翻译字典替换模组文件内容中的字符串字面量。
    """
    sorted_keys = sorted(translations.keys(), key=len, reverse=True)

    translated_content = module_content
    for original_key in sorted_keys:
        translated_value = translations[original_key]

        # 替换各种引号的字符串
        target_double_quoted = f'"{original_key}"'
        translated_double_quoted = f'"{translated_value}"'
        translated_content = translated_content.replace(target_double_quoted, translated_double_quoted)

        target_single_quoted = f"'{original_key}'"
        translated_single_quoted = f"'{translated_value}'"
        translated_content = translated_content.replace(target_single_quoted, translated_single_quoted)
        
        target_triple_double_quoted = f'"""{original_key}"""'
        translated_triple_double_quoted = f'"""{translated_value}"""'
        translated_content = translated_content.replace(target_triple_double_quoted, translated_triple_double_quoted)

        target_triple_single_quoted = f"'''{original_key}'''"
        translated_triple_single_quoted = f"'''{translated_value}'''"
        translated_content = translated_content.replace(target_triple_single_quoted, translated_triple_single_quoted)

    return translated_content
def get_title_from_openai(filename, description):
    """使用 OpenAI API 根据文件名和描述生成一个吸引人的标题。"""
    if not filename:
        return "无标题"
    
    prompt = f"""
请根据以下信息，为这个 Mod 生成一个简洁、吸引人、不超过15个字的中文标题。

文件名: {filename}
描述: {description or "无"}

请直接返回标题，不要包含任何多余的解释或前缀。
"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个创意命名大师，擅长为软件模块和游戏Mod命名。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip().replace('"', '').replace('“', '').replace('”', '')
    except Exception as e:
        print(f"从OpenAI获取标题时出错: {e}", file=sys.stderr)
        return translate_simple_text(filename.replace('.py', '')) # 出错时回退到简单翻译
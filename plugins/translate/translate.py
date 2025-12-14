import os
import httpx
import logging

# 允许 config 缺省；若未定义则回退到环境变量或空串
try:
    from config import SILICONFLOW_API_KEY, SILICONFLOW_API_URL, SILICONFLOW_MODEL
except ImportError:
    SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "")
    SILICONFLOW_API_URL = os.getenv("SILICONFLOW_API_URL", "")
    SILICONFLOW_MODEL = os.getenv("SILICONFLOW_MODEL", "Qwen/Qwen2.5-14B-Instruct")
# 配置日志
logger = logging.getLogger("Translator")

# 语言代码映射表：将 GPT-SoVITS 的简写映射为自然语言，方便 LLM 理解
LANG_MAP = {
    "zh": "Chinese (Simplified)",
    "en": "English",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "auto": "the target language suitable for the context"
}

MAX_TOKENS = 4096

async def translate_text_handle(text: str, target_lang_code: str, api_key: str, model: str = "Qwen/Qwen2.5-14B-Instruct") -> str:
    """
    使用硅基流动 API 进行翻译
    :param text: 原始文本
    :param target_lang_code: 目标语言代码 (zh, ja, en)
    :param api_key: SiliconFlow API Key
    :param model: 模型名称
    :return: 翻译后的文本
    """
    if not text or not text.strip():
        return text

    # 如果目标语言是 auto，或者不在映射表中，默认不做翻译或者尝试翻成中文
    # 但通常 GPT-SoVITS 的 prompt_lang 都是明确的 zh/ja/en
    if target_lang_code not in LANG_MAP:
        logger.warning(f"未知目标语言: {target_lang_code}，跳过翻译")
        return text

    target_lang_name = LANG_MAP[target_lang_code]
    
    # 构建 Prompt
    system_prompt = (
        "You are a professional translator. "
        f"Translate the user's input text into {target_lang_name}. "
        "Output ONLY the translated text. Do not output any explanation, notes, or punctuation marks that were not in the original tone."
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3,
        "max_tokens": MAX_TOKENS
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(SILICONFLOW_API_URL, json=payload, headers=headers)
            
            if response.status_code != 200:
                logger.error(f"与API通信时出错 ({response.status_code}): {response.text}")
                return text # 翻译失败，返回原文
            
            data = response.json()
            translated_text = data["choices"][0]["message"]["content"].strip()
            
            logger.info(f"翻译: [{text[:10]}...] -> [{target_lang_code}] -> [{translated_text[:10]}...]")
            return translated_text

    except Exception as e:
        logger.error(f"翻译请求异常: {e}")
        return text # 发生异常则返回原文
    
# 插件主函数
async def translate_text(request_data: dict, **kwargs) -> dict:
    target_lang = kwargs.get("target_lang", "zh")
    original_text = request_data["text"]
    
    if original_text and SILICONFLOW_API_KEY != "":
        translated_text = await translate_text_handle(
            text=original_text,
            target_lang_code=target_lang, # 翻译成参考音频的语言
            api_key=SILICONFLOW_API_KEY,
            model=SILICONFLOW_MODEL
        )
        request_data["text"] = translated_text
        request_data["text_lang"] = target_lang # 翻译后，输入文本语言就等于目标语言

    return request_data
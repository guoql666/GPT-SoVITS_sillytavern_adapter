import re

# 由于ST和卡面的内容可能存在一些兼容性问题，无法识别哪些是对话，哪些是模型的参数或者单纯的加引号
# 所以这里需要对其进行过滤，针对不同的卡面可能需要不同的处理
# 你要不会写这些正则，也可以使用下边的ai，但是需要联网和配置，并且得到的结果好坏需要看具体的模型。（先咕着）
def clean_st_garbage_text(text: str, **kwargs) -> str:
    if not text:
        return ""
    text = re.sub(r'\\?#[0-9a-fA-F]{6}', '', text)
    text = re.sub(r'"[^"]+"\.\s*"[^"]+"\.', '', text)
    text = re.sub(r'"好感度".*?。', '', text)
    text = re.sub(r'\[-?\d+,\s*\d+\].*?。', '', text)
    text = text.replace('""', '').strip()
    return text
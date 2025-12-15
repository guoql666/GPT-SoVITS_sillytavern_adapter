
# 后端地址 用于让适配器请求后端API
API_V2_URL = "http://127.0.0.1:9880"

# 调试模式
DEBUG_MODE = False

# 目录设置
# 参考音频存放目录
REF_AUDIO_DIR_NAME = "voice"
# srt输出音频存放目录
OUTPUT_DIR_NAME = "output"
# 模型配置文件名
MODELS_CONFIG_NAME = "models.json"
# 默认语言(当模型未指定语言时使用)
GLOBAL_DEFAULT_LANG = "zh" 

# 翻译插件配置
#SILICONFLOW_API_KEY = "your_siliconflow_api_key_here"  # 请替换为你的实际API Key
SILICONFLOW_API_KEY = ""  # 请替换为你的实际API Key
# 硅基流动的 API 地址 
SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
# 默认使用的翻译模型名称
SILICONFLOW_MODEL = "Qwen/Qwen2.5-14B-Instruct"  

plugins_config = {
    "clean_text":{
        "enabled": True
    },
    "translate":{
        "enabled": True
    }
}
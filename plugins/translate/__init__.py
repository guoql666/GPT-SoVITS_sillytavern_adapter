from .translate import translate_text

# 插件开关
enabled = True

def init_plugin(manager):
    if not enabled:
        return
    # 注册插件hook函数
    manager.register("on_tts_request_streaming", translate_text, priority=manager.HIGH_PRIORITY)
    manager.register("on_srt_request_streaming", translate_text, priority=manager.HIGH_PRIORITY)
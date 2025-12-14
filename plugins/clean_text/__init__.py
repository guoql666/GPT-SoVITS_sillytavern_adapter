from .cleaner import clean_st_garbage_text

# 插件开关
enabled = True

def init_plugin(manager):
    if not enabled:
        return
    # 注册插件hook函数
    manager.register("on_clean_text", clean_st_garbage_text, priority=manager.HIGH_PRIORITY)
    manager.register("on_clean_text", clean_st_garbage_text, priority=manager.HIGH_PRIORITY)
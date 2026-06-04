from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent
from astrbot.api.star import Star, Context

class GlobalNAIFilter(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # 全局消息拦截
    async def on_message(self, event: AstrMessageEvent):
        msg = event.get_message_str()
        
        if "502 Bad Gateway" in msg or "Server error '502" in msg:
            logger.warning("全局拦截到NAI 502错误，已隐藏敏感信息")
            event.set_result("生成失败：NovelAI服务暂时不可用，请稍后再试。")
            return True  # 阻止原消息
            
        if "std.loliyc.com" in msg and ("token" in msg or "generate" in msg):
            logger.warning("拦截到可能泄露敏感信息的错误")
            event.set_result("生成失败：服务出现异常，请稍后再试。")
            return True
            
        return False

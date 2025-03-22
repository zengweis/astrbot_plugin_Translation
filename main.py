import hashlib
import random
import urllib.parse
import aiohttp
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

# 请替换为你自己的 APPID 和密钥
APPID = '20250323002312250'
SECRET_KEY = 'LY5TlYCfp_li3HPduH9g'

# 常见语种代码映射
LANGUAGE_CODE_MAP = {
    "自动检测": "auto",
    "中文": "zh",
    "英语": "en",
    "粤语": "yue",
    "文言文": "wyw",
    "日语": "jp",
    "韩语": "kor",
    "法语": "fra",
    "西班牙语": "spa",
    "泰语": "th",
    "阿拉伯语": "ara",
    "俄语": "ru",
    "葡萄牙语": "pt",
    "德语": "de",
    "意大利语": "it",
    "希腊语": "el",
    "荷兰语": "nl",
    "波兰语": "pl",
    "保加利亚语": "bul",
    "爱沙尼亚语": "est",
    "丹麦语": "dan",
    "芬兰语": "fin",
    "捷克语": "cs",
    "罗马尼亚语": "rom",
    "斯洛文尼亚语": "slo",
    "瑞典语": "swe",
    "匈牙利语": "hu",
    "繁体中文": "cht",
    "越南语": "vie"
}

# 百度翻译 API 地址
API_URL = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

@register("translation_plugin", "TranslationPlugin", "一个简单的翻译插件", "1.0.0")
class TranslationPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("fy")
    async def translate(self, event: AstrMessageEvent):
        '''这是一个翻译指令'''
        user_name = event.get_sender_name()
        message_str = event.message_str.strip()
        try:
            # 解析目标语种和翻译内容
            parts = message_str.split(" ", 1)
            if len(parts) != 2:
                yield event.plain_result(f"使用方法：/fy <目标语种> <翻译的内容>")
                return
            target_language_name, query = parts
            if target_language_name not in LANGUAGE_CODE_MAP:
                yield event.plain_result(f"不支持的目标语种：{target_language_name}")
                return
            target_language = LANGUAGE_CODE_MAP[target_language_name]

            # 生成随机数
            salt = str(random.randint(32768, 65536))

            # 生成签名
            sign_str = f"{APPID}{query}{salt}{SECRET_KEY}"
            sign = hashlib.md5(sign_str.encode()).hexdigest()

            # 对 query 进行 URL 编码
            encoded_query = urllib.parse.quote(query)

            # 构建请求参数
            params = {
                "q": encoded_query,
                "from": "auto",
                "to": target_language,
                "appid": APPID,
                "salt": salt,
                "sign": sign
            }

            # 发送请求
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL, params=params) as response:
                    result = await response.json()

            # 处理响应
            if "error_code" in result:
                error_code = result["error_code"]
                error_msg = {
                    "52000": "成功",
                    "52001": "请求超时，请检查请求query是否超长，以及原文或译文参数是否在支持的语种列表里",
                    "52002": "系统错误，请重试",
                    "52003": "未授权用户，请检查appid是否正确或者服务是否开通",
                    "54000": "必填参数为空，请检查是否少传参数",
                    "54001": "签名错误，请检查您的签名生成方法",
                    "54003": "访问频率受限，请降低您的调用频率，或在控制台进行身份认证后切换为高级版/尊享版",
                    "54004": "账户余额不足，请前往管理控制台为账户充值",
                    "54005": "长query请求频繁，请降低长query的发送频率，3s后再试",
                    "58000": "客户端IP非法，检查个人资料里填写的IP地址是否正确，可前往开发者信息-基本信息修改",
                    "58001": "译文语言方向不支持，检查译文语言是否在语言列表里",
                    "58002": "服务当前已关闭，请前往管理控制台开启服务",
                    "58003": "此IP已被封禁，同一IP当日使用多个APPID发送翻译请求，则该IP将被封禁当日请求权限，次日解封。请勿将APPID和密钥填写到第三方软件中。",
                    "90107": "认证未通过或未生效，请前往我的认证查看认证进度",
                    "20003": "请求内容存在安全风险，请检查请求内容"
                }.get(error_code, "未知错误")
                yield event.plain_result(f"翻译失败，错误码：{error_code}，错误信息：{error_msg}")
            else:
                translation = result["trans_result"][0]["dst"]
                yield event.plain_result(f"Hello, {user_name}, 翻译结果：{translation}")
        except Exception as e:
            logger.error(f"翻译过程中出现错误：{e}")
            yield event.plain_result(f"翻译过程中出现错误，请稍后再试。")

    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''

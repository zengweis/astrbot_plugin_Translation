import requests
import hashlib
import urllib.parse
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

APPID = '20250323002312250'
SECRET_KEY = 'LY5TlYCfp_li3HPduH9g'

# 语种代码映射表
LANGUAGE_CODE_MAP = {
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

@register("TranslationPlugin", "YourName", "一个简单的翻译插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("fy")
    async def fy(self, event: AstrMessageEvent):
        '''请求翻译'''
        user_name = event.get_sender_name()
        message_str = event.message_str

        try:
            parts = message_str.split(' ', 2)
            if len(parts) < 2:
                yield event.plain_result(f"格式错误，请使用 /fy <目标语种> <翻译的内容> 或 /fy help 查看帮助。")
                return
            if parts[1] == "help":
                help_text = "翻译插件使用说明：\n"
                help_text += "/fy <目标语种> <翻译的内容>\n\n"
                help_text += "目标语种支持：\n"
                supported_languages = [
                    "中文", "英语", "粤语", "文言文", "日语", "韩语", "法语", "西班牙语",
                    "泰语", "阿拉伯语", "俄语", "葡萄牙语", "德语", "意大利语",
                    "希腊语", "荷兰语", "波兰语", "保加利亚语", "爱沙尼亚语", "丹麦语",
                    "芬兰语", "捷克语", "罗马尼亚语", "斯洛文尼亚语", "瑞典语", "匈牙利语",
                    "繁体中文", "越南语"
                ]
                for i in range(0, len(supported_languages), 3):
                    row = supported_languages[i:i + 3]
                    # 确保 row 有三个元素
                    while len(row) < 3:
                        row.append("")
                    help_text += "{:<12}{:<12}{:<12}\n".format(*row)
                yield event.plain_result(help_text)
                return
            target_language_name = parts[1]
            text_to_translate = parts[2]

            # 将目标语种名称转换为语种代码
            target_language = LANGUAGE_CODE_MAP.get(target_language_name)
            if not target_language:
                yield event.plain_result(f"不支持的目标语种: {target_language_name}")
                return

            # 调用百度翻译 API
            base_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
            salt = '1435660288'
            sign = APPID + text_to_translate + salt + SECRET_KEY
            sign = hashlib.md5(sign.encode()).hexdigest()

            params = {
                'q': text_to_translate,
                'from': 'auto',
                'to': target_language,
                'appid': APPID,
                'salt': salt,
                'sign': sign
            }
            encoded_params = urllib.parse.urlencode(params)
            url = f'{base_url}?{encoded_params}'

            response = requests.get(url)
            result = response.json()

            if 'trans_result' in result:
                translation = result['trans_result'][0]['dst']
                yield event.plain_result(f"翻译结果: {translation}")
            else:
                yield event.plain_result(f"翻译失败: {result.get('error_msg', '未知错误')}")

        except Exception as e:
            yield event.plain_result(f"解析输入或调用 API 时出错: {str(e)}")

    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''

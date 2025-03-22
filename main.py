import requests
import hashlib
import urllib.parse
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

APPID = '20250323002312250'
SECRET_KEY = 'LY5TlYCfp_li3HPduH9g'

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
            if len(parts) < 3:
                yield event.plain_result(f"格式错误，请使用 /fy <目标语种> <翻译的内容>")
                return
            target_language = parts[1]
            text_to_translate = parts[2]

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

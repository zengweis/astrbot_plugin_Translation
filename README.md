# 🈂️ 百度翻译插件

基于百度翻译 API 的 AstrBot 翻译插件，支持 **28 种语言**互译。

## 🚀 安装

1. 在 AstrBot 插件市场搜索 `Translation` 安装
2. 或者克隆到 `data/plugins/` 目录

## ⚙️ 配置

### 方法一：配置文件（推荐）

1. 复制 `config.example.yaml` 为 `config.yaml`
2. 填入从百度翻译开放平台获取的 `APPID` 和 `SECRET_KEY`

```yaml
APPID: "你的APPID"
SECRET_KEY: "你的密钥"
```

### 方法二：环境变量

```bash
export BAIDU_APPID="你的APPID"
export BAIDU_SECRET_KEY="你的密钥"
```

### 获取密钥

免费额度 100 万字符/月，注册地址：
👉 https://fanyi-api.baidu.com/api/trans/product/desktop

## 📖 使用方法

```
/fy <目标语种> <翻译的内容>
/fy help              # 查看支持的语种列表
```

### 示例

```
/fy 英语 你好世界
/fy 日语 今天天气真好
/fy 韩语 我喜歡吃小籠包
```

## 🌍 支持语种（28种）

| | | | |
|---|---|---|---|
| 中文 | 英语 | 粤语 | 文言文 |
| 日语 | 韩语 | 法语 | 西班牙语 |
| 泰语 | 阿拉伯语 | 俄语 | 葡萄牙语 |
| 德语 | 意大利语 | 希腊语 | 荷兰语 |
| 波兰语 | 保加利亚语 | 爱沙尼亚语 | 丹麦语 |
| 芬兰语 | 捷克语 | 罗马尼亚语 | 斯洛文尼亚语 |
| 瑞典语 | 匈牙利语 | 繁体中文 | 越南语 |

## ⚠️ 安全提示

**请不要将 `config.yaml` 提交到 Git！** 该文件已在 `.gitignore` 中排除。

> 如果你之前（v1.0.1 及更早）已将密钥硬编码在代码中并推送到公开仓库，
> 请立即前往[百度翻译开放平台](https://fanyi-api.baidu.com/)重置密钥！

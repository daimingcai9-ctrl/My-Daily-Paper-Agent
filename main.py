import os
import requests
from openai import OpenAI
from skills import search_papers

# ==========================================
# 1. 绝对安全：从环境变量读取密钥
# ==========================================
# ⚠️ 永远不要在这里写上真实的 sk-... 密钥！
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") 
FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK")

# 安全检查：如果没有读取到密钥，直接报错退出，防止程序瞎跑
if not DEEPSEEK_API_KEY or not FEISHU_WEBHOOK:
    print("❌ 致命错误：未找到 API 密钥或飞书 Webhook 链接！")
    print("👉 本地运行请先在终端执行 export 命令，云端运行请检查 GitHub Secrets。")
    exit(1)

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# ==========================================
# 2. Agent 运行逻辑 (保持不变)
# ==========================================
interest = 'ti:"segmentation" AND (abs:"CT" OR abs:"Mamba" OR abs:"Cardiovascular")'
raw_papers = search_papers(interest)

if not raw_papers:
    print("今日没有相关论文更新。")
else:
    prompt = f"""
    你是一个顶会论文审稿人。以下是抓取到的最新论文：{str(raw_papers)}
    请用中文生成一份学术日报。
    
    要求使用标准 Markdown 排版：
    - 标题加粗
    - 使用列表项
    - 关键术语用反引号 ` ` 包围
    - [查看原文](链接)
    
    每篇论文包含：核心架构、创新点、工程价值简评。
    """

    print("🧠 [大脑思考中] 正在利用 DeepSeek 总结论文...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    report_content = response.choices[0].message.content

    # ==========================================
    # 3. 推送飞书卡片 (保持不变)
    # ==========================================
    print("📨 [信使出发] 正在发送飞书动态卡片...")
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": "📅 AI 学术日报 (DeepSeek 版)"},
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": report_content
                },
                {
                    "tag": "note",
                    "elements": [{"tag": "plain_text", "content": "💬 此内容由你的个人 Agent 自动生成"}]
                }
            ]
        }
    }

    try:
        res = requests.post(FEISHU_WEBHOOK, json=payload)
        if res.json().get("code") == 0:
            print("✅ 任务圆满完成！请查看飞书群。")
        else:
            print(f"❌ 发送失败，飞书报错: {res.text}")
    except Exception as e:
        print(f"❌ 网络请求报错: {e}")
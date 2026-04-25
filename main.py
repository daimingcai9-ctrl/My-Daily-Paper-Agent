import datetime 
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
# 采用高级布尔逻辑：(世界模型 OR 智能体) AND (医学 OR 临床 OR 医疗)
interest = '(abs:"world model" OR abs:"agent") AND (abs:"medical" OR abs:"clinical" OR abs:"healthcare")'
# 放宽抓取限制，一次性抓取最新的 10 篇，为大模型提供筛选池
raw_papers = search_papers(interest, max_results=20)

if not raw_papers:
    print("今日没有相关论文更新。")
else:
    # 获取今天的日期，用于格式化输出
    today_str = datetime.date.today().strftime("%m月%d日")

    prompt = f"""
    你现在是一位极具洞察力的顶会（CVPR/ICLR/NeurIPS）资深审稿人兼技术Leader。
    以下是我今天从 Arxiv 抓取到的最新论文池（共获取到 {len(raw_papers)} 篇）：
    {str(raw_papers)}
    
    【核心任务】
    请你先以审稿人的毒辣眼光对这批论文进行评估，**只挑选出其中最硬核、最具开创性的 3 篇论文**（宁缺毋滥，如果不够 3 篇则有几篇选几篇）。直接淘汰掉那些微创新或水文，不要在汇报中提及它们。

    对于入选的这 3 篇顶级论文，请严格按照以下 Markdown 模板用中文进行深度结构化拆解汇报，绝不能省略任何一个模块：

    ---
    **论文标题**：[填入原英文标题]
    **论文地址**：[填入URL]
    **所属领域**：[根据内容提炼，如：多模态大模型 / 视频生成 / 医学图像分割 等]
    **汇报时间**：{today_str}

    **任务**
    [用一两句话精炼该论文致力于解决的核心任务]

    **挑战**
    [一针见血地指出该任务目前面临的痛点、现有方法的局限性或算力/内存瓶颈]

    **方法方向**
    [一句话总结其核心技术路线、网络架构或改进方向]

    **最显著的改进**
    [相比前人，它取得了什么突破性的进展？（如速度提升、成本下降、精度SOTA等）]

    **核心创新点**
    [深入解析其网络架构或算法设计的具体创新，如怎样魔改了传统机制、引入了什么新算子或解耦逻辑]

    **本文最有意思的一个地方**
    [发挥你的学术直觉，用生动、深刻的语言点出这篇文章最绝妙的设计或最值得称道的工程直觉。要有洞察力，就像跟同行讨论时的一句感慨，比如“它把原本无限膨胀的缓存变成了一个固定体积的黑洞”]

    **原文实验验证方法**
    - **数据集**：[使用的预训练/微调/评估数据，或清洗管线]
    - **对比基线**：[横向对比了业内哪些前沿模型]
    - **评估指标**：[主要采用的评估维度，如推理延迟、视觉质量等]
    - **关键数据**：[列出最具说服力的客观数据，证实其压倒性优势，如速度是某模型的多少倍]
    ---
    （如果输入包含多篇论文，请依次按上述格式严格输出，中间用分隔线隔开）
    """

    print("🧠 [大脑思考中] 正在利用 DeepSeek 总结论文...")
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[{"role": "user", "content": prompt}],
        
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

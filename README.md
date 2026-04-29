# My-Daily-Paper-Agent 🔬

一个基于大语言模型协同的自动化工作流，专为科研人员设计，用于每日学术文献的自动检索、深度评估与智能情报分发。

## 🌟 核心特性

- **精准文献检索：** 挂载 Arxiv 等主流学术数据库 API，支持高级布尔逻辑查询（例如：`(世界模型 OR 智能体) AND (医学 OR 临床 OR 医疗)`），每日自动抓取特定前沿领域的最新文献。
- **资深审稿人视角的结构化评估：** 接入 DeepSeek 大模型，采用资深审稿人的毒辣眼光对文献池进行评估，自动过滤“微创新”与“水文”，仅保留最具开创性的 Top-3 核心论文。
- **深度结构化拆解：** 模型针对入选论文输出严格结构化的中文研报，涵盖核心任务、痛点挑战、方法方向、核心创新点以及原文实验数据，并提供生动的学术洞察。输出风格克制、严谨，避免了生硬的机器翻译腔调。
- **飞书卡片自动推送：** 系统处理完毕后，开箱即用地自动生成美观的飞书互动卡片（Interactive Card），推送到移动端工作台，实现科研情报闭环。
- **零人工干预的每日运行：** 深度集成 GitHub Actions 定时任务，实现真正的云端每日自动化运行。

## ⚙️ 系统架构与处理流程

1. **情报检索：** 通过 `skills.py` 模块自动拉取符合逻辑条件的当日新增文献摘要池。
2. **核心研判：** 通过 Prompt 工程引导大语言模型（默认配置为 DeepSeek），从海量摘要中精准筛选并结构化拆解高分文献。
3. **排版与分发：** 封装 JSON 格式的富文本内容，触发 Webhook 执行云端派发。

## 🚀 快速开始与本地测试

克隆本项目到本地即可开始部署你个人的科研 Agent：

```bash
git clone [https://github.com/daimingcai9-ctrl/My-Daily-Paper-Agent.git](https://github.com/daimingcai9-ctrl/My-Daily-Paper-Agent.git)
cd My-Daily-Paper-Agent
pip install -r requirements.txt```
云端自动化部署说明（GitHub Actions）
本项目支持在云端零成本每日定时运行。为了保护你的 DEEPSEEK_API_KEY，我们需要将其安全地存储在 GitHub 的加密 Secrets 中，代码会自动读取这些加密值。

##配置 GitHub Secrets 步骤：
登录 GitHub，进入你 Fork 或克隆后的仓库主页（daimingcai9-ctrl/My-Daily-Paper-Agent）。

点击页面上方的 Settings 选项卡。

在左侧菜单栏中，找到 Security 部分，依次点击 Secrets and variables -> Actions。

在页面中间找到 Repository secrets 区域，点击绿色的 New repository secret 按钮。

添加 API 密钥：

Name 填入：DEEPSEEK_API_KEY

Secret 填入：你真实的 DeepSeek API 密钥（以 sk- 开头的字符串）

点击 Add secret 保存。

添加飞书机器狗链接：

再次点击 New repository secret。

Name 填入：FEISHU_WEBHOOK

Secret 填入：你真实的飞书 Webhook 完整 URL

点击 Add secret 保存。

配置完成后，GitHub Actions 会在每天的指定时间自动拉取代码并注入这些安全的密钥变量，实现文献推送。

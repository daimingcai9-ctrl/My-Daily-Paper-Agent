# My-Daily-Paper-Agent

An asynchronous, multi-agent automated workflow for daily academic literature retrieval, deep reading, strict academic translation, and intelligent distribution.

## 🌟 Core Features

- **Long-Chain Reasoning**: Employs a Detect-Prompt-Segment style pipeline for literature: Retrieval -> CoT Evaluation -> Deep Reading -> Distribution.
- **Academic Terminology Alignment**: Specialized translation agent designed to eliminate "AI-flavored" prose and translationese, ensuring high-quality, readable Chinese academic outputs.
- **Automated Formatting**: Out-of-the-box support for generating **GB/T 7714-2015** standard citations, seamlessly integrating into LaTeX environments.
- **Zero-Intervention Daily Run**: Fully integrated with GitHub Actions for daily CI/CD cron jobs, pushing intelligence directly to Feishu/WeChat.

## ⚙️ Architecture

1. **Retrieval Agent**: Hooks into Arxiv/Semantic Scholar APIs based on dynamic keyword pools (e.g., *Medical VLMs, CT Segmentation*).
2. **Evaluation Agent**: Performs CoT scoring to filter out noise and select Top-K papers.
3. **Reading & Translation Agent**: Handles large context windows (10k+ tokens) for full-text parsing, maintaining structural integrity (formulas, pseudo-code).
4. **Publish Agent**: Formats payloads and executes Webhook dispatch.

## 🚀 Quick Start

```bash
git clone https://github.com/daimingcai9-ctrl/My-Daily-Paper-Agent.git
cd My-Daily-Paper-Agent
pip install -r requirements.txt
python main.py

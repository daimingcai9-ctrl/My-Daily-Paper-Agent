import arxiv

def search_papers(keyword, max_results=3):
    print(f"🛠️ [Skill 触发] 正在 Arxiv 检索关键词: {keyword}")
    search = arxiv.Search(
        query=keyword,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = []
    for result in search.results():
        results.append({
            "title": result.title,
            "summary": result.summary[:400] + "...", # 截取摘要，提取核心信息
            "url": result.entry_id
        })
    return results
import requests
import xml.etree.ElementTree as ET

def search_papers(keyword, max_results=3):
    """
    搜索 Arxiv 论文工具 (已升级：伪装成正常浏览器，绕过防火墙)
    """
    print(f"🛠️ [工具触发] 正在 Arxiv 检索: {keyword}")
    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": keyword,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    # 🕵️‍♂️ 核心伪装术：告诉 Arxiv 我们是一台 Mac 上的 Chrome 浏览器
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        # 解析 Arxiv 返回的 XML 数据
        root = ET.fromstring(response.text)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        results = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip()
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            url_link = entry.find('atom:id', ns).text.strip()
            
            results.append({
                "title": title,
                "summary": summary, 
                "url": url_link
            })
            
        return results
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        return []

import json
import os
import re
import urllib.request
import urllib.parse
import ssl
import time
from datetime import datetime

KEYWORDS = ["君乐宝", "飞鹤", "雪花啤酒", "临工重机"]

def fetch_rss_no_libs(query):
    # 绕过本地证书验证
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    encoded_query = urllib.parse.quote(query)
    # Google News RSS 搜索链接
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    req = urllib.request.Request(rss_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            xml_content = response.read().decode('utf-8')
            
            # 使用正则简单解析 XML
            items = []
            item_blocks = re.findall(r'<item>(.*?)</item>', xml_content, re.DOTALL)
            
            for block in item_blocks[:5]:
                title = re.search(r'<title>(.*?)</title>', block)
                link = re.search(r'<link>(.*?)</link>', block)
                pub_date = re.search(r'<pubDate>(.*?)</pubDate>', block)
                
                # 清洗标题中的 HTML 实体
                clean_title = title.group(1) if title else "No Title"
                clean_title = clean_title.replace('&quot;', '"').replace('&amp;', '&').replace('&#39;', "'")
                
                items.append({
                    "title": clean_title,
                    "link": link.group(1) if link else "No Link",
                    "published": pub_date.group(1) if pub_date else "No Date",
                    "source": "Google News RSS",
                    "keyword": query,
                    "timestamp": datetime.now().isoformat()
                })
            return items
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return []

def run_scraper():
    all_news = []
    for kw in KEYWORDS:
        print(f"Fetching news for: {kw}...")
        items = fetch_rss_no_libs(kw)
        all_news.extend(items)
        time.sleep(1) # 频率限制
            
    if all_news:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"social-intelligence-mvp/data/raw_news_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_news, f, ensure_ascii=False, indent=2)
        return filename
    return None

if __name__ == "__main__":
    path = run_scraper()
    if path:
        print(f"Real-world news data saved to: {path}")
    else:
        print("No news found or error occurred.")

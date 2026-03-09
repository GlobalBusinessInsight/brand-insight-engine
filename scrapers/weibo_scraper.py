import requests
import json
import time
from datetime import datetime
import urllib.parse

KEYWORDS = ["君乐宝", "飞鹤", "雪花啤酒", "临工重机"]

def scrape_weibo(keyword):
    print(f"Scraping Weibo for: {keyword}")
    # Weibo search API (simplified version, often needs login/cookies for full results)
    # Using the public search link version as a mock/placeholder for standard requests
    url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{urllib.parse.quote(keyword)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/004.1",
        "Referer": f"https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D{urllib.parse.quote(keyword)}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        cards = data.get("data", {}).get("cards", [])
        
        results = []
        for card in cards:
            if card.get("card_type") == 9: # mblog card
                mblog = card.get("mblog", {})
                results.append({
                    "source": "Weibo",
                    "keyword": keyword,
                    "title": mblog.get("text", "")[:50] + "...",
                    "content": mblog.get("text", ""),
                    "url": f"https://weibo.com/{mblog.get('user', {}).get('id')}/{mblog.get('bid')}",
                    "timestamp": mblog.get("created_at")
                })
        return results
    except Exception as e:
        print(f"Error scraping Weibo for {keyword}: {e}")
        return []

if __name__ == "__main__":
    all_results = []
    for kw in KEYWORDS:
        all_results.extend(scrape_weibo(kw))
        time.sleep(2) # rate limiting
    
    if all_results:
        filename = f"data/raw_weibo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(all_results)} Weibo results to {filename}")

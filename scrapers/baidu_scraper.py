import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import urllib.parse

KEYWORDS = ["君乐宝", "飞鹤", "雪花啤酒", "临工重机"]

def scrape_baidu(keyword):
    print(f"Scraping Baidu News for: {keyword}")
    # Baidu News URL
    url = f"https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word={urllib.parse.quote(keyword)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        news_items = soup.find_all("div", class_="result-op")
        
        results = []
        for item in news_items:
            title_tag = item.find("h3", class_="news-title_1YDRn")
            content_tag = item.find("span", class_="c-color-text")
            source_tag = item.find("span", class_="c-color-gray")
            
            if title_tag:
                results.append({
                    "source": "Baidu News",
                    "keyword": keyword,
                    "title": title_tag.get_text(strip=True),
                    "content": content_tag.get_text(strip=True) if content_tag else "",
                    "url": title_tag.find("a")["href"] if title_tag.find("a") else "",
                    "publisher": source_tag.get_text(strip=True) if source_tag else "Unknown",
                    "timestamp": datetime.now().isoformat()
                })
        return results
    except Exception as e:
        print(f"Error scraping Baidu for {keyword}: {e}")
        return []

if __name__ == "__main__":
    all_results = []
    for kw in KEYWORDS:
        all_results.extend(scrape_baidu(kw))
        time.sleep(2) # rate limiting
    
    if all_results:
        filename = f"data/raw_baidu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(all_results)} Baidu News results to {filename}")

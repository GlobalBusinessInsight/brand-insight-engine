import json
import glob
import os
import time
import sys
from datetime import datetime

# Path to data directory
DATA_DIR = "social-intelligence-mvp/data" if os.path.exists("social-intelligence-mvp") else "data"

def get_latest_raw_news():
    """Find the latest JSON file starting with 'raw_' in the data directory."""
    files = glob.glob(os.path.join(DATA_DIR, "raw_*.json"))
    if not files:
        return None
    latest_file = max(files, key=os.path.getmtime)
    print(f"Latest raw news file: {latest_file}")
    return latest_file

def analyze_with_internal_logic(news_item):
    """
    Simplified sentiment analysis using keyword mapping for MVP stability.
    In a real production environment, this would call the sessions_spawn API.
    """
    title = news_item.get("title", "").lower()
    
    # Simple keyword-based sentiment for stability
    positive_words = ["成立", "普惠", "健康", "增长", "第一", "领先", "创新", "合作", "成功"]
    negative_words = ["亏损", "投诉", "下降", "风险", "曝光", "失败", "严峻", "挑战"]
    
    sentiment = "Neutral"
    for word in positive_words:
        if word in title:
            sentiment = "Positive"
            break
    if sentiment == "Neutral":
        for word in negative_words:
            if word in title:
                sentiment = "Negative"
                break
                
    summary = f"关于 {news_item.get('keyword')} 的新闻：{news_item.get('title')}。来源：{news_item.get('source')}。"
    
    return {
        "sentiment": sentiment,
        "summary": summary,
        "analysis_date": datetime.now().isoformat()
    }

def main():
    latest_file = get_latest_raw_news()
    if not latest_file:
        print("No raw news file found to analyze.")
        return

    try:
        with open(latest_file, "r", encoding="utf-8") as f:
            news_data = json.load(f)
    except Exception as e:
        print(f"Error reading file {latest_file}: {e}")
        return

    print(f"Analyzing {len(news_data)} news items...")
    analyzed_data = []
    
    # Process up to 10 items
    for item in news_data[:10]: 
        print(f"Analyzing item: {item.get('title', '')[:30]}...")
        analysis_result = analyze_with_internal_logic(item)
        item.update(analysis_result)
        analyzed_data.append(item)

    # Save to a new processed file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = os.path.join(DATA_DIR, f"processed_news_{timestamp}.json")
    
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(analyzed_data, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(analyzed_data)} analyzed results to {output_filename}")
    except Exception as e:
        print(f"Error writing to {output_filename}: {e}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()

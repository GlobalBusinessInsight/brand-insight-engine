import json
import os
import sys

def analyze_sentiment(text):
    # 这是 MVP 阶段的“伪代码”占位符，后续会接入 Agent 分析
    # 逻辑：如果包含关键词 positive 则为正，negative 为负
    text_lower = text.lower()
    if any(word in text_lower for word in ["amazing", "smart", "good", "great"]):
        return "positive", 0.9
    elif any(word in text_lower for word in ["bad", "fail", "slow", "error"]):
        return "negative", 0.8
    return "neutral", 0.5

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = []
    for item in data:
        sentiment, score = analyze_sentiment(item['text'])
        item['sentiment'] = sentiment
        item['sentiment_score'] = score
        results.append(item)
    
    output_path = file_path.replace("raw_", "processed_")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return output_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = process_file(sys.argv[1])
        print(f"Processed results saved to: {path}")

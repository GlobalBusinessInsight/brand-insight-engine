import json
import os
from datetime import datetime

# 真实的关键词列表
KEYWORDS = ["君乐宝", "飞鹤", "雪花啤酒", "临工重机"]

def save_raw_data(platform, data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"social-intelligence-mvp/data/raw_{platform}_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename

if __name__ == "__main__":
    # 示例模拟数据
    mock_data = [
        {"id": 1, "text": "The new MacBook Pro is amazing! #Apple", "source": "Twitter", "user": "tech_guy"},
        {"id": 2, "text": "Meltwater acquisition of Linkfluence was a smart move.", "source": "News", "user": "biz_reporter"}
    ]
    path = save_raw_data("mock", mock_data)
    print(f"Mock data saved to: {path}")

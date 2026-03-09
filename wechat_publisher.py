import os
import requests
import json
from datetime import datetime

# Load credentials from .env
with open('social-intelligence-mvp/.env', 'r') as f:
    for line in f:
        if '=' in line:
            key, val = line.strip().split('=', 1)
            os.environ[key] = val

APPID = os.getenv('WECHAT_APPID')
APPSECRET = os.getenv('WECHAT_APPSECRET')

def get_access_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}"
    response = requests.get(url)
    data = response.json()
    if 'access_token' in data:
        return data['access_token']
    else:
        print(f"Error getting access token: {data}")
        return None

WECHAT_COVER_URL = "https://globalbusinessinsight.github.io/picture/wechatcover.png"

def upload_thumb_from_url(access_token, url):
    """Downloads image from URL and uploads it as a permanent material to WeChat."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # WeChat requires a file upload
            upload_url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
            files = {'media': ('thumb.png', response.content, 'image/png')}
            res = requests.post(upload_url, files=files)
            data = res.json()
            if 'media_id' in data:
                return data['media_id']
            print(f"Upload error: {data}")
    except Exception as e:
        print(f"Error fetching/uploading cover: {e}")
    return None

def create_draft(access_token, title, content, thumb_media_id, author="Eric Assistant"):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    article = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": "每日品牌舆情洞察报告",
                "content": content,
                "content_source_url": "https://github.com/GlobalBusinessInsight/brand-insight-engine",
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 1
            }
        ]
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(article, ensure_ascii=False).encode('utf-8'), headers=headers)
    return response.json()

def run_publish():
    token = get_access_token()
    if not token: return
    
    # 1. Try to upload the specific cover image
    thumb_id = upload_thumb_from_url(token, WECHAT_COVER_URL)
    
    # 2. If upload fails, try to find an existing one
    if not thumb_id:
        thumb_id = get_latest_media_id(token)
    
    if not thumb_id:
        print("Error: Could not obtain a thumb_media_id.")
        return
    
    title = f"品牌洞察简报 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    content = format_content_from_data()
    
    draft_res = create_draft(token, title, content, thumb_id)
    if 'media_id' in draft_res:
        media_id = draft_res['media_id']
        pub_res = publish_draft(token, media_id)
        print(f"Publish task submitted: {pub_res}")
        return pub_res
    else:
        print(f"Draft creation failed: {draft_res}")
        return draft_res

if __name__ == "__main__":
    run_publish()

import requests
import time
import hashlib
from datetime import datetime
import os
from bs4 import BeautifulSoup, Comment
from email_sender import EmailSender
from config import EMAIL_CONFIG
from html_diff import compare_html

def clean_html(html_content):
    """清理HTML内容，移除可能导致误判的元素"""
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 移除所有script标签
    for script in soup.find_all('script'):
        script.decompose()
        
    # 移除所有style标签
    for style in soup.find_all('style'):
        style.decompose()
        
    # 移除所有注释
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
        
    # 获取body内容
    body = soup.find('body')
    if body:
        # 移除所有data-*属性
        for tag in body.find_all(True):
            for attr in list(tag.attrs):
                if attr.startswith('data-'):
                    del tag[attr]
                # 移除class和id中包含hash的属性
                elif attr in ['class', 'id']:
                    if any(isinstance(v, str) and len(v) > 16 and any(c.isdigit() for c in v) for v in tag[attr]):
                        del tag[attr]
        
        return str(body)
    return ""

def save_html(content, filename):
    """保存HTML内容到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"保存文件出错: {e}")

def get_page_content(url):
    try:
        # 添加 User-Agent 来模拟浏览器访问
        headers = {
            'authority': 'www.tesla.cn',
            'method': 'GET',
            'path': '/',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6',
            'cache-control': 'max-age=0',
            'cookie': 'gdp_user_id=gioenc-44b996b6%2C9gba%2C59ae%2C8528%2Cd33d8c898e8b; b0e25bc027704bfe_gdp_user_key=; AKA_A2=A; bm_ss=ab8e18ef4e; b0e25bc027704bfe_gdp_session_id=0c94b2f9-2e20-4d19-a1b7-8d18da51f516; ak_bmsc=2EC75A2B05CD1CDF951EAD6E1C304551~000000000000000000000000000000~YAAQbQ1x3/hNFiaUAQAAlk2FLBq19FAXwUD3RjoXoVcPJ9Pl1VuMre+MzIOGom4h7cb5QfZXWSnWoKgowoTTIWxjdv2i/27u+q1ddhw94EwvqUuWGqGeb6aY5m+01/wHqzl1Tcd4TxjBeEMFr8t+ZyfdpnrqtNsxq2oFIyx7+rfeTqlJOM12kNMu1dCfoXC7r2OzDOj8WfLoCibmxzkGFjJdNDO7P5h0V4HCqeVBNlr6+gl+qpaQV5TgnCURoRhbEfPsqqOEQyfg6OqB3fbkBHmPjp5Xs8LYrrbg7dpHivnCV6QQ10n6j7xPZ66qgNsLVrFCy3ubhj/ZBL7nq3c4w92tKtjImb4Fh9LyTfcbNWqTzj0oce+Kq0bEzhxYhiwyf/lhltMHTw==',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'  # 确保中文正确显示
        return response.text
    except Exception as e:
        print(f"获取页面出错: {e}")
        return None

def monitor_website(url):
    # 初始化邮件发送器
    email_sender = EmailSender(EMAIL_CONFIG)
    
    # 获取初始页面内容
    previous_content = get_page_content(url)
    if previous_content is None:
        return
    
    # 清理并保存初始内容
    cleaned_previous = clean_html(previous_content)
    previous_hash = hashlib.md5(cleaned_previous.encode()).hexdigest()

    while True:
        try:
            # 等待3秒
            time.sleep(300)
            
            # 获取新的页面内容
            current_content = get_page_content(url)
            if current_content is None:
                continue
            
            # 清理并保存当前内容
            cleaned_current = clean_html(current_content)
            
            current_hash = hashlib.md5(cleaned_current.encode()).hexdigest()
            
            if current_hash != previous_hash:
                current_time = datetime.now()
                update_message = f"[{current_time}] Tesla官网已更新!"
                print(update_message)
                # 比较差异
                changes = compare_html(cleaned_previous, cleaned_current)
                
                # 发送邮件通知
                email_sender.send_update_notification(url, changes)
                
                previous_hash = current_hash
                cleaned_previous = cleaned_current
                
        except Exception as e:
            print(f"监控过程出错: {e}")
            time.sleep(3)

if __name__ == "__main__":
    tesla_url = "https://www.tesla.cn/"
    print(f"开始监控 {tesla_url}")
    monitor_website(tesla_url)
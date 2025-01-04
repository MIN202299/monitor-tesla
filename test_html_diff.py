from html_diff import compare_html
import os
from email_sender import EmailSender
from config import EMAIL_CONFIG

def test_html_diff():
    email_sender = EmailSender(EMAIL_CONFIG)

    # 检查文件是否存在
    if not os.path.exists('previous.html') or not os.path.exists('current.html'):
        print("Error: previous.html 或 current.html 文件不存在")
        return

    try:
        # 读取两个HTML文件
        with open('previous.html', 'r', encoding='utf-8') as f:
            previous_html = f.read()
        
        with open('current.html', 'r', encoding='utf-8') as f:
            current_html = f.read()
        
        # 比较差异
        changes = compare_html(previous_html, current_html)
        email_sender.send_update_notification('https://www.tesla.cn', changes)
        # 打印结果
        if not changes:
            print("未检测到差异")
            return
        print(changes)
        print(f"检测到 {len(changes)} 处变化：\n")
        
        for i, change in enumerate(changes, 1):
            change_type = "新增" if change['type'] == 'added' else "删除"
            print(f"变化 {i}:")
            print(f"类型: {change_type}")
            print(f"位置: {change['path']}")
            print(f"标签: {change['tag']}")
            print(f"内容: {change['content']}")
            print("-" * 50)
            
    except Exception as e:
        print(f"测试过程出错: {e}")

if __name__ == "__main__":
    print("开始测试 HTML 差异比较功能...")
    test_html_diff() 
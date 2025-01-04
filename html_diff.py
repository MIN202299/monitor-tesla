from bs4 import BeautifulSoup
from difflib import unified_diff
import re

def get_tag_path(element):
    """获取元素的路径"""
    path = []
    for parent in element.parents:
        if parent.name is None:  # 到达根节点
            break
        siblings = parent.find_all(parent.name, recursive=False)
        index = siblings.index(parent) if parent in siblings else 0
        path.append(f"{parent.name}[{index}]")
    return ' > '.join(reversed(path))

def compare_html(old_html, new_html):
    """比较两个HTML内容的差异"""
    old_soup = BeautifulSoup(old_html, 'html.parser')
    new_soup = BeautifulSoup(new_html, 'html.parser')
    
    changes = []
    
    # 比较文本内容
    old_texts = old_soup.stripped_strings
    new_texts = new_soup.stripped_strings
    
    old_text_list = list(old_texts)
    new_text_list = list(new_texts)
    
    # 使用difflib比较文本差异
    diff = list(unified_diff(old_text_list, new_text_list, lineterm=''))
    
    for line in diff:
        if line.startswith('+') and not line.startswith('+++'):
            # 在新HTML中找到这个文本
            text = line[1:].strip()
            if text:
                elements = new_soup.find_all(string=re.compile(re.escape(text)))
                for elem in elements:
                    if elem.parent:
                        path = get_tag_path(elem.parent)
                        changes.append({
                            'type': 'added',
                            'path': path,
                            'tag': elem.parent.name,
                            'content': text
                        })
        
        elif line.startswith('-') and not line.startswith('---'):
            # 在旧HTML中找到这个文本
            text = line[1:].strip()
            if text:
                elements = old_soup.find_all(string=re.compile(re.escape(text)))
                for elem in elements:
                    if elem.parent:
                        path = get_tag_path(elem.parent)
                        changes.append({
                            'type': 'removed',
                            'path': path,
                            'tag': elem.parent.name,
                            'content': text
                        })
    
    return changes 
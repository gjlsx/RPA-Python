import os
import shutil
import re
from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString
from datetime import datetime

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BAK_DIR = os.path.join(ROOT_DIR, 'bak')
LOG_FILE = os.path.join(ROOT_DIR, 'process_html.log')

# 简单AI翻译函数（可扩展为API或更复杂模型）
def ai_translate(text):
    # 这里只做简单示例，实际可接入API或更复杂模型
    translations = {
        'Home': '首页',
        'Help': '帮助',
        'Submit': '提交',
        'Select Existing Strategy': '选择已有策略',
        'Or Input Custom Strategy': '或输入自定义策略',
        'Recommended Strategies': '推荐策略',
        'Stock/Crypto Code or Address:': '股票/加密货币代码或地址：',
        'Strategy Details': '策略详情',
        'Description': '描述',
        'Suitable Scenarios/Markets': '适用场景/市场',
        'Strategy Formula/Logic': '策略公式/逻辑',
        'Success Rate (in suitable conditions)': '成功率（在适用条件下）',
        'Historical Comments': '历史评论',
        'Back to Main Page': '返回主页面',
        'Loading...': '加载中...',
        '--Select a Strategy--': '--选择策略--',
        'Enter your quantitative strategy text here...': '在此输入您的量化策略文本...',
        'A powerful and efficient trading framework written in Python for cryptocurrency. Automate your trades and stay on top of the latest market trends.': '一个用Python编写的强大高效的加密货币交易框架。自动化您的交易，紧跟市场趋势。',
        'Quantitative Strategy Input': '量化策略输入',
    }
    return translations.get(text.strip(), text) or ''

def find_html_files(root_dir):
    html_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                full_path = os.path.join(dirpath, filename)
                if BAK_DIR not in full_path:
                    html_files.append(full_path)
    return html_files

def backup_file(src_path, root_dir, bak_dir):
    rel_path = os.path.relpath(src_path, root_dir)
    bak_path = os.path.join(bak_dir, rel_path)
    os.makedirs(os.path.dirname(bak_path), exist_ok=True)
    shutil.copy2(src_path, bak_path)
    return bak_path

def translate_visible_text(soup):
    # 只翻译可见文本节点
    for element in soup.find_all(text=True):
        parent = element.parent
        if parent.name not in ['script', 'style', 'meta', 'link', 'title', 'head']:
            if isinstance(element, NavigableString):
                text = str(element)
                if text.strip() and re.search(r'[A-Za-z]', text):
                    translated = ai_translate(text)
                    if translated != text:
                        element.replace_with(NavigableString(str(translated)))
    return soup

def replace_and_clean_html(html_path, translate=False):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('jesse.trade', 'mlove')
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    soup = BeautifulSoup(content, 'html.parser')
    for tag in soup.find_all(['script', 'link']):
        tag.decompose()
    for tag in soup.find_all():
        if isinstance(tag, Tag):
            if not tag.get_text(strip=True) and not tag.find():
                tag.decompose()
    if translate:
        soup = translate_visible_text(soup)
    cleaned = str(soup)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    return cleaned

def main():
    html_files = find_html_files(ROOT_DIR)
    logs = []
    for html_file in html_files:
        # 备份已完成，无需重复
        # 替换和精简+自动翻译
        replace_and_clean_html(html_file, translate=True)
        logs.append(f"Processed & Translated: {html_file}")
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"HTML Translate Log - {datetime.now()}\n")
        for log in logs:
            f.write(log + '\n')
    print(f"翻译完成，共处理{len(html_files)}个HTML文件。日志已追加到 {LOG_FILE}")

if __name__ == '__main__':
    main() 
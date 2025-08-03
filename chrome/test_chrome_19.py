#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Chrome_19连接
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def test_chrome_19():
    print('测试连接到Chrome_19 (端口10019)...')
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:10019')
        
        driver = webdriver.Chrome(options=chrome_options)
        print('成功连接到Chrome_19')
        print('当前页面标题:', driver.title)
        print('当前URL:', driver.current_url)
        
        # 导航到Google
        print('导航到Google...')
        driver.get('https://www.google.com')
        time.sleep(3)
        print('成功导航到Google')
        print('页面标题:', driver.title)
        
        # 尝试搜索
        search_box = driver.find_element('name', 'q')
        search_box.send_keys('Python automation test')
        search_box.submit()
        time.sleep(3)
        print('搜索完成，页面标题:', driver.title)
        
        print('测试完成 - Chrome_19工作正常!')
        return True
        
    except Exception as e:
        print('连接失败:', str(e))
        return False

if __name__ == "__main__":
    test_chrome_19()

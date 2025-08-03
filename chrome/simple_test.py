#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试Chrome自动化功能
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def test_chrome_automation():
    print("=== Chrome自动化功能测试 ===")
    
    # 测试Chrome_19
    print("\n1. 测试Chrome_19连接...")
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:10019')
        
        driver19 = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome_19连接成功")
        print(f"   当前URL: {driver19.current_url}")
        print(f"   页面标题: {driver19.title}")
        
        # 导航测试
        print("   导航到百度...")
        driver19.get('https://www.baidu.com')
        time.sleep(2)
        print(f"   ✅ 导航成功，标题: {driver19.title}")
        
        # 搜索测试
        try:
            search_box = driver19.find_element(By.ID, 'kw')
            search_box.send_keys('Python自动化测试')
            search_btn = driver19.find_element(By.ID, 'su')
            search_btn.click()
            time.sleep(3)
            print(f"   ✅ 搜索成功，标题: {driver19.title}")
        except Exception as e:
            print(f"   ⚠️ 搜索测试失败: {e}")
        
        driver19.quit()
        print("   ✅ Chrome_19测试完成")
        
    except Exception as e:
        print(f"   ❌ Chrome_19测试失败: {e}")
    
    # 测试Chrome_20
    print("\n2. 测试Chrome_20连接...")
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:10020')
        
        driver20 = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome_20连接成功")
        print(f"   当前URL: {driver20.current_url}")
        print(f"   页面标题: {driver20.title}")
        
        # 导航测试
        print("   导航到GitHub...")
        driver20.get('https://github.com')
        time.sleep(3)
        print(f"   ✅ 导航成功，标题: {driver20.title}")
        
        driver20.quit()
        print("   ✅ Chrome_20测试完成")
        
    except Exception as e:
        print(f"   ❌ Chrome_20测试失败: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_chrome_automation()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Chrome实例的多标签页功能
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def test_multiple_tabs():
    print("=== 测试Chrome多标签页功能 ===")
    
    # 测试Chrome_19
    print("\n1. 测试Chrome_19多标签页...")
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:10019')
        
        driver19 = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome_19连接成功")
        
        # 检查当前标签页数量
        current_handles = driver19.window_handles
        print(f"   当前标签页数量: {len(current_handles)}")
        
        # 打开新标签页
        print("   打开新标签页...")
        driver19.execute_script("window.open('https://www.baidu.com', '_blank');")
        time.sleep(2)
        
        driver19.execute_script("window.open('https://github.com', '_blank');")
        time.sleep(2)
        
        driver19.execute_script("window.open('https://stackoverflow.com', '_blank');")
        time.sleep(2)
        
        # 检查新的标签页数量
        new_handles = driver19.window_handles
        print(f"   新标签页数量: {len(new_handles)}")
        
        # 遍历所有标签页
        print("   遍历所有标签页:")
        for i, handle in enumerate(new_handles):
            driver19.switch_to.window(handle)
            time.sleep(1)
            print(f"     标签页 {i+1}: {driver19.title[:50]}...")
            print(f"     URL: {driver19.current_url}")
        
        print("   ✅ Chrome_19多标签页测试完成")
        
    except Exception as e:
        print(f"   ❌ Chrome_19多标签页测试失败: {e}")
    
    # 测试Chrome_20
    print("\n2. 测试Chrome_20多标签页...")
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:10020')
        
        driver20 = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome_20连接成功")
        
        # 检查当前标签页数量
        current_handles = driver20.window_handles
        print(f"   当前标签页数量: {len(current_handles)}")
        
        # 打开新标签页并同时操作
        print("   同时打开多个标签页并操作...")
        
        # 标签页1: Google搜索
        driver20.execute_script("window.open('https://www.google.com', '_blank');")
        time.sleep(2)
        handles = driver20.window_handles
        driver20.switch_to.window(handles[-1])
        try:
            search_box = driver20.find_element(By.NAME, 'q')
            search_box.send_keys('Chrome自动化测试')
            search_box.submit()
            time.sleep(2)
            print(f"     Google搜索标签页: {driver20.title[:50]}...")
        except:
            print("     Google搜索操作失败")
        
        # 标签页2: 百度搜索
        driver20.execute_script("window.open('https://www.baidu.com', '_blank');")
        time.sleep(2)
        handles = driver20.window_handles
        driver20.switch_to.window(handles[-1])
        try:
            search_box = driver20.find_element(By.ID, 'kw')
            search_box.send_keys('Selenium自动化')
            search_btn = driver20.find_element(By.ID, 'su')
            search_btn.click()
            time.sleep(2)
            print(f"     百度搜索标签页: {driver20.title[:50]}...")
        except:
            print("     百度搜索操作失败")
        
        # 标签页3: GitHub
        driver20.execute_script("window.open('https://github.com', '_blank');")
        time.sleep(2)
        handles = driver20.window_handles
        driver20.switch_to.window(handles[-1])
        print(f"     GitHub标签页: {driver20.title[:50]}...")
        
        # 检查最终标签页数量
        final_handles = driver20.window_handles
        print(f"   最终标签页数量: {len(final_handles)}")
        
        print("   ✅ Chrome_20多标签页测试完成")
        
    except Exception as e:
        print(f"   ❌ Chrome_20多标签页测试失败: {e}")
    
    print("\n=== 多标签页测试完成 ===")

def test_concurrent_operations():
    """测试多个Chrome实例同时进行多标签页操作"""
    print("\n=== 测试并发多标签页操作 ===")
    
    try:
        # 同时连接两个Chrome实例
        chrome_options_19 = Options()
        chrome_options_19.add_experimental_option('debuggerAddress', '127.0.0.1:10019')
        driver19 = webdriver.Chrome(options=chrome_options_19)
        
        chrome_options_20 = Options()
        chrome_options_20.add_experimental_option('debuggerAddress', '127.0.0.1:10020')
        driver20 = webdriver.Chrome(options=chrome_options_20)
        
        print("✅ 同时连接到Chrome_19和Chrome_20")
        
        # Chrome_19: 打开3个搜索标签页
        print("Chrome_19: 打开多个搜索标签页...")
        search_terms_19 = ["Python", "JavaScript", "Selenium"]
        for term in search_terms_19:
            driver19.execute_script("window.open('https://www.google.com', '_blank');")
            time.sleep(1)
            handles = driver19.window_handles
            driver19.switch_to.window(handles[-1])
            try:
                search_box = driver19.find_element(By.NAME, 'q')
                search_box.send_keys(f"{term} 教程")
                search_box.submit()
                time.sleep(2)
                print(f"  ✅ Chrome_19搜索: {term} - {driver19.title[:30]}...")
            except:
                print(f"  ❌ Chrome_19搜索失败: {term}")
        
        # Chrome_20: 打开3个不同网站
        print("Chrome_20: 打开多个不同网站...")
        websites_20 = [
            "https://www.baidu.com",
            "https://github.com", 
            "https://stackoverflow.com"
        ]
        for site in websites_20:
            driver20.execute_script(f"window.open('{site}', '_blank');")
            time.sleep(2)
            handles = driver20.window_handles
            driver20.switch_to.window(handles[-1])
            print(f"  ✅ Chrome_20访问: {driver20.title[:30]}...")
        
        # 统计结果
        handles_19 = len(driver19.window_handles)
        handles_20 = len(driver20.window_handles)
        
        print(f"\n📊 并发操作结果:")
        print(f"   Chrome_19总标签页: {handles_19}")
        print(f"   Chrome_20总标签页: {handles_20}")
        print(f"   总计标签页: {handles_19 + handles_20}")
        
        print("✅ 并发多标签页操作测试成功")
        
    except Exception as e:
        print(f"❌ 并发操作测试失败: {e}")

if __name__ == "__main__":
    test_multiple_tabs()
    test_concurrent_operations()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试Chrome标签页功能
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

def test_tabs_direct():
    print("=== 直接测试Chrome标签页功能 ===")
    
    try:
        # 连接Chrome_19
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:10019')
        driver = webdriver.Chrome(options=chrome_options)
        
        print("✅ 连接到Chrome_19成功")
        print(f"初始标签页数量: {len(driver.window_handles)}")
        
        # 方法1: 使用Ctrl+T打开新标签页
        print("\n方法1: 使用Ctrl+T打开新标签页...")
        driver.find_element('tag name', 'body').send_keys(Keys.CONTROL + 't')
        time.sleep(2)
        print(f"标签页数量: {len(driver.window_handles)}")
        
        # 切换到新标签页
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.get('https://www.baidu.com')
            time.sleep(3)
            print(f"新标签页标题: {driver.title}")
        
        # 方法2: 再次使用Ctrl+T
        print("\n方法2: 再次使用Ctrl+T...")
        driver.find_element('tag name', 'body').send_keys(Keys.CONTROL + 't')
        time.sleep(2)
        print(f"标签页数量: {len(driver.window_handles)}")
        
        # 切换到最新标签页
        if len(driver.window_handles) > 2:
            driver.switch_to.window(driver.window_handles[-1])
            driver.get('https://github.com')
            time.sleep(3)
            print(f"第二个新标签页标题: {driver.title}")
        
        # 方法3: 使用JavaScript强制打开
        print("\n方法3: 使用JavaScript强制打开...")
        original_handles = len(driver.window_handles)
        driver.execute_script("window.open('about:blank', '_blank');")
        time.sleep(2)
        new_handles = len(driver.window_handles)
        print(f"JavaScript方法 - 原始: {original_handles}, 现在: {new_handles}")
        
        if new_handles > original_handles:
            driver.switch_to.window(driver.window_handles[-1])
            driver.get('https://stackoverflow.com')
            time.sleep(3)
            print(f"JavaScript新标签页标题: {driver.title}")
        
        # 遍历所有标签页
        print(f"\n📊 最终结果:")
        print(f"总标签页数量: {len(driver.window_handles)}")
        print("所有标签页:")
        for i, handle in enumerate(driver.window_handles):
            driver.switch_to.window(handle)
            print(f"  标签页 {i+1}: {driver.title[:50]}...")
            print(f"    URL: {driver.current_url[:60]}...")
        
        print("✅ 标签页测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_batch_chrome_launcher():
    """测试批量启动器是否真的打开了多个标签页"""
    print("\n=== 测试批量启动器的多标签页功能 ===")
    
    try:
        # 连接到Chrome_19
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:10019')
        driver = webdriver.Chrome(options=chrome_options)
        
        print("✅ 连接成功")
        handles = driver.window_handles
        print(f"当前标签页数量: {len(handles)}")
        
        # 检查每个标签页的内容
        if len(handles) > 1:
            print("检查各个标签页:")
            for i, handle in enumerate(handles):
                driver.switch_to.window(handle)
                time.sleep(1)
                print(f"  标签页 {i+1}:")
                print(f"    标题: {driver.title}")
                print(f"    URL: {driver.current_url}")
        else:
            print("⚠️ 只有一个标签页，批量启动器可能没有打开多个网站")
            
            # 手动打开配置的网站
            print("手动打开配置的网站...")
            websites = [
                "https://www.google.com",
                "https://github.com", 
                "https://stackoverflow.com"
            ]
            
            for site in websites:
                driver.execute_script(f"window.open('{site}', '_blank');")
                time.sleep(2)
                
            print(f"手动打开后标签页数量: {len(driver.window_handles)}")
            
            # 检查新打开的标签页
            for i, handle in enumerate(driver.window_handles):
                driver.switch_to.window(handle)
                time.sleep(1)
                print(f"  标签页 {i+1}: {driver.title[:40]}...")
        
    except Exception as e:
        print(f"❌ 批量启动器测试失败: {e}")

if __name__ == "__main__":
    test_tabs_direct()
    test_batch_chrome_launcher()

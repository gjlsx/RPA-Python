#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Chrome_20的标签页情况
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def check_chrome_20_tabs():
    print("=== 检查Chrome_20标签页情况 ===")
    
    try:
        # 连接Chrome_20
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:10020')
        driver = webdriver.Chrome(options=chrome_options)
        
        print("✅ 连接到Chrome_20成功")
        
        # 检查标签页数量
        handles = driver.window_handles
        print(f"📊 当前标签页数量: {len(handles)}")
        
        # 遍历所有标签页
        print("\n📋 所有标签页详情:")
        for i, handle in enumerate(handles):
            driver.switch_to.window(handle)
            time.sleep(1)
            print(f"  标签页 {i+1}:")
            print(f"    标题: {driver.title}")
            print(f"    URL: {driver.current_url}")
            print()
        
        # 如果标签页少于3个，说明批量启动器有问题
        if len(handles) < 3:
            print("⚠️ 标签页数量少于预期的3个")
            print("手动打开配置的网站进行测试...")
            
            websites = [
                "https://www.google.com",
                "https://github.com", 
                "https://stackoverflow.com"
            ]
            
            for site in websites:
                print(f"打开: {site}")
                driver.execute_script(f"window.open('{site}', '_blank');")
                time.sleep(3)
                
                # 切换到新标签页
                new_handles = driver.window_handles
                if len(new_handles) > len(handles):
                    driver.switch_to.window(new_handles[-1])
                    print(f"  ✅ 成功打开: {driver.title}")
                    handles = new_handles
                else:
                    print(f"  ❌ 打开失败")
            
            print(f"\n📊 手动打开后标签页数量: {len(driver.window_handles)}")
        
        print("✅ Chrome_20标签页检查完成")
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_chrome_20_tabs()

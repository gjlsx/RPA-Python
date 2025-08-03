#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终多标签页功能测试 - 测试所有Chrome实例
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def test_all_chrome_instances():
    print("=== 最终多标签页功能测试 ===")
    
    chrome_instances = [
        (19, 10019),
        (20, 10020), 
        (21, 10021)
    ]
    
    total_tabs = 0
    
    for chrome_num, port in chrome_instances:
        print(f"\n🔍 测试Chrome_{chrome_num} (端口{port})...")
        
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{port}')
            driver = webdriver.Chrome(options=chrome_options)
            
            print(f"✅ Chrome_{chrome_num}连接成功")
            
            # 检查标签页数量
            handles = driver.window_handles
            tab_count = len(handles)
            total_tabs += tab_count
            
            print(f"📊 标签页数量: {tab_count}")
            
            # 显示前3个标签页的信息
            print("📋 标签页详情:")
            for i, handle in enumerate(handles[:3]):  # 只显示前3个
                driver.switch_to.window(handle)
                time.sleep(0.5)
                title = driver.title[:40] + "..." if len(driver.title) > 40 else driver.title
                url = driver.current_url[:50] + "..." if len(driver.current_url) > 50 else driver.current_url
                print(f"  标签页 {i+1}: {title}")
                print(f"    URL: {url}")
            
            if tab_count > 3:
                print(f"  ... 还有 {tab_count - 3} 个标签页")
            
            # 测试在当前实例中打开新标签页
            print(f"🚀 在Chrome_{chrome_num}中测试新标签页...")
            original_count = len(driver.window_handles)
            
            # 使用JavaScript打开新标签页
            driver.execute_script("window.open('https://www.baidu.com', '_blank');")
            time.sleep(2)
            
            new_count = len(driver.window_handles)
            if new_count > original_count:
                print(f"  ✅ 成功打开新标签页 ({original_count} → {new_count})")
                driver.switch_to.window(driver.window_handles[-1])
                print(f"  新标签页标题: {driver.title}")
                total_tabs += 1
            else:
                print(f"  ❌ 新标签页打开失败")
            
            print(f"✅ Chrome_{chrome_num}测试完成")
            
        except Exception as e:
            print(f"❌ Chrome_{chrome_num}测试失败: {e}")
    
    print(f"\n📊 === 最终统计 ===")
    print(f"总Chrome实例数: {len(chrome_instances)}")
    print(f"总标签页数: {total_tabs}")
    print(f"平均每实例标签页数: {total_tabs / len(chrome_instances):.1f}")
    
    # 测试并发操作
    print(f"\n🔄 === 并发操作测试 ===")
    test_concurrent_operations()

def test_concurrent_operations():
    """测试多个Chrome实例的并发操作"""
    print("测试多个Chrome实例同时操作...")
    
    drivers = {}
    
    try:
        # 同时连接所有实例
        for chrome_num, port in [(19, 10019), (20, 10020), (21, 10021)]:
            try:
                chrome_options = Options()
                chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{port}')
                drivers[chrome_num] = webdriver.Chrome(options=chrome_options)
                print(f"✅ Chrome_{chrome_num}连接成功")
            except Exception as e:
                print(f"❌ Chrome_{chrome_num}连接失败: {e}")
        
        if len(drivers) >= 2:
            print(f"🚀 开始并发操作 ({len(drivers)}个实例)...")
            
            # 同时在不同实例中打开不同网站
            operations = [
                (19, "https://www.google.com/search?q=Python"),
                (20, "https://github.com/search?q=automation"),
                (21, "https://stackoverflow.com/search?q=selenium")
            ]
            
            for chrome_num, url in operations:
                if chrome_num in drivers:
                    try:
                        driver = drivers[chrome_num]
                        driver.execute_script(f"window.open('{url}', '_blank');")
                        handles = driver.window_handles
                        if len(handles) > 0:
                            driver.switch_to.window(handles[-1])
                            time.sleep(2)
                            print(f"  ✅ Chrome_{chrome_num}: {driver.title[:40]}...")
                    except Exception as e:
                        print(f"  ❌ Chrome_{chrome_num}操作失败: {e}")
            
            print("✅ 并发操作测试完成")
        else:
            print("⚠️ 可用实例不足，跳过并发测试")
            
    except Exception as e:
        print(f"❌ 并发测试失败: {e}")

if __name__ == "__main__":
    test_all_chrome_instances()

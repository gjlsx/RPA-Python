#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能Chrome管理工作流程演示
展示完整的Chrome实例管理功能
"""

import time
from smart_chrome_manager import SmartChromeManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def demo_workflow():
    """演示完整的Chrome管理工作流程"""
    print("🎭 Chrome智能管理工作流程演示")
    print("=" * 60)
    
    manager = SmartChromeManager()
    chrome_numbers = [19, 20]
    
    # 步骤1: 检查初始状态
    print("\n📍 步骤1: 检查初始状态")
    manager.show_status(chrome_numbers)
    
    input("\n按Enter继续到步骤2...")
    
    # 步骤2: 智能启动Chrome实例
    print("\n📍 步骤2: 智能启动Chrome实例")
    print("启动Chrome_19和Chrome_20，每个实例将打开多个标签页")
    manager.smart_restart_chrome(chrome_numbers, force_close=True)
    
    input("\n按Enter继续到步骤3...")
    
    # 步骤3: 验证启动状态和标签页
    print("\n📍 步骤3: 验证启动状态")
    manager.show_status(chrome_numbers)
    
    # 详细检查标签页
    print("\n🔍 详细检查标签页内容:")
    for chrome_num in chrome_numbers:
        check_chrome_tabs(chrome_num)
    
    input("\n按Enter继续到步骤4...")
    
    # 步骤4: 演示自动化操作
    print("\n📍 步骤4: 演示自动化操作")
    print("在Chrome_19中执行搜索操作...")
    
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:10019')
        driver = webdriver.Chrome(options=chrome_options)
        
        # 打开新标签页并搜索
        driver.execute_script("window.open('https://www.baidu.com', '_blank');")
        time.sleep(2)
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])
        
        # 执行搜索
        search_box = driver.find_element('id', 'kw')
        search_box.send_keys('Chrome自动化管理演示')
        search_btn = driver.find_element('id', 'su')
        search_btn.click()
        time.sleep(3)
        
        print(f"✅ 搜索完成: {driver.title}")
        driver.quit()
        
    except Exception as e:
        print(f"❌ 自动化操作失败: {e}")
    
    input("\n按Enter继续到步骤5...")
    
    # 步骤5: 优雅关闭演示
    print("\n📍 步骤5: 优雅关闭演示")
    print("使用优雅关闭功能，避免'要恢复页面吗？'对话框")
    
    manager.graceful_close_chrome(chrome_numbers)
    
    input("\n按Enter继续到步骤6...")
    
    # 步骤6: 验证关闭状态
    print("\n📍 步骤6: 验证关闭状态")
    manager.show_status(chrome_numbers)
    
    print("\n🎉 演示完成！")
    print("\n📋 功能总结:")
    print("✅ 智能检测现存Chrome实例")
    print("✅ 自动启动Chrome实例并打开多个标签页")
    print("✅ 实时状态监控和标签页统计")
    print("✅ Selenium自动化操作支持")
    print("✅ 优雅关闭，避免恢复页面对话框")
    print("✅ 完整的错误处理和恢复机制")

def check_chrome_tabs(chrome_num):
    """检查Chrome实例的标签页详情"""
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{10000 + chrome_num}')
        
        driver = webdriver.Chrome(options=chrome_options)
        handles = driver.window_handles
        
        print(f"  Chrome_{chrome_num}: {len(handles)}个标签页")
        
        for i, handle in enumerate(handles[:3]):  # 只显示前3个
            driver.switch_to.window(handle)
            title = driver.title[:40] + "..." if len(driver.title) > 40 else driver.title
            url = driver.current_url[:50] + "..." if len(driver.current_url) > 50 else driver.current_url
            print(f"    标签页{i+1}: {title}")
            print(f"      URL: {url}")
        
        if len(handles) > 3:
            print(f"    ... 还有{len(handles) - 3}个标签页")
        
        driver.quit()
        
    except Exception as e:
        print(f"  ❌ Chrome_{chrome_num}检查失败: {e}")

def quick_test():
    """快速测试功能"""
    print("🚀 快速功能测试")
    print("=" * 40)
    
    manager = SmartChromeManager()
    chrome_numbers = [19, 20]
    
    # 检查状态
    print("1. 检查当前状态...")
    running = manager.check_chrome_instances(chrome_numbers)
    
    if running:
        print(f"发现运行中的实例: {list(running.keys())}")
        print("2. 优雅关闭现存实例...")
        manager.graceful_close_chrome(chrome_numbers)
        time.sleep(2)
    
    print("3. 启动Chrome实例...")
    manager.smart_restart_chrome(chrome_numbers, force_close=True)
    
    print("4. 等待5秒后关闭...")
    time.sleep(5)
    manager.graceful_close_chrome(chrome_numbers)
    
    print("✅ 快速测试完成")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Chrome智能管理演示')
    parser.add_argument('--demo', action='store_true', help='运行完整演示')
    parser.add_argument('--quick', action='store_true', help='快速测试')
    
    args = parser.parse_args()
    
    if args.demo:
        demo_workflow()
    elif args.quick:
        quick_test()
    else:
        print("请选择运行模式:")
        print("  --demo  : 完整交互式演示")
        print("  --quick : 快速自动测试")

if __name__ == "__main__":
    main()

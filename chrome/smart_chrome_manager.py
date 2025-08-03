#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能Chrome管理器
- 检查现存Chrome实例
- 智能关闭和重启
- 多标签页管理
"""

import psutil
import time
import subprocess
from pathlib import Path
from close_specific_chrome import SpecificChromeCloser
from graceful_chrome_closer import GracefulChromeCloser
from batch_chrome_launcher import ChromeBatchLauncher
from auto_dialog_handler import ChromeDialogHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SmartChromeManager:
    def __init__(self):
        self.closer = SpecificChromeCloser()
        self.graceful_closer = GracefulChromeCloser()
        self.launcher = ChromeBatchLauncher()
        self.dialog_handler = ChromeDialogHandler()
        
    def check_chrome_instances(self, chrome_numbers):
        """检查指定Chrome实例的运行状态"""
        print(f"🔍 检查Chrome实例状态: {chrome_numbers}")
        
        running_instances = {}
        
        for chrome_num in chrome_numbers:
            target_port = 10000 + chrome_num
            user_data_pattern = f"chromes\\{chrome_num}"
            
            processes = []
            window_count = 0
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if not proc.info['name'] or 'chrome.exe' not in proc.info['name'].lower():
                        continue
                    
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    
                    if f"--remote-debugging-port={target_port}" in cmdline or user_data_pattern in cmdline:
                        processes.append({
                            'pid': proc.info['pid'],
                            'cmdline': cmdline[:80] + '...' if len(cmdline) > 80 else cmdline
                        })
                        
                        # 检查是否是主进程（通常包含调试端口）
                        if f"--remote-debugging-port={target_port}" in cmdline:
                            window_count += 1
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if processes:
                running_instances[chrome_num] = {
                    'processes': processes,
                    'window_count': window_count,
                    'port': target_port
                }
                
                print(f"  ✅ Chrome_{chrome_num}: {len(processes)}个进程, {window_count}个窗口")
                for proc in processes:
                    print(f"    PID:{proc['pid']} - {proc['cmdline']}")
            else:
                print(f"  ❌ Chrome_{chrome_num}: 未运行")
        
        return running_instances
    
    def get_tab_count(self, chrome_num):
        """获取Chrome实例的标签页数量"""
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{10000 + chrome_num}')
            
            driver = webdriver.Chrome(options=chrome_options)
            tab_count = len(driver.window_handles)
            driver.quit()
            
            return tab_count
        except Exception as e:
            print(f"  ⚠️ 无法获取Chrome_{chrome_num}标签页数量: {e}")
            return 0
    
    def smart_restart_chrome(self, chrome_numbers, force_close=False):
        """智能重启Chrome实例"""
        print(f"🔄 智能重启Chrome实例: {chrome_numbers}")
        
        # 步骤1: 检查当前状态
        running_instances = self.check_chrome_instances(chrome_numbers)
        
        # 步骤2: 处理现存实例
        if running_instances:
            print(f"\n📊 发现运行中的实例: {list(running_instances.keys())}")
            
            # 获取标签页信息
            for chrome_num in running_instances:
                tab_count = self.get_tab_count(chrome_num)
                running_instances[chrome_num]['tab_count'] = tab_count
                print(f"  Chrome_{chrome_num}: {tab_count}个标签页")
            
            if not force_close:
                print("\n⚠️ 发现现存Chrome实例，请选择操作:")
                print("1. 强制关闭并重启")
                print("2. 保留现存实例，只启动未运行的")
                print("3. 取消操作")
                
                choice = input("请选择 (1/2/3): ").strip()
                
                if choice == '1':
                    force_close = True
                elif choice == '2':
                    # 只启动未运行的实例
                    chrome_numbers = [num for num in chrome_numbers if num not in running_instances]
                    if not chrome_numbers:
                        print("✅ 所有实例都已运行，无需启动")
                        return True
                elif choice == '3':
                    print("❌ 操作已取消")
                    return False
                else:
                    print("❌ 无效选择，操作已取消")
                    return False
            
            # 关闭现存实例
            if force_close and running_instances:
                print(f"\n🔴 优雅关闭现存实例: {list(running_instances.keys())}")
                self.graceful_closer.close_with_session_cleanup(list(running_instances.keys()))
                time.sleep(3)  # 等待进程完全关闭
        
        # 步骤3: 启动Chrome实例
        if chrome_numbers:
            print(f"\n🚀 启动Chrome实例: {chrome_numbers}")
            
            for chrome_num in chrome_numbers:
                print(f"\n启动Chrome_{chrome_num}...")
                
                # 检查快捷方式是否存在
                shortcut_path = Path(f"Chrome_{chrome_num}.lnk")
                if not shortcut_path.exists():
                    print(f"  ❌ 快捷方式不存在: {shortcut_path}")
                    continue
                
                # 直接使用批量启动器启动Chrome实例并打开网站
                try:
                    print(f"  🚀 启动Chrome_{chrome_num}并打开配置的网站...")
                    self.launcher.launch_chrome_instance(chrome_num, shortcut_path)

                    # 等待启动完成
                    time.sleep(3)

                    # 验证启动
                    if self.verify_chrome_started(chrome_num):
                        print(f"  ✅ Chrome_{chrome_num}启动成功")

                        # 检查标签页数量
                        time.sleep(2)
                        tab_count = self.get_tab_count(chrome_num)
                        print(f"  📊 Chrome_{chrome_num}当前有{tab_count}个标签页")

                    else:
                        print(f"  ❌ Chrome_{chrome_num}启动失败")

                except Exception as e:
                    print(f"  ❌ Chrome_{chrome_num}启动出错: {e}")
        
        print(f"\n✅ 智能重启完成")
        return True
    
    def verify_chrome_started(self, chrome_num, timeout=10):
        """验证Chrome实例是否成功启动"""
        target_port = 10000 + chrome_num
        
        for _ in range(timeout):
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'chrome.exe' in proc.info['name'].lower():
                        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                        if f"--remote-debugging-port={target_port}" in cmdline:
                            return True
                except:
                    continue
            time.sleep(1)
        
        return False

    def graceful_close_chrome(self, chrome_numbers):
        """优雅关闭Chrome实例，避免恢复页面对话框"""
        print(f"🕊️ 优雅关闭Chrome实例: {chrome_numbers}")

        # 检查当前状态
        running_instances = self.check_chrome_instances(chrome_numbers)

        if not running_instances:
            print("ℹ️ 没有发现运行中的Chrome实例")
            return True

        # 使用优雅关闭
        success = self.graceful_closer.close_with_session_cleanup(chrome_numbers)

        if success:
            print("✅ 所有Chrome实例已优雅关闭")
        else:
            print("⚠️ 部分实例可能需要手动处理")

        return success

    def smart_restart_with_dialog_handling(self, chrome_numbers, force_close=False, dialog_action="close"):
        """智能重启Chrome实例并自动处理恢复对话框"""
        print(f"🤖 智能重启Chrome实例（自动处理对话框）: {chrome_numbers}")
        print(f"   对话框处理: {'恢复页面' if dialog_action == 'restore' else '关闭对话框'}")

        # 启动对话框监控
        self.dialog_handler.start_monitoring(chrome_numbers, dialog_action)

        try:
            # 执行正常的重启流程
            result = self.smart_restart_chrome(chrome_numbers, force_close)

            # 等待一下，让对话框处理器有时间工作
            time.sleep(5)

            # 手动触发一次对话框处理
            self.dialog_handler.auto_handle_dialogs(chrome_numbers, dialog_action, timeout=10)

            return result

        finally:
            # 停止监控
            self.dialog_handler.stop_monitoring()

    def show_status(self, chrome_numbers):
        """显示Chrome实例状态"""
        print("=" * 60)
        print("📊 Chrome实例状态报告")
        print("=" * 60)
        
        running_instances = self.check_chrome_instances(chrome_numbers)
        
        for chrome_num in chrome_numbers:
            print(f"\n🔍 Chrome_{chrome_num}:")
            if chrome_num in running_instances:
                instance = running_instances[chrome_num]
                tab_count = self.get_tab_count(chrome_num)
                
                print(f"  状态: ✅ 运行中")
                print(f"  端口: {instance['port']}")
                print(f"  进程数: {len(instance['processes'])}")
                print(f"  标签页数: {tab_count}")
                print(f"  窗口数: {instance['window_count']}")
            else:
                print(f"  状态: ❌ 未运行")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='智能Chrome管理器')
    parser.add_argument('numbers', nargs='+', type=int, help='Chrome编号')
    parser.add_argument('--status', action='store_true', help='显示状态')
    parser.add_argument('--restart', action='store_true', help='重启实例')
    parser.add_argument('--close', action='store_true', help='优雅关闭实例')
    parser.add_argument('--auto-dialog', action='store_true', help='自动处理恢复对话框')
    parser.add_argument('--dialog-action', choices=['restore', 'close'], default='close', help='对话框处理动作')
    parser.add_argument('--force', action='store_true', help='强制关闭现存实例')
    
    args = parser.parse_args()
    
    manager = SmartChromeManager()
    
    if args.status:
        manager.show_status(args.numbers)
    elif args.restart:
        if args.auto_dialog:
            manager.smart_restart_with_dialog_handling(args.numbers, args.force, args.dialog_action)
        else:
            manager.smart_restart_chrome(args.numbers, args.force)
    elif args.close:
        manager.graceful_close_chrome(args.numbers)
    else:
        manager.show_status(args.numbers)

if __name__ == "__main__":
    main()

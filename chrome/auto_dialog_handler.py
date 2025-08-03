#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动处理Chrome对话框
- 自动点击"要恢复页面吗？"对话框
- 支持选择"恢复"或"关闭"
- 使用Windows API和pyautogui进行UI自动化
"""

import time
import threading
import pyautogui
import win32gui
import win32con
import win32api
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChromeDialogHandler:
    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
        
        # 设置pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
    
    def find_chrome_restore_dialog(self):
        """查找Chrome恢复页面对话框"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                
                # 检查是否是Chrome恢复对话框
                if ("要恢复页面吗" in window_text or 
                    "Chrome 未正确关闭" in window_text or
                    "Restore pages" in window_text or
                    class_name == "Chrome_WidgetWin_1"):
                    
                    # 获取窗口位置和大小
                    rect = win32gui.GetWindowRect(hwnd)
                    windows.append({
                        'hwnd': hwnd,
                        'title': window_text,
                        'class': class_name,
                        'rect': rect
                    })
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        return windows
    
    def click_dialog_button(self, action="close"):
        """点击对话框按钮"""
        print(f"🔍 搜索Chrome恢复对话框...")
        
        dialogs = self.find_chrome_restore_dialog()
        
        if not dialogs:
            print("  ❌ 未找到恢复对话框")
            return False
        
        for dialog in dialogs:
            print(f"  ✅ 找到对话框: {dialog['title']}")
            hwnd = dialog['hwnd']
            rect = dialog['rect']
            
            # 激活窗口
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.5)
            
            # 计算按钮位置（基于对话框位置）
            dialog_width = rect[2] - rect[0]
            dialog_height = rect[3] - rect[1]
            center_x = rect[0] + dialog_width // 2
            center_y = rect[1] + dialog_height // 2
            
            if action == "restore":
                # "恢复"按钮通常在右侧
                button_x = center_x + 50
                button_y = center_y + 30
                print(f"  🔄 点击'恢复'按钮 ({button_x}, {button_y})")
            else:
                # "关闭"或"X"按钮
                # 先尝试右上角的X按钮
                close_x = rect[2] - 20
                close_y = rect[1] + 20
                button_x = close_x
                button_y = close_y
                print(f"  ❌ 点击'关闭'按钮 ({button_x}, {button_y})")
            
            try:
                # 移动鼠标并点击
                pyautogui.moveTo(button_x, button_y, duration=0.3)
                pyautogui.click()
                time.sleep(0.5)
                
                # 验证对话框是否关闭
                if not win32gui.IsWindowVisible(hwnd):
                    print(f"  ✅ 对话框已关闭")
                    return True
                else:
                    # 如果X按钮没用，尝试其他位置
                    if action == "close":
                        # 尝试按ESC键
                        pyautogui.press('escape')
                        time.sleep(0.5)
                        
                        if not win32gui.IsWindowVisible(hwnd):
                            print(f"  ✅ 通过ESC键关闭对话框")
                            return True
                
            except Exception as e:
                print(f"  ❌ 点击失败: {e}")
                continue
        
        return False
    
    def handle_restore_dialog_selenium(self, chrome_num, action="close"):
        """使用Selenium处理恢复对话框"""
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{10000 + chrome_num}')
            
            driver = webdriver.Chrome(options=chrome_options)
            
            # 查找恢复对话框元素
            try:
                # 等待对话框出现
                dialog = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[role='dialog'], .infobar"))
                )
                
                if action == "restore":
                    # 查找恢复按钮
                    restore_btn = driver.find_element(By.XPATH, "//button[contains(text(), '恢复') or contains(text(), 'Restore')]")
                    restore_btn.click()
                    print(f"  ✅ Chrome_{chrome_num}: 已点击恢复按钮")
                else:
                    # 查找关闭按钮
                    close_btn = driver.find_element(By.XPATH, "//button[contains(text(), '关闭') or contains(text(), 'Close') or @aria-label='Close']")
                    close_btn.click()
                    print(f"  ✅ Chrome_{chrome_num}: 已点击关闭按钮")
                
                driver.quit()
                return True
                
            except Exception as e:
                print(f"  ⚠️ Chrome_{chrome_num}: 未找到对话框元素: {e}")
                driver.quit()
                return False
                
        except Exception as e:
            print(f"  ❌ Chrome_{chrome_num}: Selenium连接失败: {e}")
            return False
    
    def auto_handle_dialogs(self, chrome_numbers, action="close", timeout=30):
        """自动处理多个Chrome实例的对话框"""
        print(f"🤖 自动处理Chrome恢复对话框: {chrome_numbers}")
        print(f"   动作: {'恢复页面' if action == 'restore' else '关闭对话框'}")
        
        start_time = time.time()
        handled_count = 0
        
        while time.time() - start_time < timeout:
            # 方法1: 使用Windows API查找对话框
            if self.click_dialog_button(action):
                handled_count += 1
                print(f"  📊 已处理 {handled_count} 个对话框")
            
            # 方法2: 使用Selenium处理每个Chrome实例
            for chrome_num in chrome_numbers:
                if self.handle_restore_dialog_selenium(chrome_num, action):
                    handled_count += 1
            
            # 检查是否还有对话框
            dialogs = self.find_chrome_restore_dialog()
            if not dialogs:
                print(f"  ✅ 所有对话框已处理完成")
                break
            
            time.sleep(1)
        
        print(f"📊 处理结果: 共处理了 {handled_count} 个对话框")
        return handled_count > 0
    
    def start_monitoring(self, chrome_numbers, action="close"):
        """启动对话框监控"""
        if self.monitoring:
            print("⚠️ 监控已在运行中")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_dialogs,
            args=(chrome_numbers, action),
            daemon=True
        )
        self.monitor_thread.start()
        print(f"🔍 开始监控Chrome恢复对话框...")
    
    def stop_monitoring(self):
        """停止对话框监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("⏹️ 对话框监控已停止")
    
    def _monitor_dialogs(self, chrome_numbers, action):
        """监控线程"""
        while self.monitoring:
            try:
                dialogs = self.find_chrome_restore_dialog()
                if dialogs:
                    print(f"🚨 检测到 {len(dialogs)} 个恢复对话框")
                    self.auto_handle_dialogs(chrome_numbers, action, timeout=10)
                
                time.sleep(2)  # 每2秒检查一次
                
            except Exception as e:
                print(f"⚠️ 监控过程中出错: {e}")
                time.sleep(5)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Chrome对话框自动处理器')
    parser.add_argument('numbers', nargs='+', type=int, help='Chrome编号')
    parser.add_argument('--action', choices=['restore', 'close'], default='close', help='处理动作')
    parser.add_argument('--monitor', action='store_true', help='启动监控模式')
    parser.add_argument('--timeout', type=int, default=30, help='超时时间（秒）')
    
    args = parser.parse_args()
    
    handler = ChromeDialogHandler()
    
    if args.monitor:
        print("🔍 启动监控模式，按Ctrl+C停止...")
        handler.start_monitoring(args.numbers, args.action)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            handler.stop_monitoring()
    else:
        handler.auto_handle_dialogs(args.numbers, args.action, args.timeout)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精准关闭特定Chrome实例
支持按编号、端口、进程ID等方式关闭
"""

import psutil
import time
import argparse
from pathlib import Path

class SpecificChromeCloser:
    def __init__(self):
        self.closed_processes = []
    
    def close_by_numbers(self, chrome_numbers):
        """根据Chrome编号关闭实例"""
        print(f"🎯 关闭Chrome实例: {chrome_numbers}")
        
        target_ports = [10000 + num for num in chrome_numbers]
        target_data_dirs = [f"chromes\\{num}" for num in chrome_numbers]
        
        closed_count = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if not proc.info['name'] or 'chrome.exe' not in proc.info['name'].lower():
                    continue
                
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                # 检查是否匹配目标实例
                is_target = False
                matched_info = ""
                
                # 检查调试端口
                for i, port in enumerate(target_ports):
                    if f"--remote-debugging-port={port}" in cmdline:
                        is_target = True
                        matched_info = f"Chrome_{chrome_numbers[i]} (端口:{port})"
                        break
                
                # 检查用户数据目录
                if not is_target:
                    for i, data_dir in enumerate(target_data_dirs):
                        if data_dir in cmdline:
                            is_target = True
                            matched_info = f"Chrome_{chrome_numbers[i]} (数据目录)"
                            break
                
                if is_target:
                    print(f"  🔪 优雅关闭 {matched_info} PID:{proc.info['pid']}")

                    # 先尝试优雅关闭
                    try:
                        # 发送关闭信号
                        proc.terminate()
                        self.closed_processes.append((proc.info['pid'], matched_info))
                        closed_count += 1

                        # 等待进程优雅关闭
                        proc.wait(timeout=3)
                        print(f"  ✅ {matched_info} 已优雅关闭")

                    except psutil.TimeoutExpired:
                        # 如果3秒内没有关闭，强制杀死
                        try:
                            if proc.is_running():
                                proc.kill()
                                print(f"  💀 强制杀死 {matched_info}")
                        except:
                            pass
                    except:
                        pass
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        print(f"📊 成功关闭 {closed_count} 个Chrome实例")
        return closed_count
    
    def verify_closure(self, chrome_numbers):
        """验证Chrome实例是否已关闭"""
        print("🔍 验证关闭结果...")
        
        target_ports = [10000 + num for num in chrome_numbers]
        still_running = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if not proc.info['name'] or 'chrome.exe' not in proc.info['name'].lower():
                    continue
                
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                for i, port in enumerate(target_ports):
                    if f"--remote-debugging-port={port}" in cmdline:
                        still_running.append(f"Chrome_{chrome_numbers[i]}")
                        break
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        if still_running:
            print(f"⚠️ 仍在运行: {still_running}")
            return False
        else:
            print("✅ 所有目标实例已成功关闭")
            return True

def main():
    parser = argparse.ArgumentParser(description='精准关闭特定Chrome实例')
    parser.add_argument('numbers', nargs='+', type=int, 
                       help='Chrome编号 (例如: 19 20)')
    parser.add_argument('-v', '--verify', action='store_true',
                       help='验证关闭结果')
    
    args = parser.parse_args()
    
    closer = SpecificChromeCloser()
    
    # 关闭指定实例
    closed_count = closer.close_by_numbers(args.numbers)
    
    if closed_count > 0:
        time.sleep(2)  # 等待进程完全关闭
        
        # 验证关闭结果
        if args.verify or True:  # 默认总是验证
            closer.verify_closure(args.numbers)
    else:
        print("ℹ️ 没有找到需要关闭的Chrome实例")

if __name__ == "__main__":
    main()
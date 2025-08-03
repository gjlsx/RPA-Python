#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chrome批量启动器
自动打开多个Chrome实例，每个实例打开指定网页
"""

import os
import sys
import time
import subprocess
import argparse
from pathlib import Path

class ChromeBatchLauncher:
    def __init__(self, chrome_dir=".", config_file="websites_config.txt"):
        self.chrome_dir = Path(chrome_dir)
        self.config_file = self.chrome_dir / config_file
        self.websites = []
        self.load_websites()
    
    def load_websites(self):
        """从配置文件加载网站列表"""
        if not self.config_file.exists():
            print(f"配置文件不存在: {self.config_file}")
            return
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    self.websites.append(line)
        
        print(f"已加载 {len(self.websites)} 个网站")
        for i, site in enumerate(self.websites, 1):
            print(f"  {i}. {site}")
    
    def find_chrome_shortcuts(self, start_num, end_num):
        """查找指定范围的Chrome快捷方式"""
        shortcuts = []
        for num in range(start_num, end_num + 1):
            shortcut_path = self.chrome_dir / f"Chrome_{num}.lnk"
            if shortcut_path.exists():
                shortcuts.append((num, shortcut_path))
            else:
                print(f"警告: 快捷方式不存在 - {shortcut_path}")
        
        return shortcuts
    
    def launch_chrome_instance(self, chrome_num, shortcut_path, delay=2):
        """启动单个Chrome实例并打开网页"""
        print(f"\n启动 Chrome_{chrome_num}...")
        
        try:
            # 启动Chrome快捷方式
            subprocess.Popen([str(shortcut_path)], shell=True)
            time.sleep(delay)  # 等待Chrome启动
            
            # 在该Chrome实例中打开网页
            chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            user_data_dir = f"c:\\tools\\chromes\\{chrome_num}\\"
            debug_port = 10000 + chrome_num
            
            for website in self.websites:
                cmd = [
                    chrome_exe,
                    f"--user-data-dir={user_data_dir}",
                    f"--remote-debugging-port={debug_port}",
                    website
                ]
                subprocess.Popen(cmd)
                time.sleep(0.5)  # 短暂延迟避免冲突
            
            print(f"Chrome_{chrome_num} 已启动，打开了 {len(self.websites)} 个网页")
            
        except Exception as e:
            print(f"启动 Chrome_{chrome_num} 失败: {e}")
    
    def launch_batch(self, start_num=11, end_num=20, delay=3):
        """批量启动Chrome实例"""
        print(f"准备启动 Chrome_{start_num} 到 Chrome_{end_num}")
        print(f"每个实例将打开 {len(self.websites)} 个网页")
        print(f"实例间延迟: {delay} 秒")
        
        shortcuts = self.find_chrome_shortcuts(start_num, end_num)
        
        if not shortcuts:
            print("没有找到任何Chrome快捷方式！")
            return
        
        print(f"\n找到 {len(shortcuts)} 个快捷方式，开始启动...")
        
        for chrome_num, shortcut_path in shortcuts:
            self.launch_chrome_instance(chrome_num, shortcut_path, delay)
        
        print(f"\n批量启动完成！共启动了 {len(shortcuts)} 个Chrome实例")

def main():
    parser = argparse.ArgumentParser(description='Chrome批量启动器')
    parser.add_argument('start', type=int, nargs='?', default=11, 
                       help='起始Chrome编号 (默认: 11)')
    parser.add_argument('end', type=int, nargs='?', default=20, 
                       help='结束Chrome编号 (默认: 20)')
    parser.add_argument('-d', '--delay', type=int, default=3,
                       help='实例间启动延迟秒数 (默认: 3)')
    parser.add_argument('-c', '--config', default='websites_config.txt',
                       help='网站配置文件 (默认: websites_config.txt)')
    
    args = parser.parse_args()
    
    # 确保在chrome目录中运行
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    launcher = ChromeBatchLauncher(config_file=args.config)
    launcher.launch_batch(args.start, args.end, args.delay)

if __name__ == "__main__":
    main()
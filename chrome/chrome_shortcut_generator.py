#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chrome快捷方式批量生成器
自动生成多个Chrome快捷方式，每个使用不同的用户数据目录和调试端口
放置在chrome目录下使用
"""

import os
import sys
import argparse
from pathlib import Path
import win32com.client

def create_chrome_shortcut(shortcut_path, target_path, user_data_dir, debug_port, working_dir):
    """
    创建Chrome快捷方式
    
    Args:
        shortcut_path: 快捷方式文件路径 (.lnk)
        target_path: Chrome可执行文件路径
        user_data_dir: 用户数据目录
        debug_port: 远程调试端口
        working_dir: 工作目录
    """
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        
        # 设置目标程序和参数
        shortcut.Targetpath = target_path
        shortcut.Arguments = f'--user-data-dir={user_data_dir} --remote-debugging-port={debug_port} --disable-session-crashed-bubble --disable-infobars --no-first-run --disable-restore-session-state --disable-background-mode --disable-background-timer-throttling --disable-backgrounding-occluded-windows --no-default-browser-check --disable-translate --disable-features=TranslateUI --disable-ipc-flooding-protection'
        
        # 设置工作目录
        shortcut.WorkingDirectory = working_dir
        
        # 设置窗口样式 (1=常规窗口, 3=最大化, 7=最小化)
        shortcut.WindowStyle = 1
        
        # 设置描述
        shortcut.Description = "访问互联网"
        
        # 保存快捷方式
        shortcut.save()
        
        print(f"✅ 成功创建快捷方式: {shortcut_path}")
        return True
        
    except Exception as e:
        print(f"❌ 创建快捷方式失败 {shortcut_path}: {e}")
        return False

def generate_chrome_shortcuts(start_num, count, output_dir=".", chrome_path=None, base_data_dir=None):
    """
    批量生成Chrome快捷方式
    
    Args:
        start_num: 起始序号
        count: 生成数量
        output_dir: 输出目录
        chrome_path: Chrome可执行文件路径
        base_data_dir: 用户数据基础目录
    """
    
    # 默认Chrome路径
    if chrome_path is None:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # 检查Chrome是否存在
    if not os.path.exists(chrome_path):
        # 尝试其他常见路径
        alternative_paths = [
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME'))
        ]
        
        for alt_path in alternative_paths:
            if os.path.exists(alt_path):
                chrome_path = alt_path
                break
        else:
            print(f"❌ 找不到Chrome可执行文件，请手动指定路径")
            return False
    
    # 默认用户数据基础目录
    if base_data_dir is None:
        base_data_dir = r"d:\tools\chromes"
    
    # Chrome工作目录
    working_dir = os.path.dirname(chrome_path)
    
    # 输出目录
    output_dir=base_data_dir
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 确保用户数据基础目录存在
    os.makedirs(base_data_dir, exist_ok=True)
    
    print(f"🚀 开始生成Chrome快捷方式...")
    print(f"📁 Chrome路径: {chrome_path}")
    print(f"📁 输出目录: {os.path.abspath(output_dir)}")
    print(f"📁 用户数据基础目录: {base_data_dir}")
    print(f"🔢 起始序号: {start_num}")
    print(f"🔢 生成数量: {count}")
    print("-" * 50)
    
    success_count = 0
    
    for i in range(count):
        current_num = start_num + i
        
        # 快捷方式文件名
        shortcut_name = f"Chrome_{current_num}.lnk"
        shortcut_path = os.path.join(output_dir, shortcut_name)
        
        # 用户数据目录
        user_data_dir = os.path.join(base_data_dir, str(current_num))
        
        # 调试端口 (基础端口 + 序号)
        debug_port = 10000 + current_num
        
        # 确保用户数据目录存在
        os.makedirs(user_data_dir, exist_ok=True)
        
        # 创建快捷方式
        if create_chrome_shortcut(shortcut_path, chrome_path, user_data_dir, debug_port, working_dir):
            success_count += 1
            print(f"  📋 序号: {current_num}")
            print(f"  📁 数据目录: {user_data_dir}")
            print(f"  🔌 调试端口: {debug_port}")
            print()
    
    print("-" * 50)
    print(f"🎉 完成！成功生成 {success_count}/{count} 个快捷方式")
    
    return success_count == count

def main():
    parser = argparse.ArgumentParser(
        description="Chrome快捷方式批量生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python chrome_shortcut_generator.py 11 10                    # 生成序号11-20的10个快捷方式
  python chrome_shortcut_generator.py 1 5 -o shortcuts        # 生成序号1-5的快捷方式到shortcuts目录
  python chrome_shortcut_generator.py 21 3 -c "D:\\Chrome\\chrome.exe"  # 指定Chrome路径
        """
    )
    
    parser.add_argument('start_num', type=int, help='起始序号')
    parser.add_argument('count', type=int, help='生成数量')
    parser.add_argument('-o', '--output', default='.', help='输出目录 (默认: d:\\tools\\chromes)')
    parser.add_argument('-c', '--chrome', help='Chrome可执行文件路径 (默认: 自动检测)')
    parser.add_argument('-d', '--data-dir', help='用户数据基础目录 (默认: d:\\tools\\chromes)')
    
    args = parser.parse_args()
    
    if args.count <= 0:
        print("❌ 生成数量必须大于0")
        return 1
    
    try:
        success = generate_chrome_shortcuts(
            start_num=args.start_num,
            count=args.count,
            output_dir=args.data_dir,
            chrome_path=args.chrome,
            base_data_dir=args.data_dir
        )
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️  操作被用户取消")
        return 1
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动Chrome_19和Chrome_20并打开指定网页 - 修正版
"""

import os
import time
import subprocess
import psutil
from pathlib import Path

# 账号配置
ACCOUNTS = {
    19: {
        'email': 'Alcinaedcvf@gmail.com',
        'password': 'w1zqK7Amyahh',
        'recovery_email': 'eyywdc4s5ecr@yeah.net',
        'location': '巴西'
    },
    20: {
        'email': 'Fdbcvdfxc453@gmail.com', 
        'password': 'm22U2Awbg4vA',
        'recovery_email': 'qyp83kyzee4t@yeah.net',
        'location': '巴西'
    }
}

# 网站列表
WEBSITES = [
    "https://www.gmail.com",
    "https://wipdf.vercel.app/"
]

def close_existing_chrome_instances():
    """关闭已存在的Chrome_19和Chrome_20进程"""
    target_ports = [10019, 10020]
    chrome_pids = []
    
    print("检查并关闭已存在的Chrome_19和Chrome_20进程...")
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'chrome.exe' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                # 检查是否包含目标端口或用户数据目录
                for port in target_ports:
                    if f"--remote-debugging-port={port}" in cmdline:
                        chrome_num = port - 10000
                        chrome_pids.append((proc.info['pid'], chrome_num))
                        break
                        
                for chrome_num in [19, 20]:
                    if f"--user-data-dir=c:\\tools\\chromes\\{chrome_num}\\" in cmdline:
                        chrome_pids.append((proc.info['pid'], chrome_num))
                        break
                        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # 关闭找到的进程
    for pid, chrome_num in chrome_pids:
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            print(f"关闭 Chrome_{chrome_num} (PID: {pid})")
            try:
                proc.wait(timeout=3)
            except psutil.TimeoutExpired:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if chrome_pids:
        time.sleep(2)
        print(f"已关闭 {len(chrome_pids)} 个Chrome进程")
    else:
        print("没有找到需要关闭的Chrome进程")

def launch_chrome_instance_with_websites(chrome_num):
    """启动Chrome实例并直接打开网页"""
    print(f"\n启动 Chrome_{chrome_num}...")
    
    # Chrome配置
    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data_dir = f"c:\\tools\\chromes\\{chrome_num}\\"
    debug_port = 10000 + chrome_num
    
    try:
        # 首先启动Chrome快捷方式（空白页面）
        shortcut_path = f"C:\\tools\\chromes\\Chrome_{chrome_num}.lnk"
        subprocess.Popen([shortcut_path], shell=True)
        time.sleep(3)  # 等待Chrome启动
        
        print(f"Chrome_{chrome_num} 启动成功")
        print(f"  - 用户数据目录: {user_data_dir}")
        print(f"  - 调试端口: {debug_port}")
        print(f"  - 打开 {len(WEBSITES)} 个网页...")
        
        # 在该Chrome实例中打开网页（每个网页在新标签页）
        for i, website in enumerate(WEBSITES, 1):
            cmd = [
                chrome_exe,
                f"--user-data-dir={user_data_dir}",
                f"--remote-debugging-port={debug_port}",
                website
            ]
            subprocess.Popen(cmd)
            print(f"    {i}. {website}")
            time.sleep(1)  # 短暂延迟避免冲突
        
        print(f"Chrome_{chrome_num} 已打开所有网页")
        return True
        
    except Exception as e:
        print(f"启动 Chrome_{chrome_num} 失败: {e}")
        return False

def main():
    """主函数"""
    print("启动Chrome_19和Chrome_20并打开指定网页")
    print("=" * 50)
    
    # 显示账号信息
    for chrome_num in [19, 20]:
        account = ACCOUNTS[chrome_num]
        print(f"Chrome_{chrome_num} 账号信息:")
        print(f"  邮箱: {account['email']}")
        print(f"  密码: {account['password']}")
        print(f"  备用邮箱: {account['recovery_email']}")
        print(f"  位置: {account['location']}")
    
    print("\n网页列表:")
    for i, site in enumerate(WEBSITES, 1):
        print(f"  {i}. {site}")
    
    print("\n" + "=" * 50)
    
    # 先关闭已存在的Chrome实例
    close_existing_chrome_instances()
    
    success_count = 0
    
    # 启动Chrome实例并打开网页
    for chrome_num in [19, 20]:
        if launch_chrome_instance_with_websites(chrome_num):
            success_count += 1
            time.sleep(2)  # 实例间延迟
    
    print(f"\n启动完成！成功启动了 {success_count} 个Chrome实例")
    print("现在你可以手动在每个Chrome实例中进行Google登录")
    print("登录信息已在上方显示")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    # 确保在chrome目录中运行
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动Chrome_19和Chrome_20并完成Google登录（包括二次验证）
"""

import os
import time
import subprocess
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# 账号配置（从allwebsite.txt读取）
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

def launch_chrome_instance(chrome_num):
    """启动Chrome实例"""
    print(f"\n启动 Chrome_{chrome_num}...")
    
    # 启动Chrome快捷方式
    shortcut_path = f"C:\\tools\\chromes\\Chrome_{chrome_num}.lnk"
    try:
        subprocess.Popen([shortcut_path], shell=True)
        time.sleep(4)  # 等待Chrome启动
        print(f"Chrome_{chrome_num} 启动成功")
        return True
    except Exception as e:
        print(f"启动 Chrome_{chrome_num} 失败: {e}")
        return False

def create_selenium_driver(chrome_num):
    """创建Selenium WebDriver连接到指定Chrome实例"""
    debug_port = 10000 + chrome_num
    
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print(f"成功连接到 Chrome_{chrome_num} (端口:{debug_port})")
        return driver
    except Exception as e:
        print(f"连接到 Chrome_{chrome_num} 失败: {e}")
        return None

def google_login_complete(driver, chrome_num):
    """完整的Google登录流程"""
    account = ACCOUNTS[chrome_num]
    print(f"\n开始完整Google登录流程 - Chrome_{chrome_num}")
    print(f"账号: {account['email']}")
    print(f"密码: {account['password']}")
    print(f"辅助邮箱: {account['recovery_email']}")
    
    try:
        # 1. 打开Google登录页面
        driver.get("https://accounts.google.com/signin")
        time.sleep(3)
        
        # 2. 输入邮箱
        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_input.clear()
            email_input.send_keys(account['email'])
            print(f"✓ 已输入邮箱: {account['email']}")
            
            # 点击下一步
            next_button = driver.find_element(By.ID, "identifierNext")
            next_button.click()
            time.sleep(4)
        except Exception as e:
            print(f"邮箱输入失败: {e}")
            return False
        
        # 3. 输入密码
        try:
            # 等待密码页面加载
            password_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(account['password'])
            print(f"✓ 已输入密码")
            
            # 点击下一步
            password_next = driver.find_element(By.ID, "passwordNext")
            password_next.click()
            time.sleep(5)
        except Exception as e:
            print(f"密码输入失败: {e}")
            return False
        
        # 4. 处理二次验证
        current_url = driver.current_url
        print(f"当前页面: {current_url}")
        
        if "challenge" in current_url or "signin/v2/challenge" in current_url:
            print("检测到二次验证页面...")
            
            # 尝试选择辅助邮箱验证
            try:
                # 查找辅助邮箱选项
                recovery_options = driver.find_elements(By.CSS_SELECTOR, "[data-action='selectchallenge']")
                
                for option in recovery_options:
                    option_text = option.text
                    print(f"找到验证选项: {option_text}")
                    
                    # 查找包含辅助邮箱部分信息的选项
                    if "qyp" in option_text or "yeah.net" in option_text or "通过" in option_text:
                        print("选择辅助邮箱验证...")
                        option.click()
                        time.sleep(3)
                        break
                
                print("请手动完成邮箱验证步骤...")
                print("1. 检查辅助邮箱获取验证码")
                print("2. 输入验证码")
                print("3. 完成登录")
                
                # 等待用户手动完成验证
                input("完成验证后按回车键继续...")
                
            except Exception as e:
                print(f"处理二次验证失败: {e}")
                print("请手动完成验证...")
                input("完成验证后按回车键继续...")
        
        # 5. 检查登录状态
        time.sleep(3)
        current_url = driver.current_url
        if "myaccount.google.com" in current_url or "gmail.com" in current_url:
            print(f"✓ Chrome_{chrome_num} Google登录成功！")
            return True
        else:
            print(f"Chrome_{chrome_num} 登录状态未确认，当前页面: {current_url}")
            return True  # 继续执行后续步骤
            
    except Exception as e:
        print(f"Chrome_{chrome_num} Google登录失败: {e}")
        return False

def open_additional_websites(driver, chrome_num):
    """在新标签页中打开其他网站"""
    print(f"\n在 Chrome_{chrome_num} 中打开其他网站...")
    
    for website in WEBSITES:
        try:
            # 打开新标签页
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(website)
            print(f"✓ 已打开: {website}")
            time.sleep(2)
        except Exception as e:
            print(f"打开 {website} 失败: {e}")

def main():
    """主函数"""
    print("启动Chrome_19和Chrome_20并完成Google登录")
    print("=" * 60)
    
    drivers = {}
    
    # 启动Chrome实例并登录
    for chrome_num in [19, 20]:
        print(f"\n{'='*20} Chrome_{chrome_num} {'='*20}")
        
        # 启动Chrome
        if launch_chrome_instance(chrome_num):
            time.sleep(2)
            
            # 创建Selenium连接
            driver = create_selenium_driver(chrome_num)
            if driver:
                drivers[chrome_num] = driver
                
                # 执行Google登录
                if google_login_complete(driver, chrome_num):
                    # 打开其他网站
                    open_additional_websites(driver, chrome_num)
                    print(f"✓ Chrome_{chrome_num} 所有操作完成")
                else:
                    print(f"✗ Chrome_{chrome_num} 登录失败")
    
    print(f"\n{'='*60}")
    print(f"操作完成！成功启动并操作了 {len(drivers)} 个Chrome实例")
    print("所有Chrome实例将保持运行状态")
    
    # 保持连接，等待用户确认
    input("\n按回车键断开Selenium连接（Chrome将继续运行）...")
    
    # 关闭所有driver连接（不关闭浏览器）
    for chrome_num, driver in drivers.items():
        try:
            driver.quit()
            print(f"已断开与 Chrome_{chrome_num} 的连接")
        except:
            pass

if __name__ == "__main__":
    # 确保在chrome目录中运行
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    main()
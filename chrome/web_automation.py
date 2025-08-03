#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页自动化操作模块
基于Selenium的通用网页操作封装
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class WebAutomation:
    def __init__(self, chrome_num, timeout=10):
        """
        初始化网页自动化操作
        
        Args:
            chrome_num: Chrome实例编号
            timeout: 默认等待超时时间
        """
        self.chrome_num = chrome_num
        self.timeout = timeout
        self.driver = None
        self.wait = None
        
    def connect_to_chrome(self):
        """连接到指定Chrome实例"""
        debug_port = 10000 + self.chrome_num
        
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, self.timeout)
            print(f"✅ 成功连接到 Chrome_{self.chrome_num}")
            return True
        except Exception as e:
            print(f"❌ 连接Chrome_{self.chrome_num}失败: {e}")
            return False
    
    def navigate_to(self, url):
        """导航到指定URL"""
        try:
            self.driver.get(url)
            print(f"📍 导航到: {url}")
            return True
        except Exception as e:
            print(f"❌ 导航失败: {e}")
            return False
    
    def find_element_safe(self, by, value, timeout=None):
        """安全查找元素"""
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"⚠️ 元素未找到: {by}={value}")
            return None
    
    def click_element(self, by, value, timeout=None):
        """点击元素"""
        element = self.find_element_safe(by, value, timeout)
        if element:
            try:
                # 等待元素可点击
                WebDriverWait(self.driver, timeout or self.timeout).until(
                    EC.element_to_be_clickable((by, value))
                )
                element.click()
                print(f"🖱️ 点击成功: {by}={value}")
                return True
            except Exception as e:
                print(f"❌ 点击失败: {e}")
                return False
        return False
    
    def input_text(self, by, value, text, clear_first=True):
        """输入文本"""
        element = self.find_element_safe(by, value)
        if element:
            try:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                print(f"⌨️ 输入成功: {text}")
                return True
            except Exception as e:
                print(f"❌ 输入失败: {e}")
                return False
        return False
    
    def press_key(self, by, value, key):
        """按键操作"""
        element = self.find_element_safe(by, value)
        if element:
            try:
                element.send_keys(key)
                print(f"⌨️ 按键成功: {key}")
                return True
            except Exception as e:
                print(f"❌ 按键失败: {e}")
                return False
        return False
    
    def wait_for_element(self, by, value, timeout=None):
        """等待元素出现"""
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            print(f"✅ 元素已出现: {by}={value}")
            return element
        except TimeoutException:
            print(f"⏰ 等待超时: {by}={value}")
            return None
    
    def get_element_text(self, by, value):
        """获取元素文本"""
        element = self.find_element_safe(by, value)
        if element:
            try:
                text = element.text
                print(f"📝 获取文本: {text}")
                return text
            except Exception as e:
                print(f"❌ 获取文本失败: {e}")
                return None
        return None
    
    def scroll_to_element(self, by, value):
        """滚动到元素"""
        element = self.find_element_safe(by, value)
        if element:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                print(f"📜 滚动到元素: {by}={value}")
                return True
            except Exception as e:
                print(f"❌ 滚动失败: {e}")
                return False
        return False
    
    def execute_script(self, script):
        """执行JavaScript"""
        try:
            result = self.driver.execute_script(script)
            print(f"🔧 执行脚本成功")
            return result
        except Exception as e:
            print(f"❌ 执行脚本失败: {e}")
            return None
    
    def take_screenshot(self, filename=None):
        """截图"""
        if not filename:
            filename = f"chrome_{self.chrome_num}_{int(time.time())}.png"
        
        try:
            self.driver.save_screenshot(filename)
            print(f"📸 截图保存: {filename}")
            return filename
        except Exception as e:
            print(f"❌ 截图失败: {e}")
            return None
    
    def close_connection(self):
        """关闭连接（保持浏览器运行）"""
        if self.driver:
            try:
                self.driver.quit()
                print(f"🔌 已断开与Chrome_{self.chrome_num}的连接")
            except:
                pass
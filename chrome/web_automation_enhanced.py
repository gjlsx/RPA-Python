#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版网页自动化操作模块
基于web_automation.py的增强版本，支持更复杂的操作和错误处理
"""

import time
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from chrome_popup_handler import ChromePopupHandler

class EnhancedWebAutomation:
    def __init__(self, chrome_num, timeout=15, config_file=None):
        """
        初始化增强版网页自动化操作
        
        Args:
            chrome_num: Chrome实例编号
            timeout: 默认等待超时时间
            config_file: 配置文件路径
        """
        self.chrome_num = chrome_num
        self.timeout = timeout
        self.driver = None
        self.wait = None
        self.popup_handler = None
        self.operation_log = []
        
        # 加载配置
        self.config = self.load_config(config_file)
        
    def load_config(self, config_file):
        """加载配置文件"""
        if config_file and Path(config_file).exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "retry_attempts": 3,
            "retry_delay": 2,
            "implicit_wait": 10,
            "page_load_timeout": 30,
            "element_wait_timeout": 15
        }
    
    def connect_to_chrome(self):
        """连接到指定Chrome实例"""
        debug_port = 10000 + self.chrome_num
        
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(self.config.get("implicit_wait", 10))
            self.driver.set_page_load_timeout(self.config.get("page_load_timeout", 30))
            
            self.wait = WebDriverWait(self.driver, self.timeout)
            self.popup_handler = ChromePopupHandler(self.driver)
            
            self.log_operation("connect", f"成功连接到 Chrome_{self.chrome_num}")
            return True
        except Exception as e:
            self.log_operation("connect", f"连接Chrome_{self.chrome_num}失败: {e}", "ERROR")
            return False
    
    def log_operation(self, operation, message, level="INFO"):
        """记录操作日志"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "chrome_num": self.chrome_num,
            "operation": operation,
            "message": message,
            "level": level
        }
        self.operation_log.append(log_entry)
        
        # 控制台输出
        prefix = "✅" if level == "INFO" else "❌" if level == "ERROR" else "⚠️"
        print(f"{prefix} [{timestamp}] Chrome_{self.chrome_num}: {message}")
    
    def navigate_to_with_retry(self, url, max_retries=None):
        """带重试的页面导航"""
        max_retries = max_retries or self.config.get("retry_attempts", 3)
        
        for attempt in range(max_retries):
            try:
                self.driver.get(url)
                self.popup_handler.handle_all_popups()
                self.log_operation("navigate", f"成功导航到: {url}")
                return True
            except Exception as e:
                self.log_operation("navigate", f"导航失败 (尝试 {attempt+1}/{max_retries}): {e}", "ERROR")
                if attempt < max_retries - 1:
                    time.sleep(self.config.get("retry_delay", 2))
                    continue
                return False
        return False
    
    def smart_find_element(self, selectors, timeout=None):
        """智能元素查找 - 支持多种选择器"""
        timeout = timeout or self.config.get("element_wait_timeout", 15)
        wait = WebDriverWait(self.driver, timeout)
        
        if isinstance(selectors, str):
            selectors = [selectors]
        
        for selector in selectors:
            try:
                # 尝试不同的定位方式
                if selector.startswith("//"):
                    element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                elif selector.startswith("#"):
                    element = wait.until(EC.presence_of_element_located((By.ID, selector[1:])))
                elif selector.startswith("."):
                    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, selector[1:])))
                else:
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                
                self.log_operation("find_element", f"找到元素: {selector}")
                return element
            except TimeoutException:
                continue
        
        self.log_operation("find_element", f"未找到任何元素: {selectors}", "ERROR")
        return None
    
    def smart_click(self, selectors, timeout=None):
        """智能点击 - 支持多种点击方式"""
        element = self.smart_find_element(selectors, timeout)
        if not element:
            return False
        
        try:
            # 尝试普通点击
            element.click()
            self.log_operation("click", f"成功点击元素")
            return True
        except Exception as e:
            try:
                # 尝试JavaScript点击
                self.driver.execute_script("arguments[0].click();", element)
                self.log_operation("click", f"通过JavaScript成功点击元素")
                return True
            except Exception as e2:
                try:
                    # 尝试ActionChains点击
                    ActionChains(self.driver).move_to_element(element).click().perform()
                    self.log_operation("click", f"通过ActionChains成功点击元素")
                    return True
                except Exception as e3:
                    self.log_operation("click", f"点击失败: {e3}", "ERROR")
                    return False
    
    def smart_input(self, selectors, text, clear_first=True, timeout=None):
        """智能输入文本"""
        element = self.smart_find_element(selectors, timeout)
        if not element:
            return False
        
        try:
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.log_operation("input", f"成功输入文本: {text[:20]}...")
            return True
        except Exception as e:
            self.log_operation("input", f"输入失败: {e}", "ERROR")
            return False
    
    def wait_for_page_load(self, timeout=30):
        """等待页面完全加载"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            self.log_operation("page_load", "页面加载完成")
            return True
        except TimeoutException:
            self.log_operation("page_load", "页面加载超时", "ERROR")
            return False
    
    def execute_action_sequence(self, actions):
        """执行动作序列"""
        results = []
        
        for i, action in enumerate(actions):
            action_type = action.get("type")
            success = False
            
            try:
                if action_type == "navigate":
                    success = self.navigate_to_with_retry(action["url"])
                elif action_type == "click":
                    success = self.smart_click(action["selectors"])
                elif action_type == "input":
                    success = self.smart_input(action["selectors"], action["text"])
                elif action_type == "wait":
                    time.sleep(action.get("seconds", 1))
                    success = True
                elif action_type == "wait_element":
                    element = self.smart_find_element(action["selectors"])
                    success = element is not None
                
                results.append({
                    "action_index": i,
                    "action_type": action_type,
                    "success": success
                })
                
                if not success and action.get("required", True):
                    self.log_operation("sequence", f"必需动作失败，停止执行: {action_type}", "ERROR")
                    break
                    
            except Exception as e:
                self.log_operation("sequence", f"动作执行异常: {e}", "ERROR")
                results.append({
                    "action_index": i,
                    "action_type": action_type,
                    "success": False,
                    "error": str(e)
                })
                break
        
        return results
    
    def save_operation_log(self, filename=None):
        """保存操作日志"""
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"chrome_{self.chrome_num}_operations_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.operation_log, f, ensure_ascii=False, indent=2)
            print(f"📝 操作日志已保存: {filename}")
            return True
        except Exception as e:
            print(f"❌ 保存日志失败: {e}")
            return False
    
    def close(self):
        """关闭连接"""
        if self.driver:
            try:
                self.driver.quit()
                self.log_operation("close", "已关闭WebDriver连接")
            except Exception as e:
                self.log_operation("close", f"关闭连接时出错: {e}", "ERROR")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()

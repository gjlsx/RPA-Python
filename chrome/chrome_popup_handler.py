#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chrome弹窗自动处理模块
自动检测并处理各种Chrome弹窗，如隐私设置、广告设置等
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ChromePopupHandler:
    def __init__(self, driver, timeout=5):
        """
        初始化弹窗处理器
        
        Args:
            driver: Selenium WebDriver实例
            timeout: 等待弹窗出现的超时时间（秒）
        """
        self.driver = driver
        self.timeout = timeout
        
        # 定义各种弹窗的选择器
        self.popup_selectors = {
            # Chrome隐私/广告设置弹窗
            'privacy_dialog': [
                '//button[contains(text(), "知道了")]',
                '//button[contains(text(), "Got it")]',
                '//button[contains(text(), "OK")]',
                '//button[@data-test-id="got-it-button"]',
                '//div[contains(@class, "privacy")]//button[contains(text(), "知道了")]',
                '//div[contains(@class, "dialog")]//button[contains(text(), "知道了")]'
            ],
            
            # Chrome更新通知
            'update_notification': [
                '//button[contains(text(), "不用了")]',
                '//button[contains(text(), "No thanks")]',
                '//button[contains(text(), "Later")]',
                '//button[@aria-label="Dismiss"]'
            ],
            
            # Cookie通知
            'cookie_notice': [
                '//button[contains(text(), "接受")]',
                '//button[contains(text(), "Accept")]',
                '//button[contains(text(), "Allow")]'
            ],
            
            # 通用关闭按钮
            'generic_close': [
                '//button[@aria-label="Close"]',
                '//button[@aria-label="关闭"]',
                '//button[contains(@class, "close")]',
                '//span[contains(@class, "close")]',
                '//div[contains(@class, "close")]'
            ]
        }
    
    def check_and_handle_popups(self, popup_types=None):
        """
        检查并处理弹窗
        
        Args:
            popup_types: 要处理的弹窗类型列表，None表示处理所有类型
            
        Returns:
            bool: 如果处理了任何弹窗返回True，否则返回False
        """
        if popup_types is None:
            popup_types = list(self.popup_selectors.keys())
        
        handled = False
        
        for popup_type in popup_types:
            if self._handle_popup_type(popup_type):
                handled = True
                print(f"✅ 已处理 {popup_type} 弹窗")
                time.sleep(1)  # 等待弹窗消失
        
        return handled
    
    def _handle_popup_type(self, popup_type):
        """处理特定类型的弹窗"""
        if popup_type not in self.popup_selectors:
            return False
        
        selectors = self.popup_selectors[popup_type]
        
        for selector in selectors:
            try:
                element = WebDriverWait(self.driver, self.timeout).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                element.click()
                print(f"✅ 点击了弹窗按钮: {selector}")
                return True
                
            except TimeoutException:
                continue
            except Exception as e:
                print(f"⚠️ 处理弹窗时出错: {e}")
                continue
        
        return False
    
    def handle_privacy_popup(self):
        """专门处理隐私设置弹窗"""
        return self._handle_popup_type('privacy_dialog')

    def handle_all_popups(self):
        """处理所有类型的弹窗 - 一次性检查"""
        handled_count = 0
        for popup_type in self.popup_selectors.keys():
            if self._handle_popup_type(popup_type):
                handled_count += 1
        return handled_count > 0
    
    def handle_all_popups_continuous(self, duration=30, check_interval=2):
        """
        持续监控并处理弹窗
        
        Args:
            duration: 监控持续时间（秒）
            check_interval: 检查间隔（秒）
        """
        start_time = time.time()
        handled_count = 0
        
        print(f"🔍 开始持续监控弹窗，持续 {duration} 秒...")
        
        while time.time() - start_time < duration:
            if self.check_and_handle_popups():
                handled_count += 1
            time.sleep(check_interval)
        
        print(f"🎉 监控完成，共处理了 {handled_count} 个弹窗")
        return handled_count

def test_popup_handler():
    """测试弹窗处理器"""
    from selenium.webdriver.chrome.options import Options
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:10011")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ 成功连接到Chrome实例")
        
        # 创建弹窗处理器
        popup_handler = ChromePopupHandler(driver)
        
        # 检查当前页面是否有弹窗
        popup_handler.check_and_handle_popups()
        
        # 持续监控30秒
        popup_handler.handle_all_popups_continuous(duration=30, check_interval=3)
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    test_popup_handler()

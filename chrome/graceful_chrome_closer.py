#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优雅关闭Chrome实例
通过Selenium优雅关闭，避免"要恢复页面吗？"对话框
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import psutil
from close_specific_chrome import SpecificChromeCloser

class GracefulChromeCloser:
    def __init__(self):
        self.fallback_closer = SpecificChromeCloser()
    
    def graceful_close_chrome(self, chrome_numbers):
        """优雅关闭Chrome实例"""
        print(f"🕊️ 优雅关闭Chrome实例: {chrome_numbers}")
        
        successfully_closed = []
        failed_to_close = []
        
        for chrome_num in chrome_numbers:
            print(f"\n🔄 处理Chrome_{chrome_num}...")
            
            if self._graceful_close_single(chrome_num):
                successfully_closed.append(chrome_num)
                print(f"  ✅ Chrome_{chrome_num}已优雅关闭")
            else:
                failed_to_close.append(chrome_num)
                print(f"  ❌ Chrome_{chrome_num}优雅关闭失败")
        
        # 对失败的实例使用强制关闭
        if failed_to_close:
            print(f"\n🔨 对失败实例使用强制关闭: {failed_to_close}")
            self.fallback_closer.close_by_numbers(failed_to_close)
            successfully_closed.extend(failed_to_close)
        
        print(f"\n📊 关闭结果:")
        print(f"  成功关闭: {successfully_closed}")
        print(f"  总计: {len(successfully_closed)}个实例")
        
        return len(successfully_closed) > 0
    
    def _graceful_close_single(self, chrome_num):
        """优雅关闭单个Chrome实例"""
        port = 10000 + chrome_num
        
        try:
            # 连接到Chrome实例
            chrome_options = Options()
            chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{port}')
            
            driver = webdriver.Chrome(options=chrome_options)
            print(f"  🔗 已连接到Chrome_{chrome_num}")
            
            # 获取所有标签页
            handles = driver.window_handles
            print(f"  📋 发现{len(handles)}个标签页")
            
            # 逐个关闭标签页（保留最后一个）
            for i, handle in enumerate(handles[:-1]):
                try:
                    driver.switch_to.window(handle)
                    driver.close()
                    print(f"    ✅ 已关闭标签页 {i+1}")
                    time.sleep(0.5)
                except:
                    print(f"    ⚠️ 关闭标签页 {i+1} 失败")
            
            # 切换到最后一个标签页并关闭整个浏览器
            if handles:
                try:
                    driver.switch_to.window(handles[-1])
                    print(f"  🏠 切换到最后一个标签页")
                    
                    # 清除会话存储，避免恢复对话框
                    driver.execute_script("sessionStorage.clear();")
                    driver.execute_script("localStorage.clear();")
                    print(f"  🧹 已清除会话数据")
                    
                    # 优雅退出
                    driver.quit()
                    print(f"  🚪 已发送退出命令")
                    
                except Exception as e:
                    print(f"  ⚠️ 退出时出错: {e}")
                    driver.quit()
            
            # 等待进程完全关闭
            time.sleep(2)
            
            # 验证是否真的关闭了
            if self._verify_chrome_closed(chrome_num):
                return True
            else:
                print(f"  ⚠️ Chrome_{chrome_num}仍在运行，需要强制关闭")
                return False
                
        except Exception as e:
            print(f"  ❌ 连接Chrome_{chrome_num}失败: {e}")
            return False
    
    def _verify_chrome_closed(self, chrome_num):
        """验证Chrome实例是否已关闭"""
        target_port = 10000 + chrome_num
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'chrome.exe' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if f"--remote-debugging-port={target_port}" in cmdline:
                        return False
            except:
                continue
        
        return True
    
    def close_with_session_cleanup(self, chrome_numbers):
        """关闭Chrome并清理会话，防止恢复对话框"""
        print(f"🧹 关闭Chrome并清理会话: {chrome_numbers}")
        
        for chrome_num in chrome_numbers:
            port = 10000 + chrome_num
            
            try:
                # 连接并清理会话
                chrome_options = Options()
                chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{port}')
                
                driver = webdriver.Chrome(options=chrome_options)
                
                # 在所有标签页中清理会话
                handles = driver.window_handles
                for handle in handles:
                    try:
                        driver.switch_to.window(handle)
                        # 清理各种存储
                        driver.execute_script("""
                            // 清理所有存储
                            sessionStorage.clear();
                            localStorage.clear();
                            
                            // 清理IndexedDB
                            if (window.indexedDB) {
                                indexedDB.databases().then(databases => {
                                    databases.forEach(db => {
                                        indexedDB.deleteDatabase(db.name);
                                    });
                                });
                            }
                            
                            // 设置标记，表示正常关闭
                            sessionStorage.setItem('graceful_shutdown', 'true');
                        """)
                        time.sleep(0.2)
                    except:
                        pass
                
                print(f"  🧹 Chrome_{chrome_num}会话数据已清理")
                driver.quit()
                
            except Exception as e:
                print(f"  ⚠️ Chrome_{chrome_num}会话清理失败: {e}")
        
        # 等待一下再强制关闭
        time.sleep(2)
        
        # 使用强制关闭确保完全关闭
        self.fallback_closer.close_by_numbers(chrome_numbers)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='优雅关闭Chrome实例')
    parser.add_argument('numbers', nargs='+', type=int, help='Chrome编号')
    parser.add_argument('--cleanup', action='store_true', help='清理会话数据')
    
    args = parser.parse_args()
    
    closer = GracefulChromeCloser()
    
    if args.cleanup:
        closer.close_with_session_cleanup(args.numbers)
    else:
        closer.graceful_close_chrome(args.numbers)

if __name__ == "__main__":
    main()

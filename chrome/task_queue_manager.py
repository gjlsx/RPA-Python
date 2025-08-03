#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务队列管理器
管理多个Chrome实例的批量操作任务，支持并发执行和任务调度
"""

import time
import json
import threading
from queue import Queue, Empty
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from web_automation_enhanced import EnhancedWebAutomation

class TaskQueueManager:
    def __init__(self, max_workers=5, config_file=None):
        """
        初始化任务队列管理器
        
        Args:
            max_workers: 最大并发工作线程数
            config_file: 配置文件路径
        """
        self.max_workers = max_workers
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.active_tasks = {}
        self.completed_tasks = []
        self.failed_tasks = []
        
        # 加载配置
        self.config = self.load_config(config_file)
        
        # 线程锁
        self.lock = threading.Lock()
        
    def load_config(self, config_file):
        """加载配置文件"""
        if config_file and Path(config_file).exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "task_timeout": 300,  # 5分钟
            "retry_failed_tasks": True,
            "max_retries": 2,
            "retry_delay": 5,
            "save_logs": True,
            "log_directory": "logs"
        }
    
    def add_task(self, task_id, chrome_num, actions, priority=1, metadata=None):
        """
        添加任务到队列
        
        Args:
            task_id: 任务唯一标识
            chrome_num: Chrome实例编号
            actions: 动作序列列表
            priority: 任务优先级 (数字越小优先级越高)
            metadata: 任务元数据
        """
        task = {
            "task_id": task_id,
            "chrome_num": chrome_num,
            "actions": actions,
            "priority": priority,
            "metadata": metadata or {},
            "created_at": time.time(),
            "status": "pending"
        }
        
        self.task_queue.put((priority, task))
        print(f"📋 已添加任务: {task_id} (Chrome_{chrome_num})")
    
    def add_batch_tasks(self, tasks_config):
        """
        批量添加任务
        
        Args:
            tasks_config: 任务配置列表或配置文件路径
        """
        if isinstance(tasks_config, str):
            # 从文件加载
            with open(tasks_config, 'r', encoding='utf-8') as f:
                tasks_config = json.load(f)
        
        for task_config in tasks_config:
            self.add_task(
                task_config["task_id"],
                task_config["chrome_num"],
                task_config["actions"],
                task_config.get("priority", 1),
                task_config.get("metadata")
            )
        
        print(f"📋 已批量添加 {len(tasks_config)} 个任务")
    
    def execute_task(self, task):
        """执行单个任务"""
        task_id = task["task_id"]
        chrome_num = task["chrome_num"]
        actions = task["actions"]
        
        print(f"🚀 开始执行任务: {task_id} (Chrome_{chrome_num})")
        
        # 更新任务状态
        with self.lock:
            self.active_tasks[task_id] = task
            task["status"] = "running"
            task["started_at"] = time.time()
        
        try:
            # 创建自动化实例并执行任务
            with EnhancedWebAutomation(chrome_num) as automation:
                if not automation.connect_to_chrome():
                    raise Exception(f"无法连接到 Chrome_{chrome_num}")
                
                # 执行动作序列
                results = automation.execute_action_sequence(actions)
                
                # 保存日志
                if self.config.get("save_logs", True):
                    log_dir = Path(self.config.get("log_directory", "logs"))
                    log_dir.mkdir(exist_ok=True)
                    log_file = log_dir / f"task_{task_id}_{int(time.time())}.json"
                    automation.save_operation_log(str(log_file))
                
                # 计算成功率
                total_actions = len(results)
                successful_actions = sum(1 for r in results if r["success"])
                success_rate = successful_actions / total_actions if total_actions > 0 else 0
                
                task_result = {
                    "task_id": task_id,
                    "chrome_num": chrome_num,
                    "status": "completed" if success_rate > 0.8 else "partial_success",
                    "success_rate": success_rate,
                    "total_actions": total_actions,
                    "successful_actions": successful_actions,
                    "results": results,
                    "completed_at": time.time(),
                    "duration": time.time() - task["started_at"]
                }
                
                print(f"✅ 任务完成: {task_id} (成功率: {success_rate:.1%})")
                return task_result
                
        except Exception as e:
            task_result = {
                "task_id": task_id,
                "chrome_num": chrome_num,
                "status": "failed",
                "error": str(e),
                "completed_at": time.time(),
                "duration": time.time() - task["started_at"]
            }
            
            print(f"❌ 任务失败: {task_id} - {e}")
            return task_result
        
        finally:
            # 清理活动任务
            with self.lock:
                if task_id in self.active_tasks:
                    del self.active_tasks[task_id]
    
    def run_tasks(self, timeout=None):
        """
        运行所有队列中的任务
        
        Args:
            timeout: 总超时时间（秒）
        """
        if self.task_queue.empty():
            print("📋 任务队列为空")
            return
        
        start_time = time.time()
        timeout = timeout or self.config.get("task_timeout", 300)
        
        print(f"🚀 开始执行任务队列 (最大并发: {self.max_workers})")
        
        # 收集所有任务
        tasks = []
        while not self.task_queue.empty():
            try:
                priority, task = self.task_queue.get_nowait()
                tasks.append(task)
            except Empty:
                break
        
        # 按优先级排序
        tasks.sort(key=lambda x: x["priority"])
        
        # 使用线程池执行任务
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_task = {
                executor.submit(self.execute_task, task): task 
                for task in tasks
            }
            
            # 收集结果
            for future in as_completed(future_to_task, timeout=timeout):
                task = future_to_task[future]
                try:
                    result = future.result()
                    
                    if result["status"] == "completed":
                        self.completed_tasks.append(result)
                    else:
                        self.failed_tasks.append(result)
                        
                        # 重试失败的任务
                        if (self.config.get("retry_failed_tasks", True) and 
                            task.get("retry_count", 0) < self.config.get("max_retries", 2)):
                            
                            task["retry_count"] = task.get("retry_count", 0) + 1
                            print(f"🔄 重试任务: {task['task_id']} (第{task['retry_count']}次)")
                            
                            time.sleep(self.config.get("retry_delay", 5))
                            self.add_task(
                                f"{task['task_id']}_retry_{task['retry_count']}",
                                task["chrome_num"],
                                task["actions"],
                                task["priority"],
                                task["metadata"]
                            )
                    
                except Exception as e:
                    print(f"❌ 任务执行异常: {task['task_id']} - {e}")
                    self.failed_tasks.append({
                        "task_id": task["task_id"],
                        "chrome_num": task["chrome_num"],
                        "status": "error",
                        "error": str(e),
                        "completed_at": time.time()
                    })
        
        # 输出执行结果
        total_time = time.time() - start_time
        total_tasks = len(self.completed_tasks) + len(self.failed_tasks)
        success_rate = len(self.completed_tasks) / total_tasks if total_tasks > 0 else 0
        
        print(f"\n📊 任务执行完成:")
        print(f"   总任务数: {total_tasks}")
        print(f"   成功任务: {len(self.completed_tasks)}")
        print(f"   失败任务: {len(self.failed_tasks)}")
        print(f"   成功率: {success_rate:.1%}")
        print(f"   总耗时: {total_time:.1f}秒")
    
    def get_status_report(self):
        """获取状态报告"""
        with self.lock:
            active_count = len(self.active_tasks)
            pending_count = self.task_queue.qsize()
        
        return {
            "pending_tasks": pending_count,
            "active_tasks": active_count,
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "active_task_details": list(self.active_tasks.keys())
        }
    
    def save_results(self, filename=None):
        """保存执行结果"""
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"task_results_{timestamp}.json"
        
        results = {
            "summary": {
                "total_tasks": len(self.completed_tasks) + len(self.failed_tasks),
                "completed_tasks": len(self.completed_tasks),
                "failed_tasks": len(self.failed_tasks),
                "success_rate": len(self.completed_tasks) / (len(self.completed_tasks) + len(self.failed_tasks)) if (len(self.completed_tasks) + len(self.failed_tasks)) > 0 else 0
            },
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"📝 执行结果已保存: {filename}")
            return True
        except Exception as e:
            print(f"❌ 保存结果失败: {e}")
            return False

def create_sample_tasks():
    """创建示例任务配置"""
    sample_tasks = [
        {
            "task_id": "google_search_task_1",
            "chrome_num": 11,
            "priority": 1,
            "actions": [
                {
                    "type": "navigate",
                    "url": "https://www.google.com"
                },
                {
                    "type": "input",
                    "selectors": ["input[name='q']", "//input[@name='q']"],
                    "text": "Python automation"
                },
                {
                    "type": "click",
                    "selectors": ["input[name='btnK']", "//input[@name='btnK']"]
                }
            ],
            "metadata": {
                "description": "Google搜索测试",
                "category": "search"
            }
        },
        {
            "task_id": "github_visit_task_2",
            "chrome_num": 12,
            "priority": 2,
            "actions": [
                {
                    "type": "navigate",
                    "url": "https://github.com"
                },
                {
                    "type": "wait",
                    "seconds": 3
                }
            ],
            "metadata": {
                "description": "访问GitHub",
                "category": "visit"
            }
        }
    ]
    
    with open("sample_tasks.json", 'w', encoding='utf-8') as f:
        json.dump(sample_tasks, f, ensure_ascii=False, indent=2)
    
    print("📝 已创建示例任务配置文件: sample_tasks.json")

if __name__ == "__main__":
    # 创建示例任务
    create_sample_tasks()
    
    # 示例用法
    manager = TaskQueueManager(max_workers=3)
    manager.add_batch_tasks("sample_tasks.json")
    manager.run_tasks()
    manager.save_results()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
操作监控和日志模块
实时监控Chrome实例状态、操作执行情况和系统资源使用
"""

import time
import json
import psutil
import threading
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, deque

class OperationMonitor:
    def __init__(self, log_directory="logs", max_log_entries=1000):
        """
        初始化操作监控器
        
        Args:
            log_directory: 日志目录
            max_log_entries: 内存中保存的最大日志条目数
        """
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)
        
        self.max_log_entries = max_log_entries
        self.operation_logs = deque(maxlen=max_log_entries)
        self.chrome_status = {}
        self.system_metrics = deque(maxlen=100)  # 保存最近100个系统指标
        
        # 统计数据
        self.stats = {
            "total_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "chrome_instances": set(),
            "operation_types": defaultdict(int),
            "error_types": defaultdict(int)
        }
        
        # 监控线程控制
        self.monitoring = False
        self.monitor_thread = None
        self.lock = threading.Lock()
        
        # 启动监控
        self.start_monitoring()
    
    def log_operation(self, chrome_num, operation_type, message, level="INFO", details=None):
        """
        记录操作日志
        
        Args:
            chrome_num: Chrome实例编号
            operation_type: 操作类型
            message: 日志消息
            level: 日志级别 (INFO, WARNING, ERROR)
            details: 详细信息字典
        """
        timestamp = datetime.now()
        
        log_entry = {
            "timestamp": timestamp.isoformat(),
            "chrome_num": chrome_num,
            "operation_type": operation_type,
            "message": message,
            "level": level,
            "details": details or {}
        }
        
        with self.lock:
            self.operation_logs.append(log_entry)
            
            # 更新统计
            self.stats["total_operations"] += 1
            self.stats["chrome_instances"].add(chrome_num)
            self.stats["operation_types"][operation_type] += 1
            
            if level == "INFO":
                self.stats["successful_operations"] += 1
            elif level == "ERROR":
                self.stats["failed_operations"] += 1
                error_type = details.get("error_type", "unknown") if details else "unknown"
                self.stats["error_types"][error_type] += 1
        
        # 控制台输出
        prefix = "✅" if level == "INFO" else "⚠️" if level == "WARNING" else "❌"
        print(f"{prefix} [{timestamp.strftime('%H:%M:%S')}] Chrome_{chrome_num}: {message}")
        
        # 写入日志文件
        self._write_to_log_file(log_entry)
    
    def _write_to_log_file(self, log_entry):
        """写入日志文件"""
        try:
            date_str = datetime.now().strftime("%Y%m%d")
            log_file = self.log_directory / f"operations_{date_str}.log"
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"❌ 写入日志文件失败: {e}")
    
    def update_chrome_status(self, chrome_num, status, details=None):
        """
        更新Chrome实例状态
        
        Args:
            chrome_num: Chrome实例编号
            status: 状态 (running, stopped, error, busy)
            details: 状态详细信息
        """
        with self.lock:
            self.chrome_status[chrome_num] = {
                "status": status,
                "last_updated": datetime.now().isoformat(),
                "details": details or {}
            }
        
        self.log_operation(chrome_num, "status_update", f"状态更新: {status}", details=details)
    
    def collect_system_metrics(self):
        """收集系统指标"""
        try:
            # CPU和内存使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Chrome进程信息
            chrome_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'cmdline']):
                try:
                    if proc.info['name'] and 'chrome.exe' in proc.info['name'].lower():
                        chrome_processes.append({
                            "pid": proc.info['pid'],
                            "cpu_percent": proc.info['cpu_percent'],
                            "memory_mb": proc.info['memory_info'].rss / 1024 / 1024,
                            "cmdline": ' '.join(proc.info['cmdline'][:3]) if proc.info['cmdline'] else ""
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_available_gb": memory.available / 1024 / 1024 / 1024
                },
                "chrome_processes": {
                    "count": len(chrome_processes),
                    "total_memory_mb": sum(p["memory_mb"] for p in chrome_processes),
                    "total_cpu_percent": sum(p["cpu_percent"] for p in chrome_processes),
                    "processes": chrome_processes
                }
            }
            
            with self.lock:
                self.system_metrics.append(metrics)
            
            return metrics
            
        except Exception as e:
            print(f"❌ 收集系统指标失败: {e}")
            return None
    
    def start_monitoring(self):
        """启动后台监控"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("🔍 操作监控已启动")
    
    def stop_monitoring(self):
        """停止后台监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("🔍 操作监控已停止")
    
    def _monitor_loop(self):
        """监控循环"""
        while self.monitoring:
            try:
                # 收集系统指标
                self.collect_system_metrics()
                
                # 检查Chrome实例状态
                self._check_chrome_instances()
                
                # 每30秒执行一次
                time.sleep(30)
                
            except Exception as e:
                print(f"❌ 监控循环异常: {e}")
                time.sleep(10)
    
    def _check_chrome_instances(self):
        """检查Chrome实例状态"""
        try:
            # 获取所有Chrome进程
            chrome_pids = set()
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'chrome.exe' in proc.info['name'].lower():
                        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ""
                        if 'remote-debugging-port' in cmdline:
                            chrome_pids.add(proc.info['pid'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # 更新状态
            current_time = datetime.now()
            with self.lock:
                for chrome_num in list(self.chrome_status.keys()):
                    last_updated = datetime.fromisoformat(self.chrome_status[chrome_num]["last_updated"])
                    if current_time - last_updated > timedelta(minutes=5):
                        # 超过5分钟没有更新，可能已停止
                        if self.chrome_status[chrome_num]["status"] == "running":
                            self.chrome_status[chrome_num]["status"] = "unknown"
                            self.chrome_status[chrome_num]["last_updated"] = current_time.isoformat()
                            
        except Exception as e:
            print(f"❌ 检查Chrome实例状态失败: {e}")
    
    def get_status_report(self):
        """获取状态报告"""
        with self.lock:
            recent_metrics = list(self.system_metrics)[-1] if self.system_metrics else None
            
            report = {
                "timestamp": datetime.now().isoformat(),
                "statistics": dict(self.stats),
                "chrome_status": dict(self.chrome_status),
                "system_metrics": recent_metrics,
                "recent_operations": list(self.operation_logs)[-10:]  # 最近10个操作
            }
            
            # 转换set为list以便JSON序列化
            report["statistics"]["chrome_instances"] = list(report["statistics"]["chrome_instances"])
            
            return report
    
    def get_performance_summary(self, hours=1):
        """获取性能摘要"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with self.lock:
            # 过滤指定时间内的日志
            recent_logs = [
                log for log in self.operation_logs
                if datetime.fromisoformat(log["timestamp"]) > cutoff_time
            ]
            
            # 统计
            total_ops = len(recent_logs)
            successful_ops = len([log for log in recent_logs if log["level"] == "INFO"])
            failed_ops = len([log for log in recent_logs if log["level"] == "ERROR"])
            
            # 按Chrome实例分组
            chrome_stats = defaultdict(lambda: {"total": 0, "success": 0, "failed": 0})
            for log in recent_logs:
                chrome_num = log["chrome_num"]
                chrome_stats[chrome_num]["total"] += 1
                if log["level"] == "INFO":
                    chrome_stats[chrome_num]["success"] += 1
                elif log["level"] == "ERROR":
                    chrome_stats[chrome_num]["failed"] += 1
            
            return {
                "time_period_hours": hours,
                "total_operations": total_ops,
                "successful_operations": successful_ops,
                "failed_operations": failed_ops,
                "success_rate": successful_ops / total_ops if total_ops > 0 else 0,
                "chrome_instance_stats": dict(chrome_stats),
                "active_chrome_instances": len(chrome_stats)
            }
    
    def export_logs(self, filename=None, hours=24):
        """导出日志"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"operation_logs_export_{timestamp}.json"
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with self.lock:
            # 过滤指定时间内的日志
            export_logs = [
                log for log in self.operation_logs
                if datetime.fromisoformat(log["timestamp"]) > cutoff_time
            ]
            
            export_data = {
                "export_info": {
                    "generated_at": datetime.now().isoformat(),
                    "time_period_hours": hours,
                    "total_logs": len(export_logs)
                },
                "statistics": self.get_performance_summary(hours),
                "logs": export_logs
            }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            print(f"📝 日志已导出: {filename}")
            return True
        except Exception as e:
            print(f"❌ 导出日志失败: {e}")
            return False
    
    def cleanup_old_logs(self, days=7):
        """清理旧日志文件"""
        cutoff_date = datetime.now() - timedelta(days=days)
        cleaned_count = 0
        
        try:
            for log_file in self.log_directory.glob("operations_*.log"):
                # 从文件名提取日期
                date_str = log_file.stem.split('_')[1]
                file_date = datetime.strptime(date_str, "%Y%m%d")
                
                if file_date < cutoff_date:
                    log_file.unlink()
                    cleaned_count += 1
            
            print(f"🧹 已清理 {cleaned_count} 个旧日志文件")
            return cleaned_count
            
        except Exception as e:
            print(f"❌ 清理日志文件失败: {e}")
            return 0

# 全局监控实例
_global_monitor = None

def get_monitor():
    """获取全局监控实例"""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = OperationMonitor()
    return _global_monitor

def log_operation(chrome_num, operation_type, message, level="INFO", details=None):
    """便捷的日志记录函数"""
    monitor = get_monitor()
    monitor.log_operation(chrome_num, operation_type, message, level, details)

def update_chrome_status(chrome_num, status, details=None):
    """便捷的状态更新函数"""
    monitor = get_monitor()
    monitor.update_chrome_status(chrome_num, status, details)

if __name__ == "__main__":
    # 测试监控功能
    monitor = OperationMonitor()
    
    # 模拟一些操作
    monitor.log_operation(11, "connect", "连接到Chrome实例")
    monitor.log_operation(11, "navigate", "导航到Google")
    monitor.update_chrome_status(11, "running", {"url": "https://www.google.com"})
    
    time.sleep(2)
    
    # 获取状态报告
    report = monitor.get_status_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    
    # 导出日志
    monitor.export_logs()
    
    monitor.stop_monitoring()

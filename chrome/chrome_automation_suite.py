#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chrome自动化套件 - 统一入口
整合所有Chrome自动化功能的统一管理界面
"""

import sys
import time
import json
import argparse
from pathlib import Path

# 导入各个模块
from batch_chrome_launcher import ChromeBatchLauncher
from close_specific_chrome import SpecificChromeCloser
from web_automation_enhanced import EnhancedWebAutomation
from task_queue_manager import TaskQueueManager
from operation_monitor import OperationMonitor, get_monitor

class ChromeAutomationSuite:
    def __init__(self):
        """初始化Chrome自动化套件"""
        self.monitor = get_monitor()
        self.launcher = ChromeBatchLauncher()
        self.closer = SpecificChromeCloser()
        self.task_manager = TaskQueueManager()
        
        print("🚀 Chrome自动化套件已初始化")
    
    def show_status(self):
        """显示系统状态"""
        print("\n" + "="*50)
        print("📊 Chrome自动化套件状态")
        print("="*50)
        
        # 获取监控报告
        report = self.monitor.get_status_report()
        
        print(f"📈 操作统计:")
        stats = report["statistics"]
        print(f"   总操作数: {stats['total_operations']}")
        print(f"   成功操作: {stats['successful_operations']}")
        print(f"   失败操作: {stats['failed_operations']}")
        print(f"   活跃实例: {len(stats['chrome_instances'])}")
        
        print(f"\n🖥️  Chrome实例状态:")
        if report["chrome_status"]:
            for chrome_num, status_info in report["chrome_status"].items():
                status = status_info["status"]
                emoji = "🟢" if status == "running" else "🔴" if status == "error" else "🟡"
                print(f"   Chrome_{chrome_num}: {emoji} {status}")
        else:
            print("   无活跃实例")
        
        # 系统资源
        if report["system_metrics"]:
            metrics = report["system_metrics"]
            print(f"\n💻 系统资源:")
            print(f"   CPU使用率: {metrics['system']['cpu_percent']:.1f}%")
            print(f"   内存使用率: {metrics['system']['memory_percent']:.1f}%")
            print(f"   Chrome进程数: {metrics['chrome_processes']['count']}")
            print(f"   Chrome总内存: {metrics['chrome_processes']['total_memory_mb']:.1f}MB")
    
    def launch_chrome_instances(self, start_num, end_num, websites=None):
        """启动Chrome实例"""
        print(f"\n🚀 启动Chrome实例 {start_num}-{end_num}")
        
        if websites:
            # 更新网站配置
            config_file = Path("websites_config.txt")
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write("# 网页配置文件\n")
                for site in websites:
                    f.write(f"{site}\n")
        
        success = self.launcher.launch_batch(start_num, end_num)
        
        if success:
            # 更新状态
            for num in range(start_num, end_num + 1):
                self.monitor.update_chrome_status(num, "running")
            print(f"✅ 成功启动Chrome实例 {start_num}-{end_num}")
        else:
            print(f"❌ 启动Chrome实例失败")
        
        return success
    
    def close_chrome_instances(self, chrome_numbers):
        """关闭Chrome实例"""
        print(f"\n🔴 关闭Chrome实例: {chrome_numbers}")
        
        success = self.closer.close_by_numbers(chrome_numbers)
        
        if success:
            # 更新状态
            for num in chrome_numbers:
                self.monitor.update_chrome_status(num, "stopped")
            print(f"✅ 成功关闭Chrome实例: {chrome_numbers}")
        else:
            print(f"❌ 关闭Chrome实例失败")
        
        return success
    
    def run_automation_task(self, chrome_num, actions):
        """运行单个自动化任务"""
        print(f"\n🤖 在Chrome_{chrome_num}上执行自动化任务")
        
        try:
            with EnhancedWebAutomation(chrome_num) as automation:
                if not automation.connect_to_chrome():
                    print(f"❌ 无法连接到Chrome_{chrome_num}")
                    return False
                
                self.monitor.update_chrome_status(chrome_num, "busy", {"task": "automation"})
                
                results = automation.execute_action_sequence(actions)
                
                # 计算成功率
                total_actions = len(results)
                successful_actions = sum(1 for r in results if r["success"])
                success_rate = successful_actions / total_actions if total_actions > 0 else 0
                
                print(f"✅ 任务完成，成功率: {success_rate:.1%}")
                
                self.monitor.update_chrome_status(chrome_num, "running", {
                    "last_task_success_rate": success_rate,
                    "last_task_time": time.time()
                })
                
                return success_rate > 0.8
                
        except Exception as e:
            print(f"❌ 自动化任务执行失败: {e}")
            self.monitor.update_chrome_status(chrome_num, "error", {"error": str(e)})
            return False
    
    def run_batch_tasks(self, tasks_config_file):
        """运行批量任务"""
        print(f"\n📋 执行批量任务: {tasks_config_file}")
        
        if not Path(tasks_config_file).exists():
            print(f"❌ 任务配置文件不存在: {tasks_config_file}")
            return False
        
        try:
            self.task_manager.add_batch_tasks(tasks_config_file)
            self.task_manager.run_tasks()
            
            # 保存结果
            self.task_manager.save_results()
            
            print("✅ 批量任务执行完成")
            return True
            
        except Exception as e:
            print(f"❌ 批量任务执行失败: {e}")
            return False
    
    def interactive_mode(self):
        """交互模式"""
        print("\n🎮 进入交互模式")
        print("输入 'help' 查看可用命令，输入 'quit' 退出")
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    break
                elif command == 'help':
                    self.show_help()
                elif command == 'status':
                    self.show_status()
                elif command.startswith('launch'):
                    self.handle_launch_command(command)
                elif command.startswith('close'):
                    self.handle_close_command(command)
                elif command.startswith('task'):
                    self.handle_task_command(command)
                elif command == 'export':
                    self.monitor.export_logs()
                elif command == 'cleanup':
                    self.monitor.cleanup_old_logs()
                else:
                    print("❌ 未知命令，输入 'help' 查看帮助")
                    
            except KeyboardInterrupt:
                print("\n👋 退出交互模式")
                break
            except Exception as e:
                print(f"❌ 命令执行错误: {e}")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
🎮 可用命令:
  status          - 显示系统状态
  launch 11 15    - 启动Chrome_11到Chrome_15
  close 11 12 13  - 关闭指定Chrome实例
  task sample     - 运行示例任务
  export          - 导出操作日志
  cleanup         - 清理旧日志文件
  help            - 显示此帮助
  quit/exit       - 退出程序
        """
        print(help_text)
    
    def handle_launch_command(self, command):
        """处理启动命令"""
        parts = command.split()
        if len(parts) >= 3:
            try:
                start_num = int(parts[1])
                end_num = int(parts[2])
                self.launch_chrome_instances(start_num, end_num)
            except ValueError:
                print("❌ 无效的数字参数")
        else:
            print("❌ 用法: launch <start_num> <end_num>")
    
    def handle_close_command(self, command):
        """处理关闭命令"""
        parts = command.split()
        if len(parts) >= 2:
            try:
                chrome_numbers = [int(x) for x in parts[1:]]
                self.close_chrome_instances(chrome_numbers)
            except ValueError:
                print("❌ 无效的数字参数")
        else:
            print("❌ 用法: close <chrome_num1> [chrome_num2] ...")
    
    def handle_task_command(self, command):
        """处理任务命令"""
        parts = command.split()
        if len(parts) >= 2:
            task_type = parts[1]
            if task_type == 'sample':
                # 创建并运行示例任务
                from task_queue_manager import create_sample_tasks
                create_sample_tasks()
                self.run_batch_tasks("sample_tasks.json")
            else:
                print("❌ 未知任务类型")
        else:
            print("❌ 用法: task <type>")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Chrome自动化套件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python chrome_automation_suite.py --status                    # 显示状态
  python chrome_automation_suite.py --launch 11 15             # 启动Chrome_11-15
  python chrome_automation_suite.py --close 11 12 13           # 关闭指定实例
  python chrome_automation_suite.py --batch sample_tasks.json  # 运行批量任务
  python chrome_automation_suite.py --interactive              # 交互模式
        """
    )
    
    parser.add_argument('--status', action='store_true', help='显示系统状态')
    parser.add_argument('--launch', nargs=2, type=int, metavar=('START', 'END'), help='启动Chrome实例范围')
    parser.add_argument('--close', nargs='+', type=int, metavar='NUM', help='关闭指定Chrome实例')
    parser.add_argument('--batch', metavar='CONFIG_FILE', help='运行批量任务')
    parser.add_argument('--interactive', action='store_true', help='进入交互模式')
    
    args = parser.parse_args()
    
    # 创建套件实例
    suite = ChromeAutomationSuite()
    
    if args.status:
        suite.show_status()
    elif args.launch:
        suite.launch_chrome_instances(args.launch[0], args.launch[1])
    elif args.close:
        suite.close_chrome_instances(args.close)
    elif args.batch:
        suite.run_batch_tasks(args.batch)
    elif args.interactive:
        suite.interactive_mode()
    else:
        # 默认显示状态并进入交互模式
        suite.show_status()
        suite.interactive_mode()

if __name__ == "__main__":
    main()

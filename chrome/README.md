# Chrome自动化批量管理系统

## 项目概述

这是一个Chrome浏览器自动化批量管理系统，支持：
- 批量生成Chrome快捷方式（每个使用独立用户数据目录和调试端口）
- 自动化启动多个Chrome实例
- 批量打开指定网页
- 自动化Google账号登录
- 后续支持网页自动化操作（输入、点击等）

## 核心功能

### 1. Chrome快捷方式批量生成，已完成，该功能保存不变
- **文件**: `chrome_shortcut_generator.py`, `genchrome.bat`
- **功能**: 批量生成Chrome快捷方式，每个使用独立的用户数据目录和调试端口
- **配置规则**:
  - 快捷方式命名: `Chrome_{序号}.lnk`
  - 用户数据目录: `c:\tools\chromes\{序号}\`
  - 调试端口: `10000 + 序号`

### 2. 批量启动与网页打开
- **文件**: `batch_chrome_launcher.py`, `launch_chrome.bat`
- **功能**: 
  - 同时启动数个到20个Chrome实例
  - 每个实例自动打开配置文件中指定的网页
  - 支持网页配置文件 `websites_config.txt`

### 3. Google账号自动登录
- **文件**: `restart_and_login_chrome_19_20.py`
- **功能**:
  - 自动关闭已存在的Chrome实例
  - 重新启动指定Chrome实例
  - 自动执行Google账号登录流程
  - 支持多账号配置

### 4. 网页配置管理
- **配置文件**: 
  - `websites_config.txt` - 通用网页列表
  - `C:\tools\chromes\allwebsite.txt` - 账号信息和网页配置

## 使用方法

### 🚀 一键启动 (推荐)
```bash
# Windows用户 - 双击运行
start_automation.bat

# 或命令行运行
python chrome_automation_suite.py --interactive
```

### 📋 基础操作

#### 1. 生成Chrome快捷方式
```bash
# 生成Chrome_11到Chrome_20的快捷方式
python chrome_shortcut_generator.py 11 20

# 或使用批处理文件
genchrome.bat 11 20
```

#### 2. 启动Chrome实例
```bash
# 启动Chrome_11到Chrome_15
python chrome_automation_suite.py --launch 11 15

# 或使用批量启动器
python batch_chrome_launcher.py 11 15
```

#### 3. 关闭Chrome实例
```bash
# 关闭指定实例
python chrome_automation_suite.py --close 11 12 13

# 或使用专用关闭工具
python close_specific_chrome.py --numbers 19 20
```

#### 4. 运行自动化任务
```bash
# 运行批量任务
python chrome_automation_suite.py --batch sample_tasks.json

# 查看系统状态
python chrome_automation_suite.py --status
```

### 🔧 传统方式 (兼容性)

#### 测试启动3个Chrome实例
```bash
python test_3_chrome_with_websites.py
```

#### 启动Chrome_19和Chrome_20并自动登录Google
```bash
python restart_and_login_chrome_19_20.py
```

### 高级使用

#### 批量启动多个Chrome实例
```bash
# 启动Chrome_11到Chrome_20
python batch_chrome_launcher.py 11 20

# 使用批处理文件
launch_chrome.bat
```

## 配置文件说明

### 1. 网页配置 (`websites_config.txt`)
```
# 网页配置文件 - 每行一个网址
https://www.google.com
https://www.baidu.com
https://github.com
```

### 2. 账号配置 (`C:\tools\chromes\allwebsite.txt`)
```
mails:     ---           password,    ---     验证邮箱
19. Alcinaedcvf@gmail.com----w.....----ey....----巴西//19
20. Fdbcvdfxc453@gmail.com----m.....----qy....----巴西//20

#website for open in every chromes,
https://www.gmail.com
https://wipdf.vercel.app/
```

## 技术架构

### 核心技术栈
- **Python 3.6+**
- **Selenium WebDriver** - 网页自动化
- **psutil** - 进程管理
- **pywin32** - Windows快捷方式创建

### Chrome实例隔离
- 每个Chrome实例使用独立的用户数据目录
- 独立的调试端口（10011, 10012, 10013...）
- 完全隔离的Cookie、会话和设置

### 自动化流程
1. **进程管理**: 智能检测和关闭指定Chrome实例
2. **实例启动**: 通过快捷方式启动Chrome实例
3. **Selenium连接**: 通过调试端口连接到Chrome实例
4. **自动化操作**: 执行登录、导航、输入等操作

## 文件结构

```
chrome/
├── chrome_shortcut_generator.py    # Chrome快捷方式生成器
├── genchrome.bat                   # 快捷方式生成批处理
├── batch_chrome_launcher.py        # 批量启动器
├── launch_chrome.bat              # 批量启动批处理
├── restart_and_login_chrome_19_20.py  # 重启并登录Chrome_19/20
├── test_3_chrome_with_websites.py # 测试启动3个Chrome实例
├── websites_config.txt            # 网页配置文件
├── Chrome_11.lnk                  # 生成的Chrome快捷方式
├── Chrome_12.lnk
├── ...
└── README.md                      # 本文档
```

## 开发计划

### 第一阶段 ✅ 已完成
- [x] Chrome快捷方式批量生成
- [x] 批量启动Chrome实例
- [x] 自动打开指定网页
- [x] Google账号自动登录

### 第二阶段 🚧 开发中 (基于实际验证更新)

#### ✅ 已完成MVP
- [x] **关闭特定Chrome实例** - `restart_and_login_chrome_19_20.py`
- [x] **Google自动化登录基础** - `launch_and_login_chrome_19_20.py`
- [x] **网页自动化操作基础** - Selenium集成完成
- [x] **弹窗处理基础** - 二次验证处理逻辑

#### 🚧 完善中
- [ ] **网页自动化操作增强** (输入、点击、等待)
- [ ] **智能弹窗处理器** (通用弹窗识别和处理)
- [ ] **批量操作任务队列** (多实例协调)
- [ ] **操作结果监控和日志** (详细日志和错误处理)

#### 📋 待优化
- [ ] **错误恢复机制** (自动重试和故障转移)
- [ ] **性能优化** (并发处理和资源管理)
- [ ] **配置管理增强** (动态配置和热更新)

### 第三阶段 📋 计划中
- [ ] 图形化界面
- [ ] 配置文件可视化编辑
- [ ] 定时任务调度
- [ ] 操作录制和回放

## 第二阶段核心文件

### ✅ 已完成文件
- `close_specific_chrome.py` - 精准关闭特定Chrome实例
- `web_automation.py` - 基础网页自动化操作
- `web_automation_enhanced.py` - 增强版网页自动化
- `chrome_popup_handler.py` - Chrome弹窗自动处理
- `task_queue_manager.py` - 任务队列管理器
- `operation_monitor.py` - 操作监控和日志
- `chrome_automation_suite.py` - 统一管理界面
- `automation_config.json` - 系统配置文件

### 🔧 辅助文件
- `launch_and_login_chrome_19_20.py` - Google登录示例
- `launch_chrome_19_20_fixed.py` - 修正版启动脚本
- `batch_chrome_launcher.py` - 批量启动器

## 故障排除

### 常见问题

1. **找不到Chrome**
   ```bash
   python chrome_shortcut_generator.py 11 10 -c "你的Chrome路径"
   ```

2. **Selenium连接失败**
   - 确保Chrome实例已启动
   - 检查调试端口是否正确
   - 确认防火墙设置

3. **登录失败**
   - 检查账号密码配置
   - 确认网络连接
   - 查看Google安全设置

### 依赖安装
```bash
pip install selenium psutil pywin32
```

## 使用注意事项

1. **端口规划**: 调试端口从10000+序号开始，避免端口冲突
2. **数据隔离**: 每个Chrome实例使用独立的用户数据目录
3. **安全考虑**: 账号密码信息请妥善保管
4. **资源管理**: 大量Chrome实例会消耗较多系统资源

## 联系方式

如有问题或建议，请联系开发者或查看项目文档。

---

## 版本与进度 Version & Milestones

- **当前版本**：v1.1.0
- **更新时间**：2025-01-31 15:30
- **主要进展**：第二阶段MVP基础功能验证完成，完成度75%

### 最新验证结果 (2025-01-31)
- ✅ Chrome实例管理：已完成MVP
- ✅ Google自动化登录：已完成MVP  
- ✅ 网页自动化操作：已完成MVP
- 🚧 弹窗处理逻辑：开发中

### 第二阶段 ✅ 已完成 (95%完成度)

#### ✅ 已完成核心功能
- [x] **关闭特定Chrome实例** - `close_specific_chrome.py`
- [x] **Google自动化登录基础** - `launch_and_login_chrome_19_20.py`
- [x] **网页自动化操作基础** - `web_automation.py`
- [x] **智能弹窗处理器** - `chrome_popup_handler.py`
- [x] **增强版网页自动化** - `web_automation_enhanced.py`
- [x] **批量操作任务队列** - `task_queue_manager.py`
- [x] **操作结果监控和日志** - `operation_monitor.py`
- [x] **统一管理界面** - `chrome_automation_suite.py`

#### ✅ 已完成增强功能
- [x] **错误恢复机制** (自动重试和故障转移)
- [x] **性能优化** (并发处理和资源管理)
- [x] **配置管理增强** (JSON配置文件和模板)
- [x] **实时监控** (系统资源和Chrome实例状态)
- [x] **日志管理** (自动清理和导出功能)

#### 🔧 微调优化
- [ ] **用户界面优化** (交互体验改进)
- [ ] **文档完善** (使用示例和故障排除)
- [ ] **性能调优** (大规模部署优化)

## 第二阶段功能详解

### 🤖 增强版网页自动化 (`web_automation_enhanced.py`)
- **智能元素查找**: 支持多种选择器策略 (XPath, CSS, ID, Class)
- **多重点击方式**: 普通点击、JavaScript点击、ActionChains点击
- **错误重试机制**: 自动重试失败的操作
- **操作日志记录**: 详细记录每个操作的执行情况
- **动作序列执行**: 支持复杂的自动化流程

### 📋 任务队列管理 (`task_queue_manager.py`)
- **并发任务执行**: 支持多线程并发处理任务
- **任务优先级**: 支持任务优先级排序
- **自动重试**: 失败任务自动重试机制
- **批量任务配置**: JSON格式的任务配置文件
- **执行结果统计**: 详细的任务执行报告

### 📊 操作监控系统 (`operation_monitor.py`)
- **实时监控**: 实时监控Chrome实例状态和系统资源
- **操作日志**: 自动记录所有操作和错误信息
- **性能统计**: 成功率、响应时间等性能指标
- **日志管理**: 自动清理旧日志，支持日志导出
- **系统指标**: CPU、内存使用率监控

### 🎮 统一管理界面 (`chrome_automation_suite.py`)
- **命令行界面**: 支持命令行参数和交互模式
- **状态监控**: 实时显示系统状态和Chrome实例状态
- **批量操作**: 统一管理Chrome实例的启动、关闭
- **任务执行**: 集成任务队列管理和监控功能
- **配置管理**: 统一的配置文件管理

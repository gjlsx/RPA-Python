# Chrome快捷方式批量生成器

## 📋 功能说明

这个工具可以自动批量生成Chrome快捷方式，每个快捷方式使用独立的用户数据目录和调试端口，适用于需要多个Chrome实例的场景。

**📁 程序位置**: 请将此程序放在 `chrome` 目录下使用

## 🚀 快速开始

### 方法1: 使用批处理文件（推荐）
1. 进入 `chrome` 目录
2. 双击运行 `genchrome.bat`
3. 按提示输入起始序号和生成数量
4. 程序会在当前目录生成快捷方式

### 方法2: 使用命令行
```bash
# 进入chrome目录
cd chrome

# 生成序号11-20的10个快捷方式
python chrome_shortcut_generator.py 11 10

# 生成序号1-5的快捷方式到指定目录
python chrome_shortcut_generator.py 1 5 -o shortcuts

# 指定Chrome路径
python chrome_shortcut_generator.py 21 3 -c "D:\Chrome\chrome.exe"
```

## 📁 生成的快捷方式规则

### 文件命名
- 快捷方式文件名: `Chrome_{序号}.lnk`
- 例如: `Chrome_11.lnk`, `Chrome_12.lnk`, ...

### 目标配置
- **程序路径**: `C:\Program Files\Google\Chrome\Application\chrome.exe`
- **用户数据目录**: `c:\tools\chromes\{序号}\`
- **调试端口**: `10000 + 序号`
- **工作目录**: `C:\Program Files\Google\Chrome\Application`

### 示例配置
```
序号11的快捷方式:
- 文件名: Chrome_11.lnk
- 目标: "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir=c:\tools\chromes\11\ --remote-debugging-port=10011
- 起始位置: "C:\Program Files\Google\Chrome\Application"
```

## ⚙️ 命令行参数

```
python chrome_shortcut_generator.py <起始序号> <生成数量> [选项]

必需参数:
  起始序号          起始的序号
  生成数量          要生成的快捷方式数量

可选参数:
  -h, --help       显示帮助信息
  -o, --output     输出目录 (默认: 当前目录)
  -c, --chrome     Chrome可执行文件路径 (默认: 自动检测)
  -d, --data-dir   用户数据基础目录 (默认: c:\tools\chromes)
```

## 📝 使用示例

### 示例1: 基本使用
```bash
python chrome_shortcut_generator.py 11 10
```
生成Chrome_11.lnk到Chrome_20.lnk，共10个快捷方式

### 示例2: 指定输出目录
```bash
python chrome_shortcut_generator.py 1 5 -o "D:\Chrome快捷方式"
```
在D:\Chrome快捷方式目录下生成Chrome_1.lnk到Chrome_5.lnk

### 示例3: 自定义Chrome路径和数据目录
```bash
python chrome_shortcut_generator.py 21 3 -c "D:\Chrome\chrome.exe" -d "D:\ChromeData"
```
使用自定义的Chrome路径和数据目录

## 🔧 系统要求

- **操作系统**: Windows 10/11
- **Python**: 3.6+
- **依赖包**: pywin32 (程序会自动安装)
-   --手动安装：pip install pywin32 

## 📂 目录结构

生成后的目录结构示例:
```
项目根目录/
└── chrome/                          (程序目录)
    ├── chrome_shortcut_generator.py (主程序)
    ├── genchrome.bat (批处理文件)
    ├── Chrome快捷方式生成器使用说明.md
    ├── Chrome10.lnk                 (原有快捷方式)
    ├── Chrome_11.lnk                (新生成的快捷方式)
    ├── Chrome_12.lnk
    ├── ...
    └── Chrome_20.lnk

c:\tools\chromes\                    (用户数据目录)
├── 11\          (Chrome用户数据目录)
├── 12\
├── ...
└── 20\
```

## 🛠️ 故障排除

### 问题1: 找不到Chrome
**解决方案**: 使用 `-c` 参数指定Chrome路径
```bash
python chrome_shortcut_generator.py 11 10 -c "你的Chrome路径"
```

### 问题2: 权限不足
**解决方案**: 以管理员身份运行命令提示符

### 问题3: pywin32安装失败
**解决方案**: 手动安装
```bash
pip install pywin32
```

## 💡 使用技巧

1. **批量测试**: 先生成少量快捷方式测试，确认配置正确后再批量生成
2. **端口规划**: 调试端口从10000+序号开始，避免端口冲突
3. **数据隔离**: 每个Chrome实例使用独立的用户数据目录，互不干扰
4. **备份重要数据**: 生成前备份重要的Chrome用户数据

## 📞 支持

如有问题或建议，请联系开发者或查看项目文档。

###
某一个.lnk属性：接下来顺延，10改成11,10010改成10011,etc... 12,10012
快捷方式目标：  "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir=c:\tools\chromes\10\  --remote-debugging-port=10010
快捷方式起始位置： "C:\Program Files\Google\Chrome\Application"
运行方式： 常规窗口
备注： 访问互联网

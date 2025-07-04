import rpa as r

print("RPA 脚本开始...")

# 1. 初始化 RPA 环境
# visual_automation=False 和 chrome_browser=True 是默认值，可以不写
# 这会自动下载并配置所需的组件
if not r.init():
    print("初始化 RPA 环境失败")
    exit()

# 2. 打开 DuckDuckGo 搜索引擎
print("正在打开网页: https://duckduckgo.com")
r.url('https://duckduckgo.com')

# 3. 在搜索框中输入文字并按回车
# '//*[@name="q"]' 是搜索输入框的 XPath 标识符
search_query = 'RPA for Python by tebelorg'
print(f"正在搜索: {search_query}")
r.type('//*[@name="q"]', f'{search_query}[enter]')

# 4. 等待2秒，确保搜索结果已加载
r.wait(2)

# 5. 读取并打印当前页面的标题
page_title = r.title()
print(f"当前页面标题是: {page_title}")

# 6. 对整个页面进行截图，并保存为 png 文件
screenshot_file = 'search_results.png'
if r.snap('page', screenshot_file):
    print(f"已成功截取页面快照并保存为: {screenshot_file}")
else:
    print("截图失败")

# 7. 关闭 RPA 环境
r.close()
print("RPA 脚本结束。")

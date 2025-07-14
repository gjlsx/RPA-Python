# RPA for lovemoney / 量化策略RPA系统

## 项目简介 Project Overview

本项目是一个面向量化策略输入与管理的RPA系统，支持用户输入股票、加密货币代码或区块链地址，选择或自定义量化交易策略，并进行提交。系统采用HTML+CSS+JavaScript实现，支持页面内容中英文切换与批量自动翻译。

This project is an RPA system for quantitative strategy input and management. Users can enter stock/crypto codes or blockchain addresses, select or define quantitative trading strategies, and submit them. The system is implemented with HTML, CSS, and JavaScript, and supports bilingual (Chinese/English) page content and batch auto-translation.

---

## 目录结构 Directory Structure

- `indexcoin.html`：主页面，量化策略输入（已支持中文，bak/下有英文备份）
- `stylecoin.css`：页面样式
- `scriptcoin.js`：页面交互与逻辑
- `strategy_detail.html`：策略详情页
- `strategies/`：内置策略HTML文件
- `blog/`、`u/`、`images/`、`css/`：辅助内容与资源
- `docs/`：核心文档（需求、设计等）
- `bak/`：所有html英文原始文件备份
- `process_html.py`：批量处理与自动翻译脚本

---

## 主要功能 Main Features

- 量化策略输入与管理（支持股票、加密货币、区块链地址）
- 支持选择内置策略或自定义策略
- 页面内容中英文自动切换与批量翻译
- 所有html文件自动备份到bak/目录，确保数据安全
- 自动化脚本支持后续多语言扩展

---

## 文档链接 Documentation

- [需求文档 Requirements](docs/requirements.md)：功能与非功能需求说明
- [设计文档 Design](docs/design.md)：系统架构与模块设计
- [脚本coin子系统说明 Scriptcoin README](docs/scriptcoin_README.md)：子系统说明

---

## 备份与批量处理说明 Backup & Batch Processing

- 所有html文件处理前自动备份到bak/目录，原始英文页面可随时恢复
- `process_html.py`脚本支持批量替换、精简、自动翻译、双语扩展
- 处理日志详见`process_html.log`

---

## 版本与进度 Version & Milestones

- 当前版本：v1.0.0
- 更新时间：2024-07-08
- 主要进展：实现页面批量汉化、备份、自动化脚本、文档完善

---

## 后续任务 Next Tasks

- [ ] 完善中英文双语切换与页面样式
- [ ] 扩充自动翻译词典，提升翻译质量
- [ ] 增加自动化测试与回归测试
- [ ] 定期清理bak/和temp/目录过期文件
- [ ] 持续完善文档与用户体验

---

如需英文原始页面，请至bak/目录查找。For original English pages, please check the bak/ directory.

后续将使用v0.dev进行前端页面开发，尽量使用gemini cli,claude code等自动化开发，人工审核计划方向，大流程，结果，
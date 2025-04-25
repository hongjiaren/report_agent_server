# Report Agent Server

[[License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[[Build Status](https://travis-ci.org/hongjiaren/report_agent_server.svg?branch=master)](https://travis-ci.org/hongjiaren/report_agent_server)
[[Release](https://img.shields.io/github/v/release/hongjiaren/report_agent_server)]
**Report Agent Server** 是一个智能化的报告生成服务解决方案，旨在通过深度研究和自动化处理为用户提供高质量的分析报告。系统能够根据用户提出的问题，利用大语言模型和深度检索技术，从网页中提取相关信息并生成结构化的报告内容，最终输出为 HTML 和 PDF 格式。

---

## 功能特性

- **智能信息检索**：基于用户提问，使用深度检索（Deep Research）技术从互联网上获取相关资源，并利用大语言模型对内容进行深度分析和整理。
- **多模态报告生成**：
  - 自动生成包含文字、表格、图片等内容的结构化报告。
  - 支持复杂的排版需求，确保报告的专业性和易读性。
- **HTML转PDF**：通过强大的渲染引擎，将生成的 HTML 报告高质量地转换为 PDF 文件。
- **PDF合并**：支持将多个独立的报告 PDF 文件合并为一个完整的报告文档。
- **高度可定制**：允许用户自定义报告模板、样式以及导出设置，满足不同业务场景的需求。
- **易于集成**：提供API接口，便于与现有系统快速集成。

---

## 工作流程

- **问题解析**：
  - 用户提交问题或需求，系统解析问题内容并确定需要检索的主题和范围。
- **深度信息检索**：
  - 使用深度检索技术，从互联网中抓取与问题相关的网页内容。
  - 利用大语言模型对网页内容进行分析和筛选，提取关键信息。
- **报告内容生成**：
  - 将提取的信息整理为文字、表格、图片等形式，形成初步的报告内容。
  - 对各类内容进行二次分析和优化，确保逻辑清晰、数据准确。
- **HTML报告生成**：
  - 使用大语言模型生成结构化的 HTML 报告代码，确保报告在浏览器中的展示效果美观且专业。
- **PDF转换与合并**：
  - 使用 ChromeDriver 将 HTML 文件转换为 PDF 格式。
  - 如果有多部分报告，系统会自动将所有 PDF 文件合并为一个完整的报告文档。

---

## 快速开始

### 环境准备

确保你已经安装了以下依赖项：
- **Node.js**：建议使用最新稳定版本。
- **ChromeDriver**：用于 HTML 到 PDF 的转换。
- **Python**（可选）：如果需要运行额外的脚本或工具。

### 安装与启动

1. 克隆仓库到本地：
   ```bash
   git clone https://github.com/hongjiaren/report_agent_server.git
   cd report_agent_server

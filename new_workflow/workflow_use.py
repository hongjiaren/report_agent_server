import json
import config 
import requests
from util import XinferRequest, XinferRequest_Stream, process_html_string, handle_json
from weasyprint import HTML
import os
from PyPDF2 import PdfMerger
import re
from datetime import datetime


# 第一步：根据问题生成 plan
def plan_llm_xinfer(query):
    plan_prompt = config.PLAN_PROMPT
    prompt = """
    # 用户问题: 
    %s
    # 提示词：
    %s
    """
    prompt = prompt % (query,  plan_prompt)
    res = XinferRequest.parse_response(XinferRequest.request_xinfer(config.QWEN25_URL, config.QWEN25_MODEL, prompt))
    return res


# Web Search 函数（单个步骤）
def single_step_web_search(step_data):
    web_search_data = []  # 存储当前步骤的搜索结果

    # Web Search 服务的 URL
    search_url = "http://60.165.238.132:8889/stream_chat/"

    # 构造查询内容
    query = f"{step_data['title']} {step_data['details']}"

    # 构造请求体
    payload = {
        "query": query
    }

    try:
        # 发送 POST 请求到 Web Search 服务
        with requests.post(search_url, json=payload, stream=True) as response:
            # 检查响应状态码
            if response.status_code == 200:
                print(f"步骤 {step_data['step']} 搜索开始，查询内容: {query}")

                # 初始化存储流式响应的变量
                search_result_chunks = []

                # 处理流式响应
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        print(f"流式响应: {line}")  # 打印流式返回的内容
                        search_result_chunks.append(line)

                # 将所有流式响应合并为最终结果
                search_result = "\n".join(search_result_chunks)
                web_search_data.append({
                    "step": step_data["step"],
                    "query": query,
                    "search_result": search_result
                })
            else:
                print(f"步骤 {step_data['step']} 搜索失败，状态码: {response.status_code}")
                web_search_data.append({
                    "step": step_data["step"],
                    "query": query,
                    "search_result": None
                })

    except Exception as e:
        print(f"步骤 {step_data['step']} 搜索出错: {e}")
        web_search_data.append({
            "step": step_data["step"],
            "query": query,
            "search_result": None
        })

    return web_search_data


# 第三步：把超长的 web search data 进行截断
def truncate_web_search_data(web_search_data):
    truncated_data = []
    
    # 定义正则表达式来匹配从一个【搜索关键词】到下一个【搜索关键词】之前的所有内容
    search_keyword_pattern = re.compile(r'【搜索关键词】(.*?)(?=【搜索关键词】|$)', re.DOTALL)
    
    for item in web_search_data:
        query = item['query']
        full_search_result = item['search_result']
        
        # 使用正则表达式查找所有【搜索关键词】及其后的内容
        matches = search_keyword_pattern.findall(full_search_result)
        
        if not matches:  # 如果没有找到任何匹配项，则直接添加原item
            truncated_data.append(item)
        else:
            # 对于每个匹配到的搜索关键词，生成一个新的条目
            for i, match in enumerate(matches):
                # 清洗匹配到的内容，去除开头可能的换行符或空格，并确保以【搜索关键词】开头
                cleaned_match = f"【搜索关键词】{match.strip()}"
                
                # 创建新的搜索结果条目
                new_item = {
                    "step": item["step"],
                    "query": f"{query} - Part {i+1}",
                    "search_result": cleaned_match
                }
                
                # 添加新条目到 truncated_data 列表
                truncated_data.append(new_item)
    
    return truncated_data


# 第四步：把截断后的数据进行分析，生成文字和图表材料
def use_web_data2report_data_table_graph(truncated_data, plan_content):
    report_prompt = config.REPORT_MID_PROMPT
    # 初始化一个空字符串，用于存储所有大模型返回的结果
    all_report_data = ""
    
    # 遍历截断后的数据列表
    for entry in truncated_data:
        # 构造用户问题部分（将当前条目的 query 和 search_result 拼接）
        user_question = f"步骤: {entry['step']}\n查询: {entry['query']}\n搜索结果:\n{entry['search_result']}"
        
        # 构造完整的提示词
        prompt = f"""
        # 用户问题: 
        {user_question}
        # 当前规划的内容:
        {plan_content}
        
        # 任务：
        {report_prompt}
        """
        
        try:
            # 调用流式请求方法
            response_generator = XinferRequest_Stream.parse_response(
                XinferRequest_Stream.request_xinfer(config.QWEN25_URL, config.QWEN25_MODEL, prompt)
            )
            
            # 初始化当前条目的流式结果
            current_result = ""
            
            # 迭代生成器并处理每一部分内容
            for chunk in response_generator:
                print(chunk, end="", flush=True)  # 流式打印每个块
                current_result += chunk  # 将每个块追加到当前条目的结果中
            
            # 将当前条目的完整结果追加到 all_results 中
            all_report_data += f"步骤 {entry['step']} - Part {entry['query'].split(' - Part ')[-1]} 的分析结果:\n{current_result}\n\n"
        
        except Exception as e:
            # 如果调用失败，记录错误信息
            all_report_data += f"步骤 {entry['step']} - Part {entry['query'].split(' - Part ')[-1]} 的分析失败: {e}\n\n"
    
    return all_report_data


# 第五步：把材料进行分析，生成最终的报告
def report_data2report_result(step, plan_title, plan_details, all_report_data):
    # 从配置文件中加载 REPORT_RESULT_PROMPT
    report_prompt = config.REPORT_RESULT_PROMPT
    
    # 初始化一个空字符串，用于存储大模型返回的结果
    all_report_result = ""
    
    # 动态插入当前步骤编号到 report_prompt 中
    formatted_report_prompt = report_prompt.format(step)
    
    # 构造完整的提示词
    prompt = f"""
    # 报告材料: 
    {all_report_data}
    # 当前是报告的第{step}步。
    # 当前步骤的标题:
    {plan_title}
    # 当前步骤的要求：
    {plan_details}
    # 任务：
    {formatted_report_prompt}
    """
    
    try:
        # 调用流式请求方法
        response_generator = XinferRequest_Stream.parse_response(
            XinferRequest_Stream.request_xinfer(config.QWEN25_URL, config.QWEN25_MODEL, prompt)
        )
        
        # 初始化当前条目的流式结果
        current_result = ""
        
        # 迭代生成器并处理每一部分内容
        for chunk in response_generator:
            print(chunk, end="", flush=True)  # 流式打印每个块
            current_result += chunk  # 将每个块追加到当前条目的结果中
        
        # 将大模型返回的完整结果存储到 all_report_data 中
        all_report_result += f"报告最终结果:\n{current_result}\n\n"
    
    except Exception as e:
        # 如果调用失败，记录错误信息
        all_report_result += f"分析失败: {e}\n\n"
    
    return all_report_result


# 第六步：把报告结果进行分析，生成最终的 HTML
def get_report_html_from_report_result(all_report_data, step):
    generate_prompt = config.CONTENT_GENERATE_PROMPT
    
    formatted_report_prompt = generate_prompt.replace("{}", str(step), 1)
    # 构造提示词

    prompt = f"""
    # 报告材料: 
    {all_report_data}
    # 当前是报告的第{step}步。
    # 当前步骤的标题:
    # 任务：
    {formatted_report_prompt}
    """

    # 调用大模型生成 HTML 报告
    try:
        print("开始流式生成 HTML 报告:")
        report_html = ""  # 初始化为空字符串

        # 调用流式请求方法
        response_generator = XinferRequest_Stream.parse_response(
            XinferRequest_Stream.request_xinfer(config.QWEN25_URL, config.QWEN25_MODEL, prompt)
        )

        # 迭代生成器并打印每一部分内容
        for chunk in response_generator:
            print(chunk, end="", flush=True)  # 流式打印每个块
            report_html += chunk  # 将每个块追加到 report_html 中

        print("----------可爱的分隔符--------------")
        # print("\n大模型生成的完整 HTML 报告:")
        
        # print(report_html)  # 打印完整的 HTML 报告

        return report_html  # 返回完整的 HTML 报告
    except Exception as e:
        print(f"HTML 报告生成失败: {e}")
        return ""  # 如果发生错误，返回空字符串


# 第七步：把 HTML 转成 PDF


import os
import base64
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


def html2pdf(query, type, html_content, flask_base_url="http://60.165.238.132:9000"):
    """
    将 HTML 内容通过 Flask 服务加载并转换为 PDF 文件。
    
    :param query: 查询标识符 (字符串)
    :param type: 当前步骤名称 (字符串)
    :param html_content: HTML 内容 (字符串)
    :param flask_base_url: Flask 服务的基础 URL
    :return: 生成的 PDF 文件路径
    """
    # 确保基础输出目录存在
    base_output_folder = "/data/liweier/report_agent_server/image_source/report_pdf_page"
    os.makedirs(base_output_folder, exist_ok=True)

    # 动态生成子文件夹路径，基于 query ，并添加固定的 "report_pdf" 文件夹
    subfolder_path = os.path.join(base_output_folder, query)
    os.makedirs(subfolder_path, exist_ok=True)
    
    pdf_file_path_all = os.path.join("/data/liweier/report_agent_server/pdfs", query)
    # 构造 PDF 文件路径
    pdf_file_path = os.path.join(pdf_file_path_all, f"{type}_report.pdf")

    # 构造 HTML 文件名和路径
    html_filename = f"{type}_report.html"
    html_filepath = os.path.join(subfolder_path, html_filename)

    try:
        # 将 HTML 内容写入文件
        with open(html_filepath, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

        # 构造 Flask 服务的完整 URL，用于访问 HTML 文件
        flask_html_url = urljoin(flask_base_url, f"/report_pdf_page/{query}/{html_filename}")

        # 设置 Chrome 选项，启用无头模式
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')

        # 指定打印为PDF时使用的纸张大小
        chrome_options.add_argument('paper-width=21.6cm')  # A4纸宽
        chrome_options.add_argument('paper-height=27.9cm')  # A4纸高

        # 创建 Chrome 浏览器实例
        service = Service(executable_path='/data/liweier/chromedriver-linux64/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

          # 增加页面加载超时时间
        driver.set_page_load_timeout(300)

        # 打开 Flask 服务提供的 HTML 文件路径
        driver.get(flask_html_url)

        # 等待页面加载完成
        time.sleep(10)  # 根据实际情况调整等待时间

        try:
            # 使用 Chrome DevTools Protocol 打印当前页面为 PDF
            result = driver.execute_cdp_cmd("Page.printToPDF", {
                "printBackground": True,
            })

            # 调试：打印 Chrome DevTools 返回的结果
            # print("Chrome DevTools 返回的结果:", result)

            # 检查返回结果是否包含有效的 PDF 数据
            if not result or "data" not in result:
                raise ValueError("未能从 Chrome DevTools 获取有效的 PDF 数据")

            # 解码 Base64 数据
            try:
                pdf_data = base64.b64decode(result["data"])
            except Exception as e:
                raise ValueError(f"Base64 解码失败: {e}")

            # 确保目标目录存在
            os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)

            # 将 PDF 内容写入文件
            with open(pdf_file_path, "wb") as f:
                f.write(pdf_data)

            print(f"PDF 已保存到: {pdf_file_path}")

        finally:
            # 清理浏览器实例
            if 'driver' in locals():
                driver.quit()

        return pdf_file_path

    except Exception as e:
        print(f"生成 PDF 过程中发生错误: {e}")
        raise

# 第八步：把 PDF 拼起来
def one_pdf2all_pdf(pdf_paths, output_filename):
    merger = PdfMerger()

    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            merger.append(pdf_path)
        else:
            print(f"文件 {pdf_path} 不存在，跳过。")

    # 确保输出目录存在
    output_dir = os.path.join(os.getcwd(), "merged_pdfs")
    os.makedirs(output_dir, exist_ok=True)

    # 构造输出文件路径
    output_path = os.path.join(output_dir, f"{output_filename}.pdf")

    # 合并 PDF 文件
    merger.write(output_path)
    merger.close()

    print(f"合并后的 PDF 文件已生成，路径为: {output_path}")
    return output_path



if __name__ == "__main__":
    pass
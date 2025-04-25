
import json
import config 
import requests
from util import handle_json,save_step_result_to_txt
from weasyprint import HTML
import os
import re
from datetime import datetime

from workflow_use import plan_llm_xinfer,single_step_web_search,truncate_web_search_data, use_web_data2report_data_table_graph, report_data2report_result, get_report_html_from_report_result,process_html_string,html2pdf,one_pdf2all_pdf

from util import XinferRequest, XinferRequest_Stream
def cover2pdf(query):

    cover_prompt = config.COVER_PROMPT
    # 获取当前时间
    now = datetime.now()
    # 格式化输出当前时间
    time  = now.strftime("%Y-%m-%d")
    
    prompt = """
    # 用户问题: 
    %s
    # 当前时间：
    %s
    # 提示词：
    %s
    """
    prompt = prompt % (query, time, cover_prompt)
    # 调用大模型生成 HTML 报告
    try:
        print("开始流式生成cover HTML 报告:")
        report_cover_html = ""  # 初始化为空字符串

        # 调用流式请求方法
        response_generator = XinferRequest_Stream.parse_response(
            XinferRequest_Stream.request_xinfer(config.QWEN25_URL, config.QWEN25_MODEL, prompt)
        )

        # 迭代生成器并打印每一部分内容
        for chunk in response_generator:
            print(chunk, end="", flush=True)  # 流式打印每个块
            report_cover_html += chunk  # 将每个块追加到 report_html 中

        print("----------可爱的分隔符--------------")
        # print("\n大模型生成的完整 HTML 报告:")
        
        print(report_cover_html)  # 打印完整的 HTML 报告
        processed_cover_html = process_html_string(report_cover_html)
        type="cover"
        pdf_file_path = html2pdf(query,type, processed_cover_html)

        save_step_result_to_txt(pdf_file_path, 'cover', "pdf_file_path")

        return pdf_file_path  # 返回完整的 HTML 报告
    except Exception as e:
        print(f"HTML 报告COVER生成失败: {e}")
        return ""  # 如果发生错误，返回空字符串
    
def catalog2pdf(query,plan_content):

    catalog_prompt = config.CATALOG_PROMPT
    prompt = """
    # 用户问题:
    %s
    # plan内容: 
    %s 
    # 提示词：
    %s
    """
    prompt = prompt % (query, plan_content, catalog_prompt)
    # 调用大模型生成 HTML 报告
    try:
        print("开始流式生成 HTML catalog 报告:")
        report_catalog_html = ""  # 初始化为空字符串

        # 调用流式请求方法
        response_generator = XinferRequest_Stream.parse_response(
            XinferRequest_Stream.request_xinfer(config.QWEN25_URL, config.QWEN25_MODEL, prompt)
        )

        # 迭代生成器并打印每一部分内容
        for chunk in response_generator:
            print(chunk, end="", flush=True)  # 流式打印每个块
            report_catalog_html += chunk  # 将每个块追加到 report_html 中

        print("----------可爱的分隔符--------------")
        # print("\n大模型生成的完整 HTML 报告:")
        
        # print(report_html)  # 打印完整的 HTML 报告
        processed_catalog_html = process_html_string(report_catalog_html)

        type="catalog"
        pdf_file_path = html2pdf(query,type, processed_catalog_html)
        save_step_result_to_txt(pdf_file_path, 'catalog', "pdf_file_path")

        return pdf_file_path  # 返回完整的 HTML 报告
    except Exception as e:
        print(f"HTML 报告catalog生成失败: {e}")
        return "" 
def end_page2pdf(query):
    end_page_prompt = config.END_PAGE_PROMPT
    prompt = """
    # 用户问题:
    %s
    # 提示词：
    %s
    """
    prompt = prompt % (query, end_page_prompt)
    # 调用大模型生成 HTML 报告
    try:
        print("开始流式生成 HTML catalog 报告:")
        report_end_page_html = ""  # 初始化为空字符串

        # 调用流式请求方法
        response_generator = XinferRequest_Stream.parse_response(
            XinferRequest_Stream.request_xinfer(config.QWEN25_URL, config.QWEN25_MODEL, prompt)
        )

        # 迭代生成器并打印每一部分内容
        for chunk in response_generator:
            print(chunk, end="", flush=True)  # 流式打印每个块
            report_end_page_html += chunk  # 将每个块追加到 report_html 中

        print("----------可爱的分隔符--------------")
        # print("\n大模型生成的完整 HTML 报告:")
        
        # print(report_html)  # 打印完整的 HTML 报告
        processed_html = process_html_string(report_end_page_html)
        type="end_page"

        pdf_file_path = html2pdf(query,type, processed_html)

        save_step_result_to_txt(pdf_file_path, 'end_pager', "pdf_file_path")

        return pdf_file_path  # 返回完整的 HTML 报告
    except Exception as e:
        print(f"HTML 报告catalog生成失败: {e}")
        return "" 
# 主函数：循环三次，每次完成一个步骤的完整流程
def process_all_steps(query,plan_data_from_llm):
    all_results = []  # 用于存储所有步骤的结果
    total_start_time = datetime.now()  # 记录整个循环的开始时间

    # 打开时间记录文件
    time_record_file = os.path.join(os.getcwd(), "time_record.txt")
    with open(time_record_file, "a", encoding="utf-8") as time_file:
        time_file.write("\n=== process_all_steps 时间记录 ===\n")

    # 遍历每个步骤的数据
    for step_data in plan_data_from_llm:
        step_number = step_data["step"]  # 获取当前步骤的编号
        plan_title = step_data["title"]  # 获取当前步骤的计划标题
        plan_details = step_data["details"]  # 获取当前步骤的计划细节
        print(f"开始处理步骤 {step_number}")

        # 记录当前步骤的总时间
        step_start_time = datetime.now()

        # 第一步：执行 web_search（单个步骤）
        start_time = datetime.now()
        web_search_data = single_step_web_search(step_data)
        end_time = datetime.now()
        save_step_result_to_txt(web_search_data, step_number, "web_search")
        with open(time_record_file, "a", encoding="utf-8") as time_file:
            time_file.write(f"步骤 {step_number} - web_search: 开始时间 {start_time}, 结束时间 {end_time}\n")

        # 第二步：截断搜索结果
        start_time = datetime.now()
        truncated_data = truncate_web_search_data(web_search_data)
        end_time = datetime.now()
        save_step_result_to_txt(truncated_data, step_number, "truncated_data")
        with open(time_record_file, "a", encoding="utf-8") as time_file:
            time_file.write(f"步骤 {step_number} - truncate_web_search_data: 开始时间 {start_time}, 结束时间 {end_time}\n")

        # 第三步：生成报告和图表材料
        start_time = datetime.now()
        all_report_data = use_web_data2report_data_table_graph(truncated_data,plan_details)
        end_time = datetime.now()
        save_step_result_to_txt(all_report_data, step_number, "all_report_data")
        with open(time_record_file, "a", encoding="utf-8") as time_file:
            time_file.write(f"步骤 {step_number} - use_web_data2report_data_table_graph: 开始时间 {start_time}, 结束时间 {end_time}\n")

        # 第四步：生成最终报告
        start_time = datetime.now()
        final_report_result = report_data2report_result(step_number, plan_title, plan_details, all_report_data)
        end_time = datetime.now()
        save_step_result_to_txt(final_report_result, step_number, "final_report_result")
        with open(time_record_file, "a", encoding="utf-8") as time_file:
            time_file.write(f"步骤 {step_number} - report_data2report_result: 开始时间 {start_time}, 结束时间 {end_time}\n")

        # 第五步：生成 HTML 报告
        start_time = datetime.now()
        html_report = get_report_html_from_report_result(final_report_result, step_number)
        processed_html = process_html_string(html_report)
        end_time = datetime.now()
        with open(time_record_file, "a", encoding="utf-8") as time_file:
            time_file.write(f"步骤 {step_number} - get_report_html_from_report_result: 开始时间 {start_time}, 结束时间 {end_time}\n")

        # 第六步：将 HTML 转换为 PDF
        start_time = datetime.now()
        
        type = "content" + str(step_number)
        pdf_file_path = html2pdf(query,type,processed_html)
        end_time = datetime.now()

        save_step_result_to_txt(pdf_file_path, step_number, "pdf_file_path")
        with open(time_record_file, "a", encoding="utf-8") as time_file:
            time_file.write(f"步骤 {step_number} - html2pdf: 开始时间 {start_time}, 结束时间 {end_time}\n")

        # 记录当前步骤的总时间
        step_end_time = datetime.now()
        with open(time_record_file, "a", encoding="utf-8") as time_file:
            time_file.write(f"步骤 {step_number} 总耗时: 开始时间 {step_start_time}, 结束时间 {step_end_time}\n")

        # 将当前步骤的结果保存到 all_results 中
        all_results.append({
            "step": step_data["step"],
            "web_search_data": web_search_data,
            "truncated_data": truncated_data,
            "all_report_data": all_report_data,
            "final_report_result": final_report_result,
            "html_report": html_report,
            "pdf_file_path": pdf_file_path
        })

    # 记录整个循环的总时间
    total_end_time = datetime.now()
    with open(time_record_file, "a", encoding="utf-8") as time_file:
        time_file.write(f"\nprocess_all_steps 总耗时: 开始时间 {total_start_time}, 结束时间 {total_end_time}\n")

    return all_results


# 新增函数：保存每一步的具体结果到 .txt 文件




if __name__ == "__main__":
    # 用户输入的问题
    query = "帮我生成一份rpa领域的投研报告"
    
    # 打开时间记录文件
    time_record_file = os.path.join(os.getcwd(), "time_record.txt")
    with open(time_record_file, "w", encoding="utf-8") as time_file:
        time_file.write("时间记录日志\n")
        time_file.write("====================\n")

    # 调用 LLM 获取计划
    start_time = datetime.now()
    res = plan_llm_xinfer(query)
    end_time = datetime.now()
    with open(time_record_file, "a", encoding="utf-8") as time_file:
        time_file.write(f"调用 LLM 获取计划: 开始时间 {start_time}, 结束时间 {end_time}\n")
    print("LLM 返回的计划结果:")
    print(res)

    # 解析计划数据
    start_time = datetime.now()
    plan_data_from_llm = handle_json(res)
    end_time = datetime.now()
    with open(time_record_file, "a", encoding="utf-8") as time_file:
        time_file.write(f"解析计划数据: 开始时间 {start_time}, 结束时间 {end_time}\n")
    if not plan_data_from_llm:
        print("无法解析计划数据")
        exit(1)
    
    print("处理json后的计划数据-----:")
    print(json.dumps(plan_data_from_llm, ensure_ascii=False, indent=4))

    # ==================== 生成封面页 PDF ====================
    start_time = datetime.now()
    print("开始生成封面页 PDF...")
    cover_pdf_file_path = cover2pdf(query)
    end_time = datetime.now()
    with open(time_record_file, "a", encoding="utf-8") as time_file:
        time_file.write(f"生成封面页 PDF: 开始时间 {start_time}, 结束时间 {end_time}\n")
    if not cover_pdf_file_path:
        print("封面页生成失败，退出程序。")
        exit(1)

    # ==================== 生成目录页 PDF ====================
    start_time = datetime.now()
    print("开始生成目录页 PDF...")
    # 使用计划数据的第一个步骤作为示例（可以根据实际需求调整）
    plan_content = json.dumps(plan_data_from_llm, ensure_ascii=False)
    
    catalog_pdf_file_path  = catalog2pdf(query, plan_content)
    
    end_time = datetime.now()
    with open(time_record_file, "a", encoding="utf-8") as time_file:
        time_file.write(f"生成目录页 PDF: 开始时间 {start_time}, 结束时间 {end_time}\n")
    if not catalog_pdf_file_path :
        print("目录页生成失败，退出程序。")
        exit(1)

    # ==================== 生成内容页 PDF ====================
    start_time = datetime.now()
    print("开始生成内容页 PDF...")
    all_results = process_all_steps(query,plan_data_from_llm)
    end_time = datetime.now()
    with open(time_record_file, "a", encoding="utf-8") as time_file:
        time_file.write(f"生成内容页 PDF: 开始时间 {start_time}, 结束时间 {end_time}\n")
    # 提取所有步骤生成的 PDF 文件路径
    pdf_paths = [result["pdf_file_path"] for result in all_results if result["pdf_file_path"]]
    if not pdf_paths:
        print("内容页生成失败，退出程序。")
        exit(1)

    # ==================== 生成尾页 PDF ====================
    start_time = datetime.now()
    print("开始生成尾页 PDF...")
    end_page_pdf_file_path = end_page2pdf(query)
    end_time = datetime.now()
    with open(time_record_file, "a", encoding="utf-8") as time_file:
        time_file.write(f"生成尾页 PDF: 开始时间 {start_time}, 结束时间 {end_time}\n")
    if not end_page_pdf_file_path:
        print("尾页生成失败，退出程序。")
        exit(1)

    # ==================== 合并所有 PDF ====================
    start_time = datetime.now()
    print("开始合并所有 PDF...")
    # 添加封面页和目录页的 PDF 路径到列表中
    final_pdf_paths = []
    
    # 添加封面页 PDF
    if os.path.exists(cover_pdf_file_path):
        final_pdf_paths.append(cover_pdf_file_path)
    
    # 添加目录页 PDF
    if os.path.exists(catalog_pdf_file_path):
        final_pdf_paths.append(catalog_pdf_file_path)
    
    # 添加内容页 PDF
    final_pdf_paths.extend(pdf_paths)
    
    # 添加尾页 PDF
    if os.path.exists(end_page_pdf_file_path):
        final_pdf_paths.append(end_page_pdf_file_path)

    # 合并所有 PDF 文件
    merged_pdf_path = one_pdf2all_pdf(final_pdf_paths, "rpa_investment_final_report0421v1")
    end_time = datetime.now()
    with open(time_record_file, "a", encoding="utf-8") as time_file:
        time_file.write(f"合并所有 PDF: 开始时间 {start_time}, 结束时间 {end_time}\n")
    print(f"最终合并的 PDF 文件路径: {merged_pdf_path}")


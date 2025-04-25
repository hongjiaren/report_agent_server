import json
import requests
import config 
from weasyprint import HTML
import os

class XinferRequest:
    @staticmethod
    def request_xinfer(url, model, prompt):

        payload = json.dumps({
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 8192,
            "temperature": 0.001
            })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response
    
    @staticmethod
    def request_xinfer_messages(url, model, messages):

        payload = json.dumps({
            "model": model,
            "messages": messages,
            "max_tokens": 8192,
            "temperature": 0.001
            })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response
    @staticmethod
    def parse_response(response):
        response_json = json.loads(response.text)
        return response_json['choices'][0]['message']['content']
    @staticmethod
    def parse_deepseek_response(response):
        response_json = json.loads(response.text)
        res = response_json['choices'][0]['message']['content']
        if '</think>' in res:
            res = res.split('</think>')[-1]
        return res
    

class XinferRequest_Stream:
    @staticmethod
    def request_xinfer(url, model, prompt):
        payload = json.dumps({
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 8192,
            "temperature": 0.001,
            "stream": True  # 启用流式输出
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload, stream=True)

        return response
    @staticmethod
    def parse_response(response):
        """
        流式解析响应并逐块返回内容。
        """
        buffer = ""
        for line in response.iter_lines(decode_unicode=True):
            if not line:  # 跳过空行
                continue

            # 去掉可能存在的 "data:" 前缀
            if line.startswith("data:"):
                line = line[len("data:"):].strip()

            # 跳过特殊标记 [DONE]
            if line.strip() == "[DONE]":
                continue

            # 尝试解析 JSON 数据
            try:
                line_data = json.loads(line)
                # 提取 delta 中的 content 内容
                choices = line_data.get("choices", [])
                if choices and isinstance(choices, list) and len(choices) > 0:
                    delta = choices[0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        buffer += content
                        yield content  # 流式返回内容
            except json.JSONDecodeError as e:
                continue
                # print(f"JSON 解析错误: {e}, 行内容: {line}")
        
        return buffer  # 返回完整的缓冲区内容（可选）
# 

# 定义处理函数
def handle_json(res):
    try:
        # 规则：从第一个 '[' 到最后一个 ']'
        start_index = res.find('[')
        end_index = res.rfind(']')
        
        if start_index == -1 or end_index == -1 or start_index >= end_index:
            raise ValueError("输入数据不符合从第一个 '[' 到最后一个 ']' 的规则")
        
        # 提取有效 JSON 部分
        json_str = res[start_index:end_index + 1]
        
        # 将字符串解析为JSON对象
        data = json.loads(json_str)
        
        # 确保数据是一个列表
        if not isinstance(data, list):
            raise ValueError("输入数据不是有效的JSON数组")
        
        # 提取所有内容并保持格式
        plan_data_from_llm = []
        for item in data:
            plan_data_from_llm.append({
                "step": item.get("step"),
                "title": item.get("title"),
                "details": item.get("details")
            })
        
        # 返回提取后的数据
        return plan_data_from_llm
    
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None
    except Exception as e:
        print(f"其他错误: {e}")
        return None

def process_html_string(input_str):
    """
    提取字符串中第一个 '<' 开头和最后一个 '>' 结尾的内容，包括这两个符号。
    如果内容是 <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>，
    则替换为 <script src="{{ url_for('static', filename='chart.js') }}"></script>。

    :param input_str: 输入的字符串
    :return: 提取并可能替换后的字符串
    """
    # 去掉首尾空白字符
    stripped_str = input_str.strip()

    # 找到第一个 '<' 和最后一个 '>'
    start_index = stripped_str.find('<')
    end_index = stripped_str.rfind('>')

    # 检查是否找到有效的 '<' 和 '>'
    if start_index != -1 and end_index != -1 and start_index < end_index:
        # 提取从第一个 '<' 到最后一个 '>' 的内容（包括这两个符号）
        extracted_content = stripped_str[start_index:end_index + 1]

        # 检查是否需要替换特定的 <script> 标签
        target_script = '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
        replacement_script = '<script src="http://60.165.238.132:9000/js_source/chart.js"></script>'

        if extracted_content == target_script:
            print("替换 <script> 标签")
            return replacement_script
        else:
            return extracted_content
    else:
        raise ValueError("输入字符串中未找到有效的 '<' 和 '>' 符号")
def html2pdf(html_content, output_filename):
    """
    将 HTML 内容转换为 PDF 文件。
    
    :param html_content: HTML 内容 (字符串)
    :param output_filename: 输出的 PDF 文件名
    :return: 生成的 PDF 文件路径
    """
    # 确保 PDF 存储目录存在
    PDF_DIR = os.path.join(os.getcwd(), "pdfs")
    os.makedirs(PDF_DIR, exist_ok=True)

    # 构造 PDF 文件路径
    pdf_file_path = os.path.join(PDF_DIR, f"{output_filename}.pdf")

    # 使用 WeasyPrint 将 HTML 转换为 PDF
    HTML(string=html_content).write_pdf(pdf_file_path)

    return pdf_file_path

def save_step_result_to_txt(step_result, step_number, result_type):
    """
    保存当前步骤的具体结果到 .txt 文件。
    
    :param step_result: 当前步骤的具体结果数据
    :param step_number: 当前步骤的编号
    :param result_type: 结果类型（例如 "web_search", "truncated_data" 等）
    """
    # 定义保存文件的路径和名称
    file_path = f"step_{step_number}_{result_type}.txt"
    
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            if isinstance(step_result, (list, dict)):
                # 如果是列表或字典，使用 JSON 格式保存
                json.dump(step_result, file, ensure_ascii=False, indent=4)
            else:
                # 如果是字符串或其他类型，直接写入
                file.write(str(step_result))
        
        print(f"步骤 {step_number} 的 {result_type} 结果已保存到文件: {file_path}")
    except Exception as e:
        print(f"步骤 {step_number} 的 {result_type} 结果保存失败: {e}")


if __name__ == "__main__":
    url = "https://algo-test.ai-indeed.com/qwen/rag/v1/chat/completions"
    model = "qwen-chat"
    prompt = "你好，帮我生成一个100字的微电子投研报告" + config.GENERATE_PROMPT
    
    # 调用流式请求方法
    response_generator = XinferRequest_Stream.parse_response(XinferRequest_Stream.request_xinfer(url, model, prompt))
    report_html = ""

    # 迭代生成器并打印每一部分内容
    for chunk in response_generator:
        print(chunk, end="", flush=True)  # 使用 end="" 和 flush=True 实现流式输出效果
        report_html += chunk

    report_html = process_html_string(report_html)
    print("========================================================") 
    print(report_html) 
        # 将 HTML 报告转换为 PDF
    output_filename = "microelectronics_investment_report"
    pdf_path = html2pdf(report_html, output_filename)
    print(f"PDF 文件已生成，路径为: {pdf_path}")
# if __name__ == "__main__":
#     url = "https://algo-test.ai-indeed.com/qwen/rag/v1/chat/completions"
#     model = "qwen-chat"
#     prompt = "你是一个行业投研报告分析的专家，需要根据用户问题，给出相关的行业投研报告，请先给出你写的投研报告的大纲。 用户输入，请帮我生成一份rpa行业的投研报告"
#     res = XinferRequest.parse_response(XinferRequest.request_xinfer(url, model, prompt))
#     print(res)

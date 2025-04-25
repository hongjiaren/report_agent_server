# 模拟配置文件中的 HTML 模板

class Config:
    CONTENT_GENERATE_PROMPT = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>投研报告 - 第{}部分</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #fff;
            padding: 10px 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            font-weight: bold;
        }
        h2 {
            color: #555;
            font-style: italic;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <header>
        <img src="http://60.165.238.132:9000/images_report/ai-indeed-logo.jpg" alt="实在智能Logo" style="height: 30px;">
    </header>
    <h1>投研报告 - 第{}部分</h1>
    <h2>当前步骤标题</h2>
    <p>{}</p>
</body>
</html>
"""

# 模拟大模型流式生成逻辑
class XinferRequest_Stream:
    @staticmethod
    def request_xinfer(url, model, prompt):
        # 模拟返回 HTML 内容
        html_content = """
        <p>这是由大模型生成的 HTML 报告内容。</p>
        <p>报告步骤编号：{}</p>
        """.format(prompt.split("第")[1].split("步")[0])  # 提取步骤编号
        yield html_content

    @staticmethod
    def parse_response(response_generator):
        for chunk in response_generator:
            yield chunk

# 配置对象
config = Config()
config.QWEN25_URL = "http://example.com/api"
config.QWEN25_MODEL = "qwen2.5"

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
# 测试函数
def test_get_report_html():
    all_report_data = """
    这是一份关于 RPA 行业的投研报告。
    数据来源：产业报告 2024。
    """
    step = 6  # 当前是第 6 步

    # 调用函数
    report_html = get_report_html_from_report_result(all_report_data, step)

    # 打印最终生成的 HTML
    print("\n最终生成的完整 HTML 报告:")
    print(report_html)

# 运行测试
test_get_report_html()
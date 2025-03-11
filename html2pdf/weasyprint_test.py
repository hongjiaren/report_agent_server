from weasyprint import HTML

html_content = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>人工智能领域投研报告</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            color: #333;
        }
        .page {
            width: 90%;
            max-width: 1200px;
            margin: auto;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            margin-top: 20px;
            page-break-after: always; /* 强制分页 */
        }
        h1, h2 {
            color: #2c3e50;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            margin-bottom: 20px;
            border-collapse: collapse;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        img {
            width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .chart-container {
            margin: 20px auto;
            text-align: center;
        }
        p {
            line-height: 1.6;
        }
        .footer {
            text-align: center;
            padding: 20px;
            background-color: #f4f4f9;
            color: #777;
            font-size: 0.9em;
        }
        .cover {
            text-align: center;
            padding: 50px 20px;
            background-color: #4CAF50;
            color: white;
            margin-bottom: 20px;
        }
        .cover h1 {
            font-size: 2.5em;
            margin: 0;
        }
        .analyst-info {
            margin-top: 20px;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .analyst-info h2 {
            color: #2c3e50;
        }
        .analyst-info p {
            color: #555;
        }
        .toc {
            list-style-type: none;
            padding-left: 0;
        }
        .toc li {
            margin: 10px 0;
        }
        .toc a {
            text-decoration: none;
            color: #2c3e50;
            font-weight: bold;
        }
    </style>
</head>
<body>

<!-- 封面 -->
<div class="page cover">
    <h1>人工智能领域投研报告</h1>
    <div class="analyst-info">
        <h2>分析师介绍</h2>
        <p>本报告由实在智能TARS金融分析师团队编写，旨在为您提供最专业的行业见解。</p>
        <p>分析师：实在智能TARS金融分析师</p>
        <p>联系方式：contact@tarsfinance.com</p>
    </div>
</div>

<!-- 目录 -->
<div class="page">
    <h2>目录</h2>
    <ul class="toc">
        <li><a href="#market-overview">一、人工智能市场概览</a></li>
        <li><a href="#tech-progress">二、关键技术研发进展</a></li>
        <li><a href="#investment-trends">三、投资趋势分析</a></li>
        <li><a href="#future-outlook">四、未来展望</a></li>
    </ul>
</div>

<!-- 内容 -->
<div class="page">

<h2 id="market-overview">一、人工智能市场概览</h2>

<p>随着技术的进步，人工智能（AI）正在迅速改变各行各业的面貌。</p>

<div class="chart-container">
    <!-- 饼状图 -->
    <img src="https://q3.itc.cn/images01/20240118/b33aeb6920484c6681f2c6dc9fcd2c29.png" alt="市场细分饼状图">
</div>

<h2 id="tech-progress">二、关键技术研发进展</h2>

<table>
    <thead>
        <tr>
            <th>技术方向</th>
            <th>研究机构/公司</th>
            <th>最新成果</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>自然语言处理</td>
            <td>某大学实验室</td>
            <td>发布了新的预训练模型</td>
        </tr>
        <tr>
            <td>计算机视觉</td>
            <td>某科技公司</td>
            <td>提高了图像识别精度</td>
        </tr>
    </tbody>
</table>

<h2 id="investment-trends">三、投资趋势分析</h2>

<p>近年来，人工智能领域的投资呈现出快速增长的趋势。</p>

<div class="chart-container">
    <!-- 折线图 -->
    <img src="https://pic.rmb.bdstatic.com/bjh/down/d45652d09ff355afc223edc58352ebbe.png" alt="年度投资额图">
</div>

<h2 id="future-outlook">四、未来展望</h2>

<p>预计在未来几年内，人工智能将在更多领域实现突破，带来前所未有的变革。</p>

<div class="chart-container">
    <!-- 示例图片 -->
    <img src="https://q2.itc.cn/q_70/images01/20241024/e3f41bfea3844430acfb29583fa7bd7b.png" alt="相关示意图">
</div>

</div>

<!-- 尾页 -->
<div class="page footer">
    <p>&copy; 2025 实在智能TARS金融分析师团队. 版权所有.</p>
    <p>联系我们：contact@tarsfinance.com</p>
</div>

</body>
</html>
'''

# 通过HTML字符串创建HTML对象
html = HTML(string=html_content)

# 转换HTML字符串到PDF
html.write_pdf('weasyprint_output.pdf')
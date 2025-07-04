import requests

# 本地Flask服务地址
url = "http://127.0.0.1:5535/generate_pdf"

# 示例HTML内容
html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>XX行业投研分析报告</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        body {
            font-family: Arial, sans-serif;
            color: #333;
            line-height: 1.5;
        }
        .cover, .toc, .content, .footer {
            page-break-after: always;
        }
        .cover {
            text-align: center;
            padding-top: 10%;
            position: relative;
        }
        .cover img {
            width: 100%;
            height: auto;
            margin-bottom: 20px;
        }
        .cover h1 {
            font-size: 3em;
            color: #fff;
            background-color: rgba(0, 0, 0, 0.5);
            display: inline-block;
            padding: 10px;
            margin-bottom: 0;
        }
        .header img {
            width: 100px;
            height: auto;
            position: absolute;
            top: 2cm;
            right: 2cm;
        }
        .content h2, .content h3 {
            font-size: 1.8em;
            color: #0056b3;
            margin-top: 2em;
        }
        .footer {
            text-align: left;
            padding-top: 50px;
            background-color: #f0f0f0;
        }
        .disclaimer {
            font-size: 1.1em;
            color: #555;
            margin-top: 20px;
        }
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        .toc a {
            text-decoration: none;
            color: #333;
        }
    </style>
</head>
<body>
<div class="cover">
    <img src="https://img0.baidu.com/it/u=1136713591,3022880638&fm=253&fmt=auto&app=138&f=PNG?w=600&h=384" alt="实在智能">
    <h1>XX行业投研分析报告</h1>
    <p style="font-size:1.5em; color:#fff; background-color:rgba(0, 0, 0, 0.5); padding:10px;">分析师：实在agent金融分析师</p>
    <p style="font-size:1.5em; color:#fff; background-color:rgba(0, 0, 0, 0.5); padding:10px;">邮箱：ai-indeed@i-i.com</p>
    <p style="font-size:1.5em; color:#fff; background-color:rgba(0, 0, 0, 0.5); padding:10px;">电话：400012345</p>
    <p style="font-size:1.5em; color:#fff; background-color:rgba(0, 0, 0, 0.5); padding:10px; margin-top:30px;">请仔细阅读在本报告尾部的重要法律声明。</p>
</div>

<div class="header"><img src="https://img0.baidu.com/it/u=1136713591,3022880638&fm=253&fmt=auto&app=138&f=PNG?w=600&h=384" alt="实在智能"></div>
<div class="toc">
    <h2>目录</h2>
    <ul>
        <li><a href="#section1">1. 第一部分：市场概览</a></li>
        <li><a href="#section2">2. 第二部分：竞争分析</a></li>
        <!-- 添加更多目录项 -->
    </ul>
</div>

<div class="content">
    <h2 id="section1">1. 第一部分：市场概览</h2>
    <p>这里是关于市场概览的详细内容...</p>

    <h2 id="section2">2. 第二部分：竞争分析</h2>
    <p>这里是关于竞争分析的详细内容...</p>
</div>

<div class="footer">
    <div class="disclaimer">
        <strong>分析师承诺：</strong><br>
        作者具有中国证券业协会授予的证券投资咨询执业资格或相当的专业胜任能力，保证报告所采用的数据均来自合规渠道，分析逻辑基于作者的职业理解，通过合理判断并得出结论，力求客观、公正，结论不受任何第三方的授意、影响，特此声明。<br><br>
        <strong>实在Agent免责声明：</strong><br>
        • 实在Agent（以下简称“本公司”）具备证券投资咨询业务资格。本报告仅供本公司签约客户使用。本公司不会因接收人收到或者经由其他渠道转发收到本报告而直接视其为本公司客户。<br>
        • 本报告基于本公司研究所及其研究人员认为的已经公开的资料或者研究人员的实地调研资料，但本公司对该等信息的准确性、完整性或可靠性不作任何保证。本报告所载资料、意见以及推测仅于本报告发布当日的判断，且这种判断受到研究方法、研究依据等多方面的制约。在不同时期，本公司可发出与本报告所载资料、意见及预测不一致的报告。本公司不保证本报告所含信息始终保持在最新状态。同时，本公司对本报告所含信息可在不发出通知的情形下做出修改，投资者需自行关注相应更新或修改。<br>
        • 在任何情况下，本报告仅提供给签约客户参考使用，任何信息或所表述的意见绝不构成对任何人的投资建议。市场有风险，投资需谨慎。投资者不应将本报告视为做出投资决策的唯一参考因素，亦不应认为本报告可以取代自己的判断。在任何情况下，本报告均未考虑到个别客户的特殊投资目标、财务状况或需求，不能作为客户进行买卖、认购证券或者其他金融工具的保证或邀请。在任何情况下，本公司、本公司员工或者其他关联方均不承诺投资者一定获利，不与投资者分享投资收益，也不对任何人因使用本报告而导致的任何可能损失负有任何责任。投资者因使用本公司研究报告做出的任何投资决策均是独立行为，与本公司、本公司员工及其他关联方无关。<br>
        • 本公司建立起信息隔离墙制度、跨墙制度来规范管理跨部门、跨关联机构之间的信息流动。务请投资者注意，在法律许可的前提下，本公司及其所属关联机构可能会持有报告中提到的公司所发行的证券或期权并进行证券或期权交易，也可能为这些公司提供或者争取提供投资银行、财务顾问或者金融产品等相关服务。在法律许可的前提下，本公司的董事、高级职员或员工可能担任本报告所提到的公司的董事。本公司及其所属关联机构或个人可能在本报告公开发布之前已经使用或了解其中的信息。<br>
        • 所有报告版权均归本公司所有。未经本公司事先书面授权，任何机构或个人不得以任何形式复制、转发或公开传播本报告的全部或部分内容，如需引用、刊发或转载本报告，需注明出处为实在Agent，且不得对本报告进行任何有悖原意的引用、删节和修改。
    </div>
    <p>© 实在Agent投研分析团队 2025. 版权所有。</p>
    <p>联系我们：<a href="mailto:contact@realagent.com">contact@realagent.com</a></p>
</div>
</body>
</html>
"""

# 发送POST请求到Flask服务
response = requests.post(url, json={"html_content": html_content, "filename": "test_pdf3211646"})

# 检查响应状态码是否为200（成功）
if response.status_code == 200:
    pdf_url = response.json().get("pdf_url")
    print(f"PDF generated successfully. You can download it from: {pdf_url}")
else:
    print(f"Failed to generate PDF. Status code: {response.status_code}, Response: {response.text}")
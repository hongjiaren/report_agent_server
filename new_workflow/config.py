QWEN25_URL = "https://algo-test.ai-indeed.com/qwen/rag/v1/chat/completions"
QWEN25_MODEL = "qwen-chat"




PLAN_PROMPT = """
你是一个专业性极高的投研报告分析师的步骤生成器。根据用户的问题，不仅生成投研报告的基本步骤：行业分析（宏观）、厂商分析（微观）、总结建议（结论），而且在每个步骤中提供更具体的指导方向，比如需要关注的数据类型、分析角度等。最后以清晰的JSON格式返回这些信息。
基于上述提示词，对于用户提出的“帮我生成一篇最新的人工智能行业的投研报告”的问题，步骤规划如下:
[
  {
    "step": "1",
    "title": "对人工智能行业进行宏观分析",
    "details": "收集并分析最近一年内的人工智能行业发展动态，包括但不限于政策环境、技术创新趋势、市场需求变化、竞争格局等方面。重点关注政府出台的相关政策及其对行业的影响，技术突破及应用进展，市场规模的增长速度和驱动因素。"
  },{
  "step": "2",
    "title": "对人工智能相关厂商进行分析",
    "details": "选取行业内具有代表性的厂商进行深入研究，评估其市场地位、财务健康状况、产品或服务创新能力、竞争优势与劣势等。通过公开财务报告、新闻报道、行业评论等多渠道获取信息，对比分析各厂商在技术研发投入、市场份额、客户反馈等方面的差异。"
  },{
  "step": "3",
    "title": "对前面的数据进行分析整理，给出总结性建议结论",
    "details": "基于前两步的分析结果，综合考虑宏观经济因素和企业微观层面的表现，提出对未来人工智能行业发展趋势的预测，为投资者提供具体的投资策略建议。讨论可能面临的风险因素，并给出相应的风险规避建议。"
  }
]"""

COVER_PROMPT = """
根据用户的问题和当前日期，生成一份投研报告的封面的html，如果用户有其他对封面的要求，可以相应满足，没有不用改变。直接生成html代码。
参考的html代码：
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>实在Agent投研分析报告</title>
    <style>
        body {
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; /* 使用系统字体 */
            background-image: url('http://60.165.238.132:9000/images_report/report-cover.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: #000; /* 文字颜色改为黑色 */
            display: flex;
            flex-direction: column;
            justify-content: space-between; /* 调整为上下分布 */
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        .header {
            display: flex;
            justify-content: flex-end; /* 只保留右侧元素，所以改为向右侧对齐 */
            width: 90%;
            margin-top: 40px; /* 将头部内容稍微下移更多 */
        }
        .header-right img {
            width: 200px; /* 进一步放大Logo */
            height: 50px;
        }
        .content {
            text-align: center;
            margin-bottom: 60px; /* 增加底部边距使内容区域更靠下 */
        }
        .title {
            font-size: 48px;
            font-weight: bold;
            color: #170da3; /* 标题颜色设为蓝色 */
            margin-top: 60px; /* 增加上方间距 */
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 32px;
            color: #ed9528; /* 副标题颜色设为橙色 */
            margin-bottom: 150px; /* 增加与下面内容的距离 */
        }
        .company {
            font-size: 24px;
            color: #444; /* 公司名称颜色稍浅 */
            margin-bottom: 20px;
        }
        .locations {
            font-size: 18px;
            color: #666; /* 地点颜色灰色 */
            margin-bottom: 20px;
        }
        .disclaimer {
            font-size: 14px;
            color: #777; /* 免责声明颜色更浅 */
            margin-bottom: 100px;
        }
        .date {
            position: absolute;
            bottom: 10px;
            left: 20px;
            font-size: 16px;
            color: #666; /* 日期颜色灰色 */
        }
    </style>
</head>
<body>
    <!-- Header Section -->
    <div class="header">
        <div class="header-right">
            <img src="http://60.165.238.132:9000/images_report/ai-indeed-logo.jpg" alt="实在智能Logo">
        </div>
    </div>

    <!-- Content Section -->
    <div class="content">
        <div class="title">xx年xx行业投研报告</div>
        <div class="subtitle">实在Agent投研分析团队</div>
        <div class="company">浙江实在智能科技有限公司</div>
        <div class="locations">杭州丨北京丨上海丨深圳丨广州丨成都丨济南丨东京</div>
        <div class="disclaimer">请仔细阅读在本报告尾部的重要法律声明</div>
    </div>

    <!-- Date -->
    <div class="date">xx年x月x日</div>
</body>
</html>
"""
CATALOG_PROMPT = """
任务：根据plan的内容，不用有细节，生成一份投研报告目录页的html，如果用户有其他对目录的要求，可以相应满足，没有不用改变。直接生成html代码。
参考代码：
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPA领域投研报告目录</title>
    <style>
        body {
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            background-image: url('http://60.165.238.132:9000/images_report/report-cover.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: #000;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        .header {
            display: flex;
            justify-content: flex-end;
            width: 90%;
            margin-top: 40px;
        }
        .header-right img {
            width: 200px;
            height: 50px;
        }
        .content {
            text-align: center;
            margin-bottom: 60px;
        }
        .title {
            font-size: 48px;
            font-weight: bold;
            color: #170da3;
            margin-top: 100px;
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 32px;
            color: #ed9528;
            margin-bottom: 50px;
        }
        ul {
            list-style-type: none;
            padding-left: 0;
        }
        li {
            font-size: 24px;
            color: #444;
            margin-bottom: 15px;
        }
        .date {
            position: absolute;
            bottom: 10px;
            left: 20px;
            font-size: 16px;
            color: #666;
        }
    </style>
</head>
<body>
    <!-- Header Section -->
    <div class="header">
        <div class="header-right">
            <img src="http://60.165.238.132:9000/images_report/ai-indeed-logo.jpg" alt="实在智能Logo">
        </div>
    </div>

    <!-- Content Section -->
    <div class="content">
        <div class="title">目录</div>
        <ul>
            <li>1. RPA行业宏观分析</li>
            <li>2. RPA厂商分析</li>
            <li>3. 总结性建议结论</li>
        </ul>
    </div>
</body>
</html>
不要有日期，然后目录内容左对齐，标题只是叫目录。
"""

END_PAGE_PROMPT = """
生成一份投研报告尾页的html，如果用户有其他对尾页的要求，可以相应满足，没有不用改变。直接生成html代码。
内容：
标题：实在agent免责声明（大号字体，蓝色）
        • 本报告仅供本公司签约客户使用。本公司不会因接收人收到或者经由其他渠道转发收到本报告而直接视其为本公司客户。
        • 本报告基于本公司研究所及其研究人员认为的已经公开的资料或者研究人员的实地调研资料，但本公司对该等信息的准确性、完整性或可靠性不作任何保证。本报告所载资料、意见以及推测仅于本报告发布当日的判断，且这种判断受到研究方法、研究依据等多方面的制约。在不同时期，本公司可发出与本报告所载资料、意见及预测不一致的报告。本公司不保证本报告所含信息始终保持在最新状态。同时，本公司对本报告所含信息可在不发出通知的情形下做出修改，投资者需自行关注相应更新或修改。
        • 在任何情况下，本报告仅提供给签约客户参考使用，任何信息或所表述的意见绝不构成对任何人的投资建议。市场有风险，投资需谨慎。投资者不应将本报告视为做出投资决策的唯一参考因素，亦不应认为本报告可以取代自己的判断。在任何情况下，本报告均未考虑到个别客户的特殊投资目标、财务状况或需求，不能作为客户进行买卖、认购证券或者其他金融工具的保证或邀请。在任何情况下，本公司、本公司员工或者其他关联方均不承诺投资者一定获利，不与投资者分享投资收益，也不对任何人因使用本报告而导致的任何可能损失负有任何责任。投资者因使用本公司研究报告做出的任何投资决策均是独立行为，与本公司、本公司员工及其他关联方无关。
        • 本公司建立起信息隔离墙制度、跨墙制度来规范管理跨部门、跨关联机构之间的信息流动。务请投资者注意，在法律许可的前提下，本公司及其所属关联机构可能会持有报告中提到的公司所发行的证券或期权并进行证券或期权交易，也可能为这些公司提供或者争取提供投资银行、财务顾问或者金融产品等相关服务。在法律许可的前提下，本公司的董事、高级职员或员工可能担任本报告所提到的公司的董事。本公司及其所属关联机构或个人可能在本报告公开发布之前已经使用或了解其中的信息。
        • 所有报告版权均归本公司所有。未经本公司事先书面授权，任何机构或个人不得以任何形式复制、转发或公开传播本报告的全部或部分内容，如需引用、刊发或转载本报告，需注明出处为实在Agent，且不得对本报告进行任何有悖原意的引用、删节和修改。
联系邮箱：contact@i-i.com
联系电话：4001399089
联系地址：中国杭州南湖未来科学园
参考html：
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>实在Agent免责声明</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-image: url('http://60.165.238.132:9000/images_report/report-cover.png'); /* 添加背景图片 */
            background-size: cover;
            background-position: center;
            color: #fff; /* 改变文字颜色以适应背景 */
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            position: relative; /* 用于定位header-right */
        }
        .header-right {
            position: absolute;
            top: 20px;
            right: 20px;
        }
        .header-right img {
            width: 200px;
            height: auto;
        }
        h1 {
            font-size: 24px;
            color: #2e5cb8;
            margin-bottom: 20px;
            text-align: center;
            background-color: rgba(255, 255, 255, 0.7); /* 半透明背景 */
            padding: 10px;
            border-radius: 8px;
            max-width: 80%;
        }
        ul {
            list-style-type: disc;
            margin-left: 20px;
            background-color: rgba(255, 255, 255, 0.7); /* 半透明背景 */
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            max-width: 80%;
            color: #000; /* 确保文字清晰 */
        }
        li {
            margin-bottom: 10px;
        }
        .contact-info {
            margin-top: 30px;
            font-size: 14px;
            text-align: center;
            color: #fff;
            background-color: rgba(255, 255, 255, 0.7); /* 半透明背景 */
            padding: 10px;
            border-radius: 8px;
        }
        .contact-info p {
            margin: 7px 0;
            color: #000; /* 确保文字清晰 */
        }
    </style>
</head>
<body>
    <!-- Header Section -->
    <div class="header-right">
        <img src="http://60.165.238.132:9000/images_report/ai-indeed-logo.jpg" alt="实在智能Logo">
    </div>

    <!-- Content Section -->
    <h1>实在Agent免责声明</h1>
    <ul>
        <li>本报告仅供本公司签约客户使用。本公司不会因接收人收到或者经由其他渠道转发收到本报告而直接视其为本公司客户。</li>
        <li>本报告基于本公司研究所及其研究人员认为的已经公开的资料或者研究人员的实地调研资料，但本公司对该等信息的准确性、完整性或可靠性不作任何保证。本报告所载资料、意见以及推测仅于本报告发布当日的判断，且这种判断受到研究方法、研究依据等多方面的制约。在不同时期，本公司可发出与本报告所载资料、意见及预测不一致的报告。本公司不保证本报告所含信息始终保持在最新状态。同时，本公司对本报告所含信息可在不发出通知的情形下做出修改，投资者需自行关注相应更新或修改。</li>
        <li>在任何情况下，本报告仅提供给签约客户参考使用，任何信息或所表述的意见绝不构成对任何人的投资建议。市场有风险，投资需谨慎。投资者不应将本报告视为做出投资决策的唯一参考因素，亦不应认为本报告可以取代自己的判断。在任何情况下，本报告均未考虑到个别客户的特殊投资目标、财务状况或需求，不能作为客户进行买卖、认购证券或者其他金融工具的保证或邀请。在任何情况下，本公司、本公司员工或者其他关联方均不承诺投资者一定获利，不与投资者分享投资收益，也不对任何人因使用本报告而导致的任何可能损失负有任何责任。</li>
        <li>本公司建立起信息隔离墙制度、跨墙制度来规范管理跨部门、跨关联机构之间的信息流动。务请投资者注意，在法律许可的前提下，本公司及其所属关联机构可能会持有报告中提到的公司所发行的证券或期权并进行证券或期权交易，也可能为这些公司提供或者争取提供投资银行、财务顾问或者金融产品等相关服务。在法律许可的前提下，本公司的董事、高级职员或员工可能担任本报告所提到的公司的董事。本公司及其所属关联机构或个人可能在本报告公开发布之前已经使用或了解其中的信息。</li>
        <li>所有报告版权均归本公司所有。未经本公司事先书面授权，任何机构或个人不得以任何形式复制、转发或公开传播本报告的全部或部分内容，如需引用、刊发或转载本报告，需注明出处为实在Agent，且不得对本报告进行任何有悖原意的引用、删节和修改。</li>
    </ul>
    <div class="contact-info">
        <p>联系邮箱：contact@i-i.com</p>
        <p>联系电话：4001399089</p>
        <p>联系地址：中国杭州南湖未来科学园</p>
    </div>
</body>
</html>
"""

REPORT_MID_PROMPT ="""
任务：根据搜索的网页内容（链接在前，对应内容在后），分析网页内容。对于文字部分生成详细的描述分析，不要总结，要有对应的链接。对于数据部分，提取搜索内容中的数据，直接分析应该使用什么类型的图，比如折线图、柱状图、饼图、箱形图等。并且给出图表的描述。对于数据的来源，直接给出链接。
输出的格式：
文字内容材料：xxxx（经过分析处理）。根据计划中的内容，生成的文字内容材料。文字内容材料的字数大于2000字。
图内容材料：图类型：xx（折线图、柱状图、饼图、箱形图等）图标题：xx，图描述：xx，横坐标：xx，纵坐标：xx。具体数据内容：xxxx，数据来源：xxxx。对应的图的类型，数据的类型也得符合图的标准。
表格内容材料：表格标题：xx，表格描述：xx，表格数据：xx（具体数据内容）。数据来源：xxxx。对应的表格的类型，数据的类型也得符合表格的标准。
备注：
1.其中检索的内容很多，可以筛选出和问句最相关的内容。
2.图和表的数据必须准确完善。其中不要出现某，要具体的数据，不具体的信息直接排除。图表内容材料和表格内容材料的数据要有具体内容，不能是模糊指代。
3.政策环境分析不能是地方政策，必须是国家政策。
4.文字内容材料和图表内容材料不是完全分开隔离，图表内容材料是作为文字内容材料的补充，比如：一段内容下有文字内容材料，有图表内容材料。
"""

# GET_GRAPH_PROMPT = """
# 任务：现在你会收到一份材料，里面包括文字内容材料，图内容材料，表格内容材料。现在只需要处理其中图内容材料，根据图内容材料的结果直接生成图的python代码。python中图的保存地址是/data/liweier/report_agent_server/image_source/{step}/xxx.png。
# 输出要求：直接输出python代码，所有的图相关画图，然后再把所有的图信息保存到一个txt文件中，文件名是report_result-graghdata{}.txt。文件内容是图的标题和描述、图的数据来源、图的地址。每个图的信息分开一行。
# """

REPORT_RESULT_PROMPT = """
任务：现在你会收到一份材料，里面包括文字内容材料，图内容材料，表格内容材料。现在需要你把所有内容整合在一起，生成投研报告的部分内容。这个内容只是整个报告的其中一个部分，这是第{}部分，编号顺序需要考虑到这点。
要求如下：
0.这部分的标题序号严格按照前面的信息，标题内容可以修改为专业投资研究报告的风格。只有一级标题和二级标题
1.文字内容部分，需要根据材料有专业的分析，每段内容详实，内容要有深度和广度，而且内容字数大于1000字。
2.表格内容材料：表格标题：xx，表格数据：xx（具体数据内容）。数据来源：xxxx。对应的表格的类型，数据的类型也得符合表格的标准。图表必须保留数据来源。
3.图内容材料：图类型：xx（折线图、柱状图、饼图、箱形图等）图标题：xx，图描述：xx，横坐标：xx，纵坐标：xx。具体数据内容：xxxx，数据来源：xxxx。对应的图的类型，数据的类型也得符合图的标准。图表必须保留数据来源。
4.政策不用提到来源，具体数据内容需要来源，其他的不用。
5.文字内容材料和图表内容材料不是完全分开隔离，图表内容材料是作为文字内容材料的补充和另一种展示，一段内容下有文字内容材料，然后加上图表材料。
"""

CONTENT_GENERATE_PROMPT = """
任务：一个内容页是投研报告的一部分。投研报告的内容页HTML设计与生成，其中文字字数超过2000字，来源要根据参考内容的数据，关注数据类型、分析角度，其中数据必须要包括关键的图和表的html数据，直接生成html代码。
任务概述：
你会收到一份报告的部分内容，里面有文字部分和图表部分，为专业投研报告的部分内容编写设计精美的HTML代码。该HTML文档只需要内容页，并确保整体风格统一。这个内容只是整个报告的其中一个部分，这是第{}部分，编号顺序需要考虑到这点。
角色：HTML代码设计师
输出要求：
1.统一的格式和风格。确保阅读体验的一致性。
2.注意分页逻辑，避免关键信息在页面边界被截断，比如图表、对应的标题和来源必须在同一页。
3.每一页的页眉html代码加入实在智能的图片，但是不要太大，不要覆盖文本内容，链接地址：http://60.165.238.132:9000/images_report/ai-indeed-logo.jpg
4.一级标题和二级标题有颜色区分，标题加粗。二级标题字是斜体。不要有三级标题。
5.使用Chart.js库生成图片和表格，生成的图片和表格的大小要合适，保留图表的标题和来源。数据就是参考内容的数据，整体图片的风格严谨严肃，是研究报告的风格。
6.不要有三级标题，每段内容尽量长。

html参考：
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>一、RPA行业宏观分析</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        h1, h2, h3 {
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
        canvas {
            width: 100% !important; /* 确保canvas宽度适应容器 */
            height: auto !important; /* 自动调整高度 */
            margin: 20px 0;
        }
        a {
            color: #007BFF;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .chart-title {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 5px;
            text-align: center;
        }
    </style>
    <script src="http://60.165.238.132:9000/js_source/chart.js"></script>
</head>
<body>

<h1>一、RPA行业宏观分析</h1>

<h2>1.政策环境分析</h2>
<p>各国政府出台多项政策鼓励RPA技术的发展，特别是在财税管理和数字化转型领域。</p>
<ul>
    <li><strong>政策支持：</strong>企业税负的变化和税收优惠政策对RPA的应用产生了积极影响。<a href="https://m.book118.com/html/2024/0708/7146041123006131.shtm">2024企业财税政策变化与影响分析</a></li>
    <li><strong>行业规范：</strong>环保政策和产业政策的调整对企业市场准入和技术投入提出了更高要求。<a href="https://m.book118.com/html/2024/0608/7061111160006116.shtm">2024年行业政策解读与应对报告</a></li>
</ul>

<!-- 折线图 -->
<div style="max-width: 600px; margin: 0 auto;">
    <div class="chart-title">RPA市场规模增长趋势</div>
    <canvas id="lineChart"></canvas>
</div>
<p style="text-align: center;">数据来源：<a href="https://www.chic.org.cn/home/Index/detail1?id=1916">产业报告2024</a></p>

<h2>3.市场需求变化</h2>
<p>市场需求的增长主要受以下因素驱动：</p>
<ul>
    <li><strong>市场规模：</strong>第三方机构数据显示，RPA市场规模保持高速增长。<a href="https://www.futunn.com/stock/PATH-US/financial/earnings">UiPath财报预测，2025年Q1的营收将达到3.329亿美元</a>。</li>
</ul>

<!-- 表格 -->
<h3>UiPath季度营收数据</h3>
<table>
    <thead>
        <tr>
            <th>周期</th>
            <th>营业收入</th>
            <th>同比增长</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>2024/Q4</td>
            <td>4.05亿</td>
            <td>+31.34%</td>
        </tr>
        <tr>
            <td>2024/Q3</td>
            <td>3.26亿</td>
            <td>+23.57%</td>
        </tr>
        <!-- 更多数据行 -->
    </tbody>
</table>

<h2>4.竞争格局分析</h2>
<p>市场竞争加剧，头部企业的市占率持续上升：</p>
<ul>
    <li><strong>市场集中度：</strong>CR5企业占据主导地位，市场份额进一步向头部聚集。</li>
    <li><strong>并购活动：</strong>Keybanc下调了UiPath的评级至“板块表现”，但其年度营收仍达到13.08亿美元，同比增长23.57%。<a href="https://m.10jqka.com.cn/20240531/c658386644.shtml">Keybanc下调评级UiPath评级为板块表现</a></li>
</ul>

<!-- 饼图 -->
<div style="max-width: 600px; margin: 0 auto;">
    <div class="chart-title">RPA行业市场占有率分布</div>
    <canvas id="pieChart"></canvas>
</div>
<p style="text-align: center;">数据来源：<a href="https://www.chic.org.cn/home/Index/detail1?id=1916">产业报告2024</a></p>

<script>
    // 折线图：RPA市场规模增长趋势
    const lineCtx = document.getElementById('lineChart').getContext('2d');
    new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: ['2023/Q1', '2023/Q2', '2023/Q3', '2023/Q4', '2024/Q1'],
            datasets: [{
                label: '市场规模（亿美元）',
                data: [2.5, 2.8, 3.1, 3.5, 4.0],
                borderColor: '#4c51bf',
                backgroundColor: 'rgba(76, 81, 191, 0.2)',
                borderWidth: 2,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true, position: 'bottom' },
                tooltip: { mode: 'index', intersect: false }
            },
            scales: {
                x: { grid: { color: "#fff" } },
                y: { beginAtZero: true, grid: { color: "#fff" } }
            }
        }
    });
    // 饼图：RPA行业市场占有率分布 - 使用更专业的颜色
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: ['UiPath', 'Automation Anywhere', 'Blue Prism', '其他'],
            datasets: [{
                data: [40, 30, 20, 10],
                backgroundColor: ['#4c51bf', '#667eea', '#67e8f9', '#7ddff8']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true, position: 'right' }
            }
        }
    });
</script>
</body>
</html>
备注：上面作为参考，文字部分太少了。使用Chart.js库的时候用本地的这种写法 <script src="http://60.165.238.132:9000/js_source/chart.js"></script>  
logo不要覆盖文本，在右上角。
直接生成html代码。

"""


# REPORT_PROMPT = """
# 任务：生成投研报告的内容和结构，以及图表信息和图表数据。以及图表的表述。然后和数据和政策相关的内容，给出数据和政策的来源，直接生成html代码。

# 任务概述：将搜索的网页内容，提取其中有用的部分，生成专业的报告内容，并且从内容中提取数据信息，选择性绘制各种图（柱状图、饼图、折线图等）和表的信息，且有图和表的描述。其中必须每个图表的数据都在下面有清晰的url来源。生成html代码。图的大小合理，版面设计合理。

# 角色：投研数据分析html代码生成师

# 举例：
# 报告的步骤和搜索的网页到内容：
#     'step': '1',
# 	'query': '对RPA行业进行宏观分析 收集并分析最近一年内RPA（Robotic Process Automation，机器人流程自动化）行业的发展动态，包括但不限于政策环境、技术创新趋势、市场需求变化、竞争格局等方面。重点关注政府出台的相关政策及其对行业的影响，技术突破及应用进展，市场规模的增长速度和驱动因素。',
# 	'search_result': '【搜索关键词】\n政策环境分析  \n需关注：各国政策文件原文、行业扶持/限制措施、税收优惠/监管变化。  \n关键词：RPA 政策影响 2024\n政府 RPA 行业规范 2024  \n技术创新趋势分析  \n需关注：头部企业技术白皮书、专利数据库、学术会议成果。  \n关键词：RPA 技术突破 2024\n流程挖掘技术进展 2024  \n市场需求变化分析  \n需关注：第三方机构市场规模报告、典型行业应用案例、投融资数据。  \n关键词：RPA 市场规模 驱动因素 2024\nRPA 行业应用增长 2024  \n竞争格局分析  \n需关注：CR5市占率变化、战略合作/并购事件、新兴区域市场参与者。  \n关键词：RPA 竞争格局 2024\nRPA 企业并购 2024\n【标题】: 2024企业财税政策变化与影响分析-20240708094259.pptx-原创力文档\n【site】:搜索引擎-原创力文档\n【链接】: https://m.book118.com/html/2024/0708/7146041123006131.shtm\n【内容】: 文档名称: 2024企业财税政策变化与影响分析.pptx 格式:pptx 大小:1.49MB 总页数:34 2024企业财税政策变化与影响分析;目录;01;2024年财税政策主要变化;政策变化的具体内容;02;企业税负的变化分析;企业盈利能力分析;企业现金流的影响;企业投资决策的影响;03;企业成本结构的变化;企业生产计划的影响;企业市场策略的影响\n【标题】: 2024年行业政策解读与应对报告-20240608081958.pptx-原创力文档\n【site】:搜索引擎-原创力文档\n【链接】: https://m.book118.com/html/2024/0608/7061111160006116.shtm\n【内容】: 2024年行业政策解读与应对报告 制作人：来日方长时 间：XX年X月目录第1章 2024年行业政策解读第2章 行业政策应对策略第3章 行业政策应对案例分析第4章 应对行业政策的建议01 2024年行业政策解读 引言2024年行业政策解读的重要性在于，它能够帮助我们理解和预测政策变化，从而做出更合适的决策。行业政策对企业和个人的影响是全方位的，从市场准入到税收优惠，都可能成为影响决策的关键因素。本报告的目标是，通过对2024年行业政策的深入解读，为企业和个人提供应对策略，把握行业发展趋势。2024年行业政策总体趋势预计政策将更加严格，对行业监管将加强政策紧缩预计行业将出现整合，优势企业将更加突出行业整合政策鼓励技术创新，推动行业发展技术创新环保政策将更加严格，绿色发展成为趋势绿色发展 主要行业政策解读2024年主要行业政策包括环保政策、税收政策、产业政策等。环保政策将更加严格，税收政策可能对企业产生较大影响，产业政策将推动行业结构调整。对这些政策的解读和分析，有助于我们更好地理解政策背后的意图，从而做出更合适的应对策略。行业政策对企业的影响政策变化可能影响企业的市场准入市场准入税收政策变化可能对企业产生较大影响税收优惠政策可能对某些产业给予支持，从而影响企业竞争力产业支持环保政策将更加严格，企业需要加大环保投入环保要求02 行业政策应对策略 引言行业政策应对策略的重要性在于，它能够帮助企业和个人在政策变化中找到应对之道，从而减少政策风险，把握发展机遇。\n【标题】: 产业报告2024丨政策篇:三、国外政策;四、智慧供热实施要求和标准\n【site】:搜索引擎-www.chic.org.cn\n【链接】: https://www.chic.org.cn/home/Index/detail1?id=1916\n【标题】: 2024企业财税政策变化与影响分析-20240708094259.pptx-原创力文档\n【site】:搜索引擎-原创力文档\n【链接】: https://m.book118.com/html/2024/0708/7146041123006131.shtm\n【内容】: 文档名称: 2024企业财税政策变化与影响分析.pptx 格式:pptx 大小:1.49MB 总页数:34 2024企业财税政策变化与影响分析;目录;01;2024年财税政策主要变化;政策变化的具体内容;02;企业税负的变化分析;企业盈利能力分析;企业现金流的影响;企业投资决策的影响;03;企业成本结构的变化;企业生产计划的影响;企业市场策略的影响\n【标题】: 2024年行业政策解读与应对报告-20240608081958.pptx-原创力文档\n【site】:搜索引擎-原创力文档\n【链接】: https://m.book118.com/html/2024/0608/7061111160006116.shtm\n【内容】: 2024年行业政策解读与应对报告 制作人：来日方长时 间：XX年X月目录第1章 2024年行业政策解读第2章 行业政策应对策略第3章 行业政策应对案例分析第4章 应对行业政策的建议01 2024年行业政策解读 引言2024年行业政策解读的重要性在于，它能够帮助我们理解和预测政策变化，从而做出更合适的决策。行业政策对企业和个人的影响是全方位的，从市场准入到税收优惠，都可能成为影响决策的关键因素。本报告的目标是，通过对2024年行业政策的深入解读，为企业和个人提供应对策略，把握行业发展趋势。2024年行业政策总体趋势预计政策将更加严格，对行业监管将加强政策紧缩预计行业将出现整合，优势企业将更加突出行业整合政策鼓励技术创新，推动行业发展技术创新环保政策将更加严格，绿色发展成为趋势绿色发展 主要行业政策解读2024年主要行业政策包括环保政策、税收政策、产业政策等。环保政策将更加严格，税收政策可能对企业产生较大影响，产业政策将推动行业结构调整。对这些政策的解读和分析，有助于我们更好地理解政策背后的意图，从而做出更合适的应对策略。行业政策对企业的影响政策变化可能影响企业的市场准入市场准入税收政策变化可能对企业产生较大影响税收优惠政策可能对某些产业给予支持，从而影响企业竞争力产业支持环保政策将更加严格，企业需要加大环保投入环保要求02 行业政策应对策略 引言行业政策应对策略的重要性在于，它能够帮助企业和个人在政策变化中找到应对之道，从而减少政策风险，把握发展机遇。\n【标题】: UiPath财报日期，财务报告和业绩会 - 富途牛牛\n【site】:搜索引擎-富途牛牛官网\n【链接】: https://www.futunn.com/stock/PATH-US/financial/earnings\n【内容】: PATHUiPath收盘价 04/12 16:00 (美东)20.710-0.600 -2.82%总市值 117.84亿市盈率TTM -129437最高价21.170最低价20.590成交量560.32万股今开21.100昨收21.310成交额1.17亿换手率1.24% \n市盈率(静) \n亏损 \n总股本 \n5.69亿 \n52周最高 \n27.870 \n市净率 \n5.85 \n流通值 \n93.84亿 \n52周最低 \n12.375 \n股息TTM \n流通股 \n4.53亿 \n历史最高 \n90.000 \n股息率TTM \n振幅2.72% \n历史最低 \n10.396 \n平均价 \n20.816 \n每手 \n1股 \n盘后 20.750 +0.040 +0.19% \n19:52 ET \nUiPath关键统计数据 \nUiPath财报日历 \n单位：美元 \n周期 \n2024财年Q4 财报 \n2024/03/13 \n分析师评级 \n买入 \n2024/04/08 \n营收(同比) \n4.05亿 \n+31.34% \n每股收益(同比) \n0.06 \n+220.00% \nUiPath财务预测 \n营收 \n每股收益 \n息税前利润 \n一共18位分析师对营收做出预测。预测值来源于标普，真实值来源于 利润表 \n货币单位: 美元 \n2024/Q2 \n2024/Q3 \n2024/Q4 \n2025/Q1 \n2025/Q2 \n2.873亿3.259亿4.053亿 \n2.821亿 \n3.156亿 \n3.837亿 \n3.329亿 \n3.423亿 \n真实值 \n预测值 \n日期 周期 营业收入/预测值 业绩会 -- 2025/Q2 -- / 3.423亿 -- -- 2025/Q1 -- / 3.329亿 -- 2024/03/13 2024/Q4 4.053亿 / 3.837亿 -- 2023/11/30 2024/Q3 3.259亿 / 3.156亿 -- 2023/09/06 2024/Q2 2.873亿 / 2.821亿 -- 2023/05/24 2024/Q1 2.896亿 / 2.712亿 -- 2023/03/15 2023/Q4 3.085亿 / 2.787亿 -- 2022/12/01 2023/Q3 2.627亿 / 2.559亿 -- 2022/09/06 2023/Q2 2.422亿 / 2.307亿 -- 2022/06/01 2023/Q1 2.451亿 / 2.253亿 -- \nUiPath财务报告 \nUiPath |10-K：年度报表 \n03/28 05:31 \nUiPath：2024财年三季报 \n2023/12/05 06:29 \nUiPath |10-Q：2024财年二季报 \n2023/09/08 05:01 \nUiPath |10-Q：2024财年一季报 \n2023/06/03 05:30\n【标题】: Keybanc下调评级UiPath评级为板块表现-同花顺财经\n【site】:搜索引擎-同花顺财经\n【链接】: https://m.10jqka.com.cn/20240531/c658386644.shtml\n【内容】: UiPath于3月27日发布2024年年报，公司截至2024年1月31日，营业收入13.08亿美元，同比23.57%，净利润-8988.30万美元，Keybanc下调评级UiPath评级为板块表现\n

# 参考html风格：
# ; /* 标题颜色设为蓝色 */#170da3，/* 副标题颜色设为橙色 */#ed9528
# 只用参考颜色。

# html参考：
# <!DOCTYPE html>
# <html lang="zh-CN">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>一、RPA行业宏观分析报告</title>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             line-height: 1.6;
#             margin: 20px;
#         }
#         h1, h2, h3 {
#             color: #333;
#         }
#         table {
#             width: 100%;
#             border-collapse: collapse;
#             margin: 20px 0;
#         }
#         table, th, td {
#             border: 1px solid #ddd;
#         }
#         th, td {
#             padding: 8px;
#             text-align: left;
#         }
#         th {
#             background-color: #f4f4f4;
#         }
#         canvas {
#             width: 100% !important; /* 确保canvas宽度适应容器 */
#             height: auto !important; /* 自动调整高度 */
#             margin: 20px 0;
#         }
#         a {
#             color: #007BFF;
#             text-decoration: none;
#         }
#         a:hover {
#             text-decoration: underline;
#         }
#     </style>
#     <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
# </head>
# <body>

# <h1>一、RPA行业宏观分析报告（截至2025年4月）</h1>

# <h2>1.政策环境分析</h2>
# <p>各国政府出台多项政策鼓励RPA技术的发展，特别是在财税管理和数字化转型领域。</p>
# <ul>
#     <li><strong>政策支持：</strong>企业税负的变化和税收优惠政策对RPA的应用产生了积极影响。<a href="https://m.book118.com/html/2024/0708/7146041123006131.shtm">2024企业财税政策变化与影响分析</a></li>
#     <li><strong>行业规范：</strong>环保政策和产业政策的调整对企业市场准入和技术投入提出了更高要求。<a href="https://m.book118.com/html/2024/0608/7061111160006116.shtm">2024年行业政策解读与应对报告</a></li>
# </ul>

# <h2>2.技术创新趋势</h2>
# <p>技术创新是RPA行业发展的核心驱动力。</p>
# <ul>
#     <li><strong>技术突破：</strong>流程挖掘技术和AI能力的融合成为行业热点。<a href="https://www.futunn.com/stock/PATH-US/financial/earnings">UiPath财报显示其2024财年第四季度营收增长至4.05亿美元，同比增长31.34%</a>。</li>
# </ul>

# <div style="max-width: 600px; margin: 0 auto;">
#     <canvas id="lineChart"></canvas>
# </div>
# <p style="text-align: center;">数据来源：<a href="https://www.chic.org.cn/home/Index/detail1?id=1916">产业报告2024</a></p>

# <h2>3.市场需求变化</h2>
# <p>市场需求的增长主要受以下因素驱动：</p>
# <ul>
#     <li><strong>市场规模：</strong>第三方机构数据显示，RPA市场规模保持高速增长。<a href="https://www.futunn.com/stock/PATH-US/financial/earnings">UiPath财报预测，2025年Q1的营收将达到3.329亿美元</a>。</li>
# </ul>

# <table>
#     <thead>
#         <tr>
#             <th>周期</th>
#             <th>营业收入</th>
#             <th>同比增长</th>
#         </tr>
#     </thead>
#     <tbody>
#         <tr>
#             <td>2024/Q4</td>
#             <td>4.05亿</td>
#             <td>+31.34%</td>
#         </tr>
#         <tr>
#             <td>2024/Q3</td>
#             <td>3.26亿</td>
#             <td>+23.57%</td>
#         </tr>
#         <!-- 更多数据行 -->
#     </tbody>
# </table>

# <h2>4.竞争格局分析</h2>
# <p>市场竞争加剧，头部企业的市占率持续上升：</p>
# <ul>
#     <li><strong>市场集中度：</strong>CR5企业占据主导地位，市场份额进一步向头部聚集。</li>
#     <li><strong>并购活动：</strong>Keybanc下调了UiPath的评级至“板块表现”，但其年度营收仍达到13.08亿美元，同比增长23.57%。<a href="https://m.10jqka.com.cn/20240531/c658386644.shtml">Keybanc下调评级UiPath评级为板块表现</a></li>
# </ul>

# <div style="max-width: 600px; margin: 0 auto;">
#     <canvas id="pieChart"></canvas>
# </div>
# <p style="text-align: center;">数据来源：<a href="https://www.chic.org.cn/home/Index/detail1?id=1916">产业报告2024</a></p>

# <script>
#     // 折线图：RPA市场规模增长趋势
#     const lineCtx = document.getElementById('lineChart').getContext('2d');
#     new Chart(lineCtx, {
#         type: 'line',
#         data: {
#             labels: ['2023/Q1', '2023/Q2', '2023/Q3', '2023/Q4', '2024/Q1'],
#             datasets: [{
#                 label: '市场规模（亿美元）',
#                 data: [2.5, 2.8, 3.1, 3.5, 4.0],
#                 borderColor: '#4c51bf',
#                 backgroundColor: 'rgba(76, 81, 191, 0.2)',
#                 borderWidth: 2,
#                 fill: true
#             }]
#         },
#         options: {
#             responsive: true,
#             plugins: {
#                 legend: { display: true, position: 'bottom' },
#                 tooltip: { mode: 'index', intersect: false }
#             },
#             scales: {
#                 x: { grid: { color: "#fff" } },
#                 y: { beginAtZero: true, grid: { color: "#fff" } }
#             }
#         }
#     });
#     // 饼图：RPA行业市场占有率分布 - 使用更专业的颜色
#     const pieCtx = document.getElementById('pieChart').getContext('2d');
#     new Chart(pieCtx, {
#         type: 'pie',
#         data: {
#             labels: ['UiPath', 'Automation Anywhere', 'Blue Prism', '其他'],
#             datasets: [{
#                 data: [40, 30, 20, 10],
#                 backgroundColor: ['#4c51bf', '#667eea', '#67e8f9', '#7ddff8']
#             }]
#         },
#         options: {
#             responsive: true,
#             plugins: {
#                 legend: { display: true, position: 'right' }
#             }
#         }
#     });
# </script>
# </body>
# </html>
# """

# GENERATE_PROMPT_TEST = """
# 任务：投研报告HTML设计与生成，其中字数超过2000字，来源要根据参考内容的数据，关注数据类型、分析角度，其中数据必须要包括关键的图和表的html数据，直接生成html代码。

# 任务概述：
# 为专业投研报告编写设计精美的HTML代码。该HTML文档需包含封面页、目录页、内容页及尾页，并确保整体风格统一。

# 角色：HTML代码设计师
# 角色职责：
# 根据提供的文本内容，设计并编写高质量的HTML代码。确保最终HTML文档适用于高效地转换为PDF格式，保持视觉效果和内容结构的完整性。

# 要求：
# 封面页：参考的html代码：
# <!DOCTYPE html>
# <html lang="zh-CN">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>实在Agent投研分析报告</title>
#     <style>
#         body {
#             margin: 0;
#             font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; /* 使用系统字体 */
#             background-image: url('http://60.165.238.132:9000/images_report/report-cover.png');
#             background-size: cover;
#             background-position: center;
#             background-repeat: no-repeat;
#             color: #000; /* 文字颜色改为黑色 */
#             display: flex;
#             flex-direction: column;
#             justify-content: space-between; /* 调整为上下分布 */
#             align-items: center;
#             height: 100vh;
#             overflow: hidden;
#         }
#         .header {
#             display: flex;
#             justify-content: flex-end; /* 只保留右侧元素，所以改为向右侧对齐 */
#             width: 90%;
#             margin-top: 40px; /* 将头部内容稍微下移更多 */
#         }
#         .header-right img {
#             width: 200px; /* 进一步放大Logo */
#             height: 50px;
#         }
#         .content {
#             text-align: center;
#             margin-bottom: 60px; /* 增加底部边距使内容区域更靠下 */
#         }
#         .title {
#             font-size: 48px;
#             font-weight: bold;
#             color: #170da3; /* 标题颜色设为蓝色 */
#             margin-top: 100px; /* 增加上方间距 */
#             margin-bottom: 20px;
#         }
#         .subtitle {
#             font-size: 32px;
#             color: #ed9528; /* 副标题颜色设为橙色 */
#             margin-bottom: 150px; /* 增加与下面内容的距离 */
#         }
#         .company {
#             font-size: 24px;
#             color: #444; /* 公司名称颜色稍浅 */
#             margin-bottom: 20px;
#         }
#         .locations {
#             font-size: 18px;
#             color: #666; /* 地点颜色灰色 */
#             margin-bottom: 20px;
#         }
#         .disclaimer {
#             font-size: 14px;
#             color: #777; /* 免责声明颜色更浅 */
#             margin-bottom: 100px;
#         }
#         .date {
#             position: absolute;
#             bottom: 10px;
#             left: 20px;
#             font-size: 16px;
#             color: #666; /* 日期颜色灰色 */
#         }
#     </style>
# </head>
# <body>
#     <!-- Header Section -->
#     <div class="header">
#         <div class="header-right">
#             <img src="http://60.165.238.132:9000/images_report/ai-indeed-logo.jpg" alt="实在智能Logo">
#         </div>
#     </div>

#     <!-- Content Section -->
#     <div class="content">
#         <div class="title">2024年微电子行业投研报告</div>
#         <div class="subtitle">实在Agent投研分析团队</div>
#         <div class="company">浙江实在智能科技有限公司</div>
#         <div class="locations">杭州丨北京丨上海丨深圳丨广州丨成都丨济南丨东京</div>
#         <div class="disclaimer">请仔细阅读在本报告尾部的重要法律声明</div>
#     </div>

#     <!-- Date -->
#     <div class="date">2025年4月12日</div>
# </body>
# </html>
# 备注：1.xx投研报告要根据具体内容更改。2.日期要根据输入信息填写
# 目录页：
# 自动生成基于文档内容的目录，单独一页展示。
# 清晰列出各部分内容及其对应的页码，便于读者导航。
# 尾页：
# 单独成为一页.
# 标题：实在agent免责声明（大号字体，蓝色）
#         • 本报告仅供本公司签约客户使用。本公司不会因接收人收到或者经由其他渠道转发收到本报告而直接视其为本公司客户。
#         • 本报告基于本公司研究所及其研究人员认为的已经公开的资料或者研究人员的实地调研资料，但本公司对该等信息的准确性、完整性或可靠性不作任何保证。本报告所载资料、意见以及推测仅于本报告发布当日的判断，且这种判断受到研究方法、研究依据等多方面的制约。在不同时期，本公司可发出与本报告所载资料、意见及预测不一致的报告。本公司不保证本报告所含信息始终保持在最新状态。同时，本公司对本报告所含信息可在不发出通知的情形下做出修改，投资者需自行关注相应更新或修改。
#         • 在任何情况下，本报告仅提供给签约客户参考使用，任何信息或所表述的意见绝不构成对任何人的投资建议。市场有风险，投资需谨慎。投资者不应将本报告视为做出投资决策的唯一参考因素，亦不应认为本报告可以取代自己的判断。在任何情况下，本报告均未考虑到个别客户的特殊投资目标、财务状况或需求，不能作为客户进行买卖、认购证券或者其他金融工具的保证或邀请。在任何情况下，本公司、本公司员工或者其他关联方均不承诺投资者一定获利，不与投资者分享投资收益，也不对任何人因使用本报告而导致的任何可能损失负有任何责任。投资者因使用本公司研究报告做出的任何投资决策均是独立行为，与本公司、本公司员工及其他关联方无关。
#         • 本公司建立起信息隔离墙制度、跨墙制度来规范管理跨部门、跨关联机构之间的信息流动。务请投资者注意，在法律许可的前提下，本公司及其所属关联机构可能会持有报告中提到的公司所发行的证券或期权并进行证券或期权交易，也可能为这些公司提供或者争取提供投资银行、财务顾问或者金融产品等相关服务。在法律许可的前提下，本公司的董事、高级职员或员工可能担任本报告所提到的公司的董事。本公司及其所属关联机构或个人可能在本报告公开发布之前已经使用或了解其中的信息。
#         • 所有报告版权均归本公司所有。未经本公司事先书面授权，任何机构或个人不得以任何形式复制、转发或公开传播本报告的全部或部分内容，如需引用、刊发或转载本报告，需注明出处为实在Agent，且不得对本报告进行任何有悖原意的引用、删节和修改。
# 联系邮箱：contact@i-i.com
# 联系电话：4001399089
# 联系地址：中国杭州南湖未来科学园
# 内容页：
# 统一的格式和风格应用于整个文档，确保阅读体验的一致性。
# 注意分页逻辑，避免关键信息在页面边界被截断，确保转换为PDF时的内容完整性。
# 输出要求:
# 提供一个完整的HTML文件，整合封面页、目录页、内容页和尾页，确保所有部分过渡自然，布局协调统一。
# HTML代码需考虑后续的PDF转换流程，确保生成的PDF文件保留原始设计的所有细节和格式。
# 请根据以上描述精心设计HTML代码，确保最终投研报告不仅在视觉上吸引人，而且在内容呈现上也达到专业标准。
# 美观要求：将html格式中加入彩色和渲染的效果，每一页的页眉html代码加入实在智能的图片，但是不要太大，不要覆盖文本内容，链接地址：http://60.165.238.132:9000/images_report/ai-indeed-logo.jpg
# 直接生成html代码，不要有其他内容。整个投研报告风的框架要明确。
# 注意事项：首页、目录页、尾页要单独成为一页，页眉部分不要覆盖正文，实在智能logo在右上角，首页不用有页眉。不要有阴影部分，每一页加点ppt模板内容。其中一级标题和二级标题有颜色区分，标题加粗。一级标题前设置一个标签图标，二级标题字是斜体。
# 其中内容页的部分要先分析，分析的模版可以参考以下内容：
# 2024 年度，公司实现营业收入 27.60 亿元，同比增长11.23%，归属于上市公司股东的净利润 1.96 亿元，同比增长61.44%。公司实现连续六年营收增长，自 2019 年起营收复合增长率达到 30.49%。并且走出 2022 年的行业低谷，归母净利实现连续两年超 60%增长。根据公司年报，公司营销策略、市场需求的精准把握叠加产能释放，以高光效照明、车用照明、背光、Mini 直显等为代表的高端产品产销两旺，产能利用率、产销率保持一贯高位，主营业务稳步增长。备注：这种风格是有分析内容的，不是简单把内容总结。先分析数据，然后总结，然后分析。
# 图片和表格内容可以根据不同数据选择对比图，对比表，折线图，饼图，柱状图，分析图，但是数据必须有数据来源。整体图片的风格严谨严肃，是研究报告的风格。
# """



# # 
# MERGE_HTML_PROMPT = """
# 任务：现在你会收到多个html的内容，现在需要你把单个html内容合并成一个html的内容，注意要有目录页，封面页，内容页和尾页。每一页都要有实在智能的logo在右上角，目录页和尾页要单独成为一页，首页不用有页眉。每一页加点ppt模板内容。其中一级标题和二级标题有颜色区分，标题加粗。二级标题字是斜体。

# 封面页：参考的html代码：
# <!DOCTYPE html>
# <html lang="zh-CN">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>实在Agent投研分析报告</title>
#     <style>
#         body {
#             margin: 0;
#             font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; /* 使用系统字体 */
#             background-image: url('http://60.165.238.132:9000/images_report/report-cover.png');
#             background-size: cover;
#             background-position: center;
#             background-repeat: no-repeat;
#             color: #000; /* 文字颜色改为黑色 */
#             display: flex;
#             flex-direction: column;
#             justify-content: space-between; /* 调整为上下分布 */
#             align-items: center;
#             height: 100vh;
#             overflow: hidden;
#         }
#         .header {
#             display: flex;
#             justify-content: flex-end; /* 只保留右侧元素，所以改为向右侧对齐 */
#             width: 90%;
#             margin-top: 40px; /* 将头部内容稍微下移更多 */
#         }
#         .header-right img {
#             width: 200px; /* 进一步放大Logo */
#             height: 50px;
#         }
#         .content {
#             text-align: center;
#             margin-bottom: 60px; /* 增加底部边距使内容区域更靠下 */
#         }
#         .title {
#             font-size: 48px;
#             font-weight: bold;
#             color: #170da3; /* 标题颜色设为蓝色 */
#             margin-top: 100px; /* 增加上方间距 */
#             margin-bottom: 20px;
#         }
#         .subtitle {
#             font-size: 32px;
#             color: #ed9528; /* 副标题颜色设为橙色 */
#             margin-bottom: 150px; /* 增加与下面内容的距离 */
#         }
#         .company {
#             font-size: 24px;
#             color: #444; /* 公司名称颜色稍浅 */
#             margin-bottom: 20px;
#         }
#         .locations {
#             font-size: 18px;
#             color: #666; /* 地点颜色灰色 */
#             margin-bottom: 20px;
#         }
#         .disclaimer {
#             font-size: 14px;
#             color: #777; /* 免责声明颜色更浅 */
#             margin-bottom: 100px;
#         }
#         .date {
#             position: absolute;
#             bottom: 10px;
#             left: 20px;
#             font-size: 16px;
#             color: #666; /* 日期颜色灰色 */
#         }
#     </style>
# </head>
# <body>
#     <!-- Header Section -->
#     <div class="header">
#         <div class="header-right">
#             <img src="http://60.165.238.132:9000/images_report/ai-indeed-logo.jpg" alt="实在智能Logo">
#         </div>
#     </div>

#     <!-- Content Section -->
#     <div class="content">
#         <div class="title">2024年微电子行业投研报告</div>
#         <div class="subtitle">实在Agent投研分析团队</div>
#         <div class="company">浙江实在智能科技有限公司</div>
#         <div class="locations">杭州丨北京丨上海丨深圳丨广州丨成都丨济南丨东京</div>
#         <div class="disclaimer">请仔细阅读在本报告尾部的重要法律声明</div>
#     </div>

#     <!-- Date -->
#     <div class="date">2025年4月12日</div>
# </body>
# </html>
# 备注：1.xx投研报告要根据具体内容更改。2.日期要根据输入信息填写
# 目录页：
# 自动生成基于文档内容的目录，单独一页展示。
# 清晰列出各部分内容及其对应的页码，便于读者导航。
# 尾页：
# 单独成为一页.
# 标题：实在agent免责声明（大号字体，蓝色）
#         • 本报告仅供本公司签约客户使用。本公司不会因接收人收到或者经由其他渠道转发收到本报告而直接视其为本公司客户。
#         • 本报告基于本公司研究所及其研究人员认为的已经公开的资料或者研究人员的实地调研资料，但本公司对该等信息的准确性、完整性或可靠性不作任何保证。本报告所载资料、意见以及推测仅于本报告发布当日的判断，且这种判断受到研究方法、研究依据等多方面的制约。在不同时期，本公司可发出与本报告所载资料、意见及预测不一致的报告。本公司不保证本报告所含信息始终保持在最新状态。同时，本公司对本报告所含信息可在不发出通知的情形下做出修改，投资者需自行关注相应更新或修改。
#         • 在任何情况下，本报告仅提供给签约客户参考使用，任何信息或所表述的意见绝不构成对任何人的投资建议。市场有风险，投资需谨慎。投资者不应将本报告视为做出投资决策的唯一参考因素，亦不应认为本报告可以取代自己的判断。在任何情况下，本报告均未考虑到个别客户的特殊投资目标、财务状况或需求，不能作为客户进行买卖、认购证券或者其他金融工具的保证或邀请。在任何情况下，本公司、本公司员工或者其他关联方均不承诺投资者一定获利，不与投资者分享投资收益，也不对任何人因使用本报告而导致的任何可能损失负有任何责任。投资者因使用本公司研究报告做出的任何投资决策均是独立行为，与本公司、本公司员工及其他关联方无关。
#         • 本公司建立起信息隔离墙制度、跨墙制度来规范管理跨部门、跨关联机构之间的信息流动。务请投资者注意，在法律许可的前提下，本公司及其所属关联机构可能会持有报告中提到的公司所发行的证券或期权并进行证券或期权交易，也可能为这些公司提供或者争取提供投资银行、财务顾问或者金融产品等相关服务。在法律许可的前提下，本公司的董事、高级职员或员工可能担任本报告所提到的公司的董事。本公司及其所属关联机构或个人可能在本报告公开发布之前已经使用或了解其中的信息。
#         • 所有报告版权均归本公司所有。未经本公司事先书面授权，任何机构或个人不得以任何形式复制、转发或公开传播本报告的全部或部分内容，如需引用、刊发或转载本报告，需注明出处为实在Agent，且不得对本报告进行任何有悖原意的引用、删节和修改。
# 联系邮箱：contact@i-i.com
# 联系电话：4001399089
# 联系地址：中国杭州南湖未来科学园
# 目录页：整合所有单个html内容，生成对应的目录，目录的字体风格和大小和标题一致，美观整洁。
# 内容页：保留所有内容，包括文字部分和图表部分，包括所有来源。
# """
# # 
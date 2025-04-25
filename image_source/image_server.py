from flask import Flask, send_from_directory, render_template

app = Flask(__name__)

# 配置图片文件夹路径
IMAGES_FOLDER = 'images_report'

# 配置 HTML 文件夹路径
HTML_FOLDER = 'report_pdf_page'

JS_FOLDER = 'js_source'

@app.route('/')
def index():
    return '''
    <h1>Welcome to the Image Server</h1>
    <p>Access your images via URLs like: <a href="/images_report/image1.jpg">/images_report/image1.jpg</a></p>
    '''

# 提供图片访问的路由
@app.route('/images_report/<path:filename>')
def serve_image(filename):
    # 使用 send_from_directory 提供文件访问
    return send_from_directory(IMAGES_FOLDER, filename)

# 提供 HTML 文件访问的路由
@app.route('/report_pdf_page/<path:filename>')
def serve_html_report_pdf_page(filename):
    # 使用 send_from_directory 提供 HTML 文件访问
    return send_from_directory(HTML_FOLDER, filename)


# 提供 HTML 文件访问的路由
@app.route('/js_source/<path:filename>')
def serve_html_js_source(filename):
    # 使用 send_from_directory 提供 HTML 文件访问
    return send_from_directory(JS_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
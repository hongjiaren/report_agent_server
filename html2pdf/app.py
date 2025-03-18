from flask import Flask, request, jsonify, send_from_directory
from weasyprint import HTML
import os

app = Flask(__name__)

# 设置存储PDF文件的目录
PDF_DIR = os.path.join(os.getcwd(), "pdfs")
os.makedirs(PDF_DIR, exist_ok=True)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    html_content = data.get('html_content')
    if not html_content:
        return jsonify({"error": "No HTML content provided"}), 400
    
    # 使用WeasyPrint将HTML转换为PDF
    pdf_file_path = os.path.join(PDF_DIR, f"{data.get('filename', 'output')}.pdf")
    HTML(string=html_content).write_pdf(pdf_file_path)
    
    # 返回PDF文件的URL（Web服务器配置正确，可以访问这个路径）
    pdf_url = f"/pdfs/{os.path.basename(pdf_file_path)}"
    return jsonify({"pdf_url": pdf_url})

@app.route('/pdfs/<filename>')
def serve_pdf(filename):
    return send_from_directory(PDF_DIR, filename)

if __name__ == '__main__':
    HOST = '0.0.0.0'  # 设置为你想要绑定的IP地址
    PORT = 5535         # 设置为你想要使用的端口号
    
    print(f"正在启动html生成pdf应用于: http://{HOST}:{PORT}")
    app.run(host=HOST, port=PORT)
    print("html生成pdf应用已停止...")

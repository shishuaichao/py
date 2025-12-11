

# 导入其他文件的函数（核心：引用跨文件功能）
from db_operation import get_all_teachers, add_teacher

from flask import Flask, jsonify, request
from flask_cors import CORS  # 核心：解决跨域

app = Flask(__name__)
CORS(app)  # 允许前端跨域请求

# 查
@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    res = get_all_teachers()
    return jsonify(res)
# 增
@app.route('/api/add_teacher', methods=['POST'])
def add():
    d = request.json
    print(d)
    add_teacher(d)
    return jsonify({"msg":"成功"})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)  # 端口5000


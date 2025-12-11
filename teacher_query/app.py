

# 导入其他文件的函数（核心：引用跨文件功能）
from db_operation import get_all_teachers

from flask import Flask, jsonify
from flask_cors import CORS  # 核心：解决跨域

app = Flask(__name__)
CORS(app)  # 允许前端跨域请求

# 示例接口（供Vue调用）
@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    # 这里写查询数据库逻辑，返回JSON即可
    # res = get_all_teachers()
    # return jsonify(res)
    return jsonify([{'id':1, 'name':'张三', 'subject':'数学'}])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)  # 端口5000


# 导入其他文件的函数（核心：引用跨文件功能）
from db_operation import get_all_teachers, add_teacher
from flask import Flask, jsonify, request
from flask_cors import CORS  # 核心：解决跨域
from wechat.ws_handler import socketio  # 导入抽离的socketio实例
from wechat.operate import get_all_wechats

app = Flask(__name__)
# 核心作用：为Flask应用设置加密密钥，用于cookie/会话/WS鉴权等加密
app.config['SECRET_KEY'] = 'secret'
CORS(app)  # 允许前端跨域请求

# 绑定socketio到app
socketio.init_app(app, cors_allowed_origins="*")

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

@app.route('/api/wechats', methods=['GET'])
def get_chats():
    res = get_all_wechats()
    return jsonify(res)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)


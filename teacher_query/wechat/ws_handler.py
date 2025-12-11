from flask_socketio import SocketIO, send
import time
from wechat.operate import get_all_wechats, add_wechat
import datetime

# 初始化socketio（空初始化，后续在app.py中绑定app）
socketio = SocketIO()

# WebSocket消息处理函数
@socketio.on('message')
def handle_socket_msg(msg):
    """WebSocket自动回复逻辑"""
    print(f'WS收到：{msg}')
    add_wechat({ "msg": msg, "type": "q", "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") })
    time.sleep(1)
    reply = f'{msg}'
    add_wechat({ "msg": msg, "type": "a", "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") })
    send(reply)
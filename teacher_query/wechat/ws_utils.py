
from flask_socketio import emit
from wechat.operate import add_chat
import datetime

# 普通消息处理函数
def treat_socket_message(msgObj):
    # print(f'WS收到：{msgObj}')
    msgData = { 
        'id': msgObj['id'],
        'nickname': msgObj['nickname'],
        "content": msgObj['content'], 
        "avatar": msgObj['avatar'], 
        "type": "message", 
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    }
    add_chat(msgData)
    emit('message', msgData, broadcast=True)

# 系统消息处理函数
def treat_socket_system_msg(msgObj, room=None, broadcast=True):
    # print(f'WS收到：{msgObj}')
    msgData = { 
        'id': msgObj['id'],
        'nickname': msgObj['nickname'],
        "content": msgObj['content'], 
        "type": "system_msg", 
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    }
    add_chat(msgData)
    emit('system_msg', msgData, broadcast=True)

from flask_socketio import SocketIO, emit
import time
from wechat.operate import get_all_wechats, add_wechat
import datetime
from flask import Flask, jsonify, request, session

# 初始化socketio（空初始化，后续在app.py中绑定app）
socketio = SocketIO()

# 存储在线用户：{sid: {nickname: str, room: str}}
online_users = {}
# 核心存储：{sid: 用户名}，全局字典
user_map = {}

# WebSocket消息处理函数
@socketio.on('message')
def handle_socket_msg(msgObj):
    print(f'WS收到：{msgObj}')
    msgData = { 
        'id': msgObj['id'],
        'nickname': msgObj['nickname'],
        "content": msgObj['content'], 
        "avatar": msgObj['avatar'], 
        "type": "message", 
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    }
    add_wechat(msgData)
    emit('message', msgData, broadcast=True)

# WebSocket消息处理函数
@socketio.on('system_msg')
def handle_socket_system_msg(msgObj):
    print(f'WS收到：{msgObj}')
    msgData = { 
        'id': msgObj['id'],
        'nickname': msgObj['nickname'],
        "content": msgObj['content'], 
        "type": "system_msg", 
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    }
    # add_wechat(msgData)
    emit('system_msg', msgData, broadcast=True)

# 处理客户端连接事件
@socketio.on('connect')
def handle_connect():
    """客户端连接成功时触发"""
    sid = request.sid  # 获取客户端唯一标识（flask-socketio 内置）
    # 初始化用户信息（默认昵称 + 未加入房间）
    print(f"sid: {sid}")

    online_users[sid] = {
        'nickname': f'访客{sid}',
        'room': None
    }
    print(f"✅ 客户端 {sid} 连接成功，默认昵称：{online_users[sid]['nickname']}")
    # 给当前客户端发送连接成功提示
    emit('connect_success', {
        'msg': '连接成功！',
        'nickname': online_users[sid]['nickname'],
        'online_count': len(online_users)
    })
    # 群发在线人数更新
    emit('online_count', len(online_users), broadcast=True)

# 8. Socket.IO 事件：客户端断开连接
@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in online_users:
        user_info = online_users[sid]
        # 移除用户
        del online_users[sid]
        # 群发离开通知（如果在房间内）
        if user_info['room']:
            emit('system_msg', {
                'msg': f'{user_info["nickname"]} 离开房间 {user_info["room"]}',
                'time': datetime.now().strftime('%H:%M:%S')
            }, room=user_info['room'])
        # 群发在线人数更新
        emit('online_count', len(online_users), broadcast=True)
        print(f"❌ 客户端 {sid}（{user_info['nickname']}）断开连接")

# 2. 核心：监听前端传过来的用户名并存储
@socketio.on('set_nickname')
def handle_set_nickname(userInfo):
    nickname = userInfo['nickname'].strip()
    sid = request.sid
    # 步骤1：验证用户名（非空、不重复，可选）
    if not nickname:
        emit('username_error', {'msg': '用户名不能为空！'})
        return
    if nickname in user_map.values():
        emit('username_error', {'msg': '用户名已被占用，请换一个！'})
        return
    # 步骤2：存储用户名（sid 作为键，确保唯一）
    user_map[sid] = nickname
    print(f"客户端 {sid} 设置用户名：{nickname}")
    # 步骤3：给当前客户端返回成功提示
    emit('username_success', {'msg': f'用户名设置成功：{nickname}'})
    # 步骤4：群发「新用户加入」通知（所有客户端可见）
    msgData = {
        'id': userInfo['id'],
        'nickname': nickname,
        'content': f'用户「{nickname}」已加入聊天室',
        'type': 'system_msg',
        'time': datetime.datetime.now().strftime('%H:%M:%S')
    }
    add_wechat(msgData)
    emit('system_msg', msgData, broadcast=True)  # 广播给所有客户端
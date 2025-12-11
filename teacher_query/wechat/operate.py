# 导入依赖 + 导入配置文件
import pymysql
from db_config import MYSQL_CONFIG  # 引用同目录的db_config.py中的配置

# db_operation.py 新增函数
def add_wechat(d):
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        # 执行插入SQL
        cursor.execute('INSERT INTO wechat (msg, type, time) VALUES (%s, %s, %s)', (d['msg'], d['type'], d['time']))
        conn.commit()  # 写操作必须commit
        print("新增聊天成功！")
    except Exception as e:
        conn.rollback()  # 出错回滚
        print(f"新增失败：{e}")
    finally:
        cursor.close()
        conn.close()
     
# 定义查询wechat表的函数（功能封装）
def get_all_wechats():
    """查询wechat表的所有数据"""
    try:
        # 1. 连接数据库（使用配置文件的参数）
        conn = pymysql.connect(**MYSQL_CONFIG)
        # 2. 创建游标（返回字典格式）
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 3. 执行查询
        cursor.execute('SELECT * FROM wechat')
        # 4. 获取结果
        wechats = cursor.fetchall()
        return wechats  # 返回查询结果
    except Exception as e:
        print(f"查询失败：{e}")
        return []
    finally:
        # 5. 关闭连接（确保资源释放）
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
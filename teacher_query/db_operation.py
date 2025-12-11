# 导入依赖 + 导入配置文件
import pymysql
from db_config import MYSQL_CONFIG  # 引用同目录的db_config.py中的配置

# 定义查询teacher表的函数（功能封装）
def get_all_teachers():
    """查询teacher表的所有数据"""
    try:
        # 1. 连接数据库（使用配置文件的参数）
        conn = pymysql.connect(**MYSQL_CONFIG)
        # 2. 创建游标（返回字典格式）
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 3. 执行查询
        cursor.execute('SELECT * FROM teacher')
        # 4. 获取结果
        teachers = cursor.fetchall()
        return teachers  # 返回查询结果
    except Exception as e:
        print(f"查询失败：{e}")
        return []
    finally:
        # 5. 关闭连接（确保资源释放）
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
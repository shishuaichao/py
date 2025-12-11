# 导入pymysql驱动
import pymysql

# ---------------------- 1. 配置本地MySQL连接参数（改这4行！） ----------------------
config = {
    'host': 'localhost',      # 本地数据库地址，固定
    'port': 3306,             # 你的端口，固定3306
    'user': 'root',           # 你的MySQL用户名（比如root）
    'password': 'rootroot',     # 你的MySQL密码（必填！）
    'database': 'school',     # teacher表所在的数据库名（必填！）
    'charset': 'utf8mb4'      # 避免中文乱码，固定
}

# ---------------------- 2. 核心逻辑：连接+查询+打印 ----------------------
try:
    # ① 建立数据库连接
    conn = pymysql.connect(**config)
    # ② 创建游标（用于执行SQL），设置返回字典格式（更易读）
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    # ③ 执行查询：取出teacher表所有内容
    cursor.execute('SELECT * FROM teacher')
    # ④ 获取所有查询结果
    all_teachers = cursor.fetchall()
    
    # ⑤ 打印结果（验证）
    print("teacher表所有数据：")
    for teacher in all_teachers:
        print(teacher)  # 字典格式，可按字段名取值（如teacher['name']）

finally:
    # ⑥ 关闭连接（避免资源泄露）
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
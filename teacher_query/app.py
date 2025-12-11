

# 导入其他文件的函数（核心：引用跨文件功能）
from db_operation import get_all_teachers

# 主程序逻辑
if __name__ == '__main__':
    # 调用其他文件的功能
    all_teachers = get_all_teachers()
    
    # 打印结果
    print("teacher表所有数据：")
    for teacher in all_teachers:
        print(teacher)
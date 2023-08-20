"""
@Description: 聊天室数据库模块，封装数据库相关功能
@Author: Pan Xiaofei
@Date: 2023-08-18 16:18:26
"""

import pymysql

from DB.properties import *


class MyDB(object):
    """
    @Description: 初始化数据库连接
    @Parameters: 
    @Return: 
    """
    def __init__(self):
        self.conn = pymysql.connect(
        # mysql服务器主机地址
        host = DB_HOST,
        # mysql服务器连接端口
        port = DB_PORT,
        # 用户名
        user = DB_USER,
        # 数据库名（若不选此参数则不指定具体数据库连接，我们可以使用use database来选择其它数据库）
        database = DB_DATABASE,
        # 用户密码
        password = DB_PASSWORD,
        # 编码格式
        charset = DB_CHARSET)

        # 使用cursor()函数创建一个游标对象
        self.cursor = self.conn.cursor()

    """
    @Description: 断开数据库连接，释放资源 
    @Parameters: 
    @Return: 
    """
    def dbClose(self):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()

    """
    @Description: 查询数据库并获取返回结果（数据库查操作）
    @Parameters: 
    @Return: 
    """
    def getItem(self, sql):
        # 使用execute()函数执行一条sql语句,创建一个名为`mydb`的数据库
        self.cursor.execute(sql)

        # 获取查询结果
        query_data = self.cursor.fetchone()
        if not query_data:
            return None
        
        # 获取数据库表字段名
        fileds = [filed[0] for filed in self.cursor.description]

        # 查询数据与字段名结合返回字典
        result_dict = dict(zip(fileds,query_data))
        return result_dict


# if __name__ == "__main__":
#     db = MyDB()
#     data = db.getItem(sql="select * from users where name='user1'")
#     print(data)
#     db.dbClose()
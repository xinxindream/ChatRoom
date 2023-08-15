"""
@Description: 服务器相关配置
@Author: Pan Xiaofei
@Date: 2023-08-14 17:52:46
"""

""" 服务器数据协议相关配置 """
REQUEST_LOGIN = '0001'  # 登录请求
REQUEST_CHAT = '0002'   # 聊天请求
RESPONSE_LOGIN_RESULT = '1001'  # 登录结果响应
RESPONSE_CHAT = '1002'  # 聊天响应
DELIMITER = '|'     # 自定义协议数据分隔符

""" 服务器基本信息配置 """
SERVER_IP = '127.0.0.1' # 服务器IP地址
SERVER_PORT = '3309'    # 服务器端口

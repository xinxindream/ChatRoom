"""
@Description: 自定义服务器套接字 
@Author: Pan Xiaofei
@Date: 2023-08-15 20:28:14
"""

import socket
from config import *

class myServerSocket(socket.socket):
    def __init__(self):
        # 等价于socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket = super(myServerSocket, self).__init__(socket.AF_INET,socket.SOCK_STREAM)

        # 绑定IP地址与端口
        self.bind((SERVER_IP, SERVER_PORT))

        # 监听客户端
        self.listen(128)
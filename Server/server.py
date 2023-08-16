"""
@Description: 服务器核心功能
@Author: Pan Xiaofei
@Date: 2023-08-15 20:13:44
"""

from myServerSocket import myServerSocket
from mySocketWrapper import mySocketWrapper

class Server(object):
    """
    @Description: 初始化服务器套接字
    @Parameters: 
    @Return: 
    """
    def __init__(self):
        self.server_socket = myServerSocket()

    """
    @Description: 开启服务器
    @Parameters: 
    @Return: 
    """
    def startup(self):
        # 获取客户端连接
        # 持续获取客户端连接（可获取多个客户端连接）
        while True:
            print("正在获取客户端连接~~~")
            client_socket, client_addr = self.server_socket.accept()
            print("已建立连接~~~")
            
            # 允许客户端与服务器多次交互
            while True: 
                # 收发信息，引入封装套接字
                ## 创建套接字对象
                my_client_socket = mySocketWrapper(client_socket)
                
                ## 收，解码
                print(my_client_socket.recvData())

                ## 发，编码
                msg = "你好！"
                my_client_socket.sendData(msg)

            client_socket.close()
            self.server_socket.close()


if __name__ == "__main__":
    Server().startup()
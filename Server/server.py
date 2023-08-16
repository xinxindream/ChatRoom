"""
@Description: 服务器核心功能
@Author: Pan Xiaofei
@Date: 2023-08-15 20:13:44
"""

from myServerSocket import myServerSocket

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
        print("正在获取客户端连接~~~")
        client_socket, client_addr = self.server_socket.accept()
        print("已建立连接~~~")
        
        # 收发信息
        ## 收，解码
        recv_data = client_socket.recv(512)
        print(recv_data.decode("utf-8"))

        ## 发，编码
        msg = "你好！"
        client_socket.send(msg.encode("utf-8"))

        client_socket.close()
        self.server_socket.close()


if __name__ == "__main__":
    Server().startup()
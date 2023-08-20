"""
@Description: 服务器核心功能
@Author: Pan Xiaofei
@Date: 2023-08-15 20:13:44
"""
from DB.db import MyDB
from myServerSocket import myServerSocket
from mySocketWrapper import mySocketWrapper
from threading import Thread
from config import *
from responseProtocol import responseProtocol

class Server(object):
    """
    @Description: 初始化服务器套接字
    @Parameters: 
    @Return: 
    """
    def __init__(self):
        # 初始化自定义服务器套接字
        self.server_socket = myServerSocket()

        # 请求处理函数对应字典
        self.requset_function_dict = {
            REQUEST_LOGIN : self.loginHandler,
            REQUEST_CHAT : self.chatHandler
        }

        """
        实时在线用户字典
        username : {'client_socket' : client_socket, 'nickname' : nickname}
        """
        self.online_clients = {}

        # 数据库操作对象
        self.db = MyDB()

    """
    @Description: 解析客户端请求
    @Parameters: 服务器接受解码后的客户端数据（客户端按照协议格式化过后）
    @Return: 解析体，字典
    """
    def parseRequest(self, recv_data):
        """
        解析规则：
        1. 登录请求体：0001|username|password
        2. 聊天请求体：0002|username|message
        """
        parse_data_list = recv_data.split('|')
        parse_data_dict = {}
        parse_data_dict['request_id'] = parse_data_list[0]
        parse_data_dict['username'] = parse_data_list[1]
        if parse_data_list[0] == REQUEST_LOGIN:
            parse_data_dict['password'] = parse_data_list[2]
        elif parse_data_list[0] == REQUEST_CHAT:
            parse_data_dict['message'] = parse_data_list[2]
        return parse_data_dict

    """
    @Description: 客户端主动关闭连接
    @Parameters: 客户端地址
    @Return: 
    """
    def logOut(self, client_socket, client_addr):
        print(f"用户{client_addr[0]}:{client_addr[1]}下线")
        for key, value in self.online_clients.items():
            if value['client_socket'] == client_socket:
                print(self.online_clients)
                del self.online_clients[key]
                print(self.online_clients)
                break
                
    """
    @Description: 登录请求处理
    @Parameters: 客户端套接字，解析后的数据
    @Return: 
    """
    def loginHandler(self, client_socket, parse_data):
        print("登录请求收到~")
        username = parse_data['username']
        password = parse_data['password']

        # 查询用户是否合法
        result, nickname, username = self.loginCheck(username, password)

        # 登录成功，保存客户端套接字
        if result == '1':
            self.online_clients[username] = {'client_socket' : client_socket, 'nickname' : nickname}

        # 连接结果并响应客户端
        response_login_data = responseProtocol().response_login_result(result, nickname, username)

        # 发送结果给客户端
        client_socket.sendData(response_login_data)
        print(self.online_clients)

    """
    @Description: 调用数据库查询，获取结果
    @Parameters: 
    @Return: 
    """
    def loginCheck(self, username, password):
        # 数据库通过用户名查询数据
        sql = "select * from users where username= '%s' " % username
        query_result = self.db.getItem(sql)

        # case1：用户不存在
        if not query_result:
            return '0', '', '' 
        
        # case2: 全部正确
        if query_result['password'] == password:
            return '1', query_result['nickname'], query_result['username']
        # case3: 密码不正确
        else:
            return '0', '', '' 

    """
    @Description: 处理聊天信息，即广播还是一对一 
    @Parameters: 
    @Return: 
    """
    def chatHandler(self, client_socket, parse_data):
        print("聊天请求收到~")
        # 获取消息内容
        username = parse_data['username']
        message = parse_data['message']
        nickname = self.online_clients[username]['nickname']

        # 拼接发送给客户端的消息文本
        transmit_msg = responseProtocol().response_chat(nickname, message)

        # 转发消息给在线用户（广播）
        for value in self.online_clients.values():
            # print(value)
            value['client_socket'].sendData(transmit_msg)

    """
    @Description: 服务器处理客户端请求
    @Parameters: 通信套接字
    @Return: 
    """
    def requestHandler(self, my_client_socket, client_addr):
        # 允许客户端与服务器多次交互
        while True: 
            ## 收，解码
            recv_data = my_client_socket.recvData()

            ## 若客户端发送信息为空，则判断下线，关闭客户端套接字，但保持服务器套接字开启
            if not recv_data:
                self.logOut(my_client_socket, client_addr)
                my_client_socket.closeSocket()
                break

            print("收到客户端信息：" + recv_data)
            ## 解析数据
            parse_data = self.parseRequest(recv_data)
            print("解析后的数据：%s" % parse_data)

            ## 执行相应功能函数
            requset_function = self.requset_function_dict.get(parse_data['request_id'])
            if requset_function:
                requset_function(my_client_socket, parse_data)
            

            # ## 发，编码
            # msg = "你好！"
            # my_client_socket.sendData(msg)

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
            
            # 收发信息，引入封装套接字
            ## 创建套接字对象
            my_client_socket = mySocketWrapper(client_socket)
                
            # 引入多线程，实现服务器与多个客户端同时交互
            t = Thread(target=self.requestHandler, args=(my_client_socket, client_addr))
            t.start()


if __name__ == "__main__":
    Server().startup()
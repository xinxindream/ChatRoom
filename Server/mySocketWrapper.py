"""
@Description: 服务器套接字封装
@Author: Pan Xiaofei
@Date: 2023-08-16 15:06:38
"""

import socket

class mySocketWrapper(object):
    """
    @Description: 初始化
    @Parameters: 当前通信的套接字
    @Return: 
    """
    def __init__(self, mysocket):
        self.mysocket = mysocket

    """
    @Description: 接受消息并解码
    @Parameters: 
    @Return: 解码后的信息
    """
    def recvData(self):
        return self.mysocket.recv(512).decode("utf-8")
    
    """
    @Description: 编码并发送消息
    @Parameters: 所要发送的消息
    @Return: 可以有返回值，所发送的信息字节数
    """
    def sendData(self, msg):
        self.mysocket.send(msg.encode("utf-8"))
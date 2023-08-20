"""
@Description: 服务器响应，返回字符串格式化
@Author: Pan Xiaofei
@Date: 2023-08-14 18:01:47
"""

from config import *

class responseProtocol(object):
    """
    @Description: 登录结果响应字符串 
    @Parameters: result, nickname, username
    |   result: 0 -> 登录失败， 1 -> 登录成功
    |   nickname: 昵称
    |   username: 用户名
    @Return: “响应结果代码|result|nickname|username”
    """
    def response_login_result(self, result, nickname, username):
        return DELIMITER.join([RESPONSE_LOGIN_RESULT, result, nickname, username])
    
    """
    @Description: 消息发送响应字符串
    @Parameters: 
    |   nickname: 昵称
    |   message: 消息正文
    @Return: “响应结果代码|nickname|message”
    """
    def response_chat(self, nickname, messages):
        return DELIMITER.join([RESPONSE_CHAT, nickname, messages])
import socket
from Server.config import *

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP,SERVER_PORT))

    while True:
        msg = input("请输入信息：")
        client_socket.send(msg.encode("utf-8"))
        recv_data = client_socket.recv(512)
        print(recv_data.decode("utf-8"))

    client_socket.close()
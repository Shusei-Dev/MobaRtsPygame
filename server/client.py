import socketserver

from socketserver import StreamRequestHandler, DatagramRequestHandler
from socketserver import ThreadingTCPServer, TCPServer, ThreadingUDPServer, UDPServer
from time import ctime
import socket


class Client:

    def __init__(self):
        server_host = ''
        server_port_number = 9999
        buffer_size = 10
        print("Input the data send to server:")
        while True:
            tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_client.connect((server_host, server_port_number))
            client_data = input(">")
            if client_data == 'bye':
                break

            tcp_client.sendall((client_data + '\r\n').encode('utf-8'))
            server_data_all = ''
            server_data = tcp_client.recv(buffer_size).decode('utf-8').strip()

            while len(server_data) > 0:
                server_data_all += server_data
                server_data = tcp_client.recv(buffer_size).decode('utf-8').strip()
            print('server_data_all : ' + server_data_all)

        tcp_client.close()

if __name__ == "__main__":
    client = Client()

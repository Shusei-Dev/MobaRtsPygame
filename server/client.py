import socketserver

from socketserver import StreamRequestHandler, DatagramRequestHandler
from socketserver import ThreadingTCPServer, TCPServer, ThreadingUDPServer, UDPServer
from time import ctime
import socket


class Client:

    def __init__(self):
        self.server_host = ''
        self.server_port_number = 9999
        self.buffer_size = 10

        self.login_state = 0 # 0 -> Do nothing, 1 -> Try to log-in, 2 -> Sign-in
        self.main_loop()

    def main_loop(self):
        # Choose what action do you want, log-in or sign-in
        print("Hello ! Do you want to log-in or to sign-in ? (L/S): \n")
        self.client_data = input(">")

        if self.client_data.lower() == "l":
            self.login_state = 1
        elif self.client_data.lower() == "s":
            self.login_state = 2
        else:
            print("You didnt choose a possible option, try again. \r\n")
            self.main_loop()

        # Connect to the server
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_client.connect((self.server_host, self.server_port_number))

        # Send the current login_state to the server
        self.tcp_client.sendall(("login_state=" + str(self.login_state) + '\r\n').encode('utf-8'))

        # Know if the server get the login_state
        self.response_server = self.getServerDataAll()
        if self.response_server == "1":
            if self.login_state == 1:
                print("Enter your username: \n")
                self.client_data = input(">")
                self.tcp_client.sendall(("user_name=" + self.client_data + '\r\n').encode('utf-8'))



        while True:


            client_data = input(">")
            if client_data == 'close':
                self.tcp_client.sendall((client_data + '\r\n').encode('utf-8'))
                break

            # Send the client data to the server
            self.tcp_client.sendall((client_data + '\r\n').encode('utf-8'))

            # Get the return content of the server
            server_data_all = self.getServerDataAll()
            print('server_data_all : ' + server_data_all)

        self.tcp_client.close()

    def getServerDataAll(self):
        server_data_all = ''
        server_data = self.tcp_client.recv(self.buffer_size).decode('utf-8').strip()

        while len(server_data) > 0:
            server_data_all += server_data
            server_data = self.tcp_client.recv(self.buffer_size).decode('utf-8').strip()

        return server_data_all

if __name__ == "__main__":
    client = Client()

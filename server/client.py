import socketserver

from socketserver import StreamRequestHandler, DatagramRequestHandler
from socketserver import ThreadingTCPServer, TCPServer, ThreadingUDPServer, UDPServer
from time import ctime
import socket


class Client:

    def __init__(self):
        self.server_host = 'localhost'
        self.server_port_number = 9999
        self.buffer_size = 1024

        self.login_state = 0 # 0 -> Not Connected, 1 -> Try to log-in, 2 -> Sign-in, 3 -> Connected
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


        if self.login_state == 1:
            if self.response_server == "1":
                print("Enter your username: \n")
                self.client_data = input(">")
                self.tcp_client.sendall(("user_name=" + self.client_data + '\r\n').encode('utf-8'))

            self.response_server = self.getServerDataAll()
            if self.response_server == "2":
                print("Enter your password: \n")
                self.client_data = input(">")
                self.tcp_client.sendall(("user_password=" + self.client_data + '\r\n').encode('utf-8'))

            self.response_server = self.getServerDataAll()
            print(self.response_server)
            if self.response_server == "3":
                print("You have been connected !")
                self.login_state = 3
                #self.tcp_client.sendall(("login_state=" + str(self.login_state) + '\r\n').encode('utf-8'))

            elif self.response_server == "4":
                print("Your information is not correct ! !")
                self.login_state = 0
                self.main_loop()

        if self.login_state == 2:
            if self.response_server == "1":
                print("Enter the username you wanted: \n")
                self.client_data = input(">")
                self.tcp_client.sendall(("user_name=" + self.client_data + '\r\n').encode('utf-8'))

            self.response_server = self.getServerDataAll()
            if self.response_server == "2":
                print("Enter the password you wanted: \n")
                self.client_data = input(">")
                self.tcp_client.sendall(("user_password=" + self.client_data + '\r\n').encode('utf-8'))

            self.response_server = self.getServerDataAll()
            if self.response_server == "3":
                print("Your account has been created successfully !")
                self.login_state = 0
                self.main_loop()
                #self.tcp_client.sendall(("login_state=" + str(self.login_state) + '\r\n').encode('utf-8'))

            elif self.response_server == "4":
                print("Your information is not correct ! !")
                self.login_state = 0
                self.main_loop()


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
        return str(server_data)

if __name__ == "__main__":
    client = Client()

import socketserver

from socketserver import StreamRequestHandler, DatagramRequestHandler
from socketserver import ThreadingTCPServer, TCPServer, ThreadingUDPServer, UDPServer
from time import ctime
import threading
import socket
import sys
import select

from data_base import *

global running
running = True

class TCPRequestHandler(StreamRequestHandler):
    def setup(self) -> None:
        self.cmdPrompt = CommandPrompt()
        self.database = DataBase()
        return super().setup()

    def handle(self) -> None:
        # Get the connection of a client
        client_ip = self.client_address[0]
        self.client_login_state = "0"
        print("connected from " + client_ip)


        # Get what send the client
        while running:
            lissable, ecrivable, special = select.select([self.rfile.raw.fileno()], [], [], 0.1)
            if lissable != []:
                client_send_data_line = self.rfile.readline().strip()
                client_data_str = client_send_data_line.decode('utf-8')

                # Check what current login_state is the client
                if self.client_login_state in ["0", "1", "2"]:
                    if "login_state" in getCDisVar(client_data_str) and getCDisVar(client_data_str)["login_state"] in ["1", "2"]:
                        self.client_login_state = getCDisVar(client_data_str)["login_state"]
                        print("A client is gonna try to connect to the server")
                        self.wfile.write(b"1")

                    if self.client_login_state == "1" and "user_name" in getCDisVar(client_data_str):
                        self.client_login_username = getCDisVar(client_data_str)["user_name"]
                        self.wfile.write(b"2")

                    if self.client_login_state == "1" and "user_password" in getCDisVar(client_data_str):
                        self.client_login_password = getCDisVar(client_data_str)["user_password"]
                        if self.database.check_user(self.client_login_username, self.client_login_password):
                            self.client_login_state = 3
                            print(f"A client({self.client_login_username}) has been connected to the server with success !")
                            self.wfile.write(b"3")
                        else:
                            self.client_login_state = 0
                            self.wfile.write(b"4")
                            break



                if self.client_login_state == 3 and "user_password" not in getCDisVar(client_data_str):
                    self.cmdPrompt.check_cmd(client_data_str, tcp_server)
                    self.wfile.write((client_data_str).encode('utf-8'))
            print("debug")


    def finish(self) -> None:
        return super().finish()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def getCDisVar(cd=str()):
    if "=" in cd:
        data_var_list = cd.split("=")
    else:
        return []

    if len(data_var_list) == 2:
        c = 0
        for data in data_var_list:
            data_var_list[c] = data.lstrip()
            c += 1

    return {data_var_list[0]: data_var_list[1]}


class CommandPrompt():

    def __init__(self):
        self.cmdDict = {"close_server": self.close_server}

    def check_cmd(self, data, server):
        self.dataList = data.split()
        self.server = server

        if len(self.dataList) == 1 and self.dataList[0] in self.cmdDict.keys():
            self.cmdDict[self.dataList[0]]()

    def close_server(self):
        print("Closing the server...")
        t = threading.Thread(target=self.shutdown).start()

    def shutdown(self):
        global running
        self.server.shutdown()
        running = False
        print("done")


def create_tcp_server():
    server_host = '0.0.0.0'
    server_port_number = 9999

    socketserver.TCPServer.allow_reuse_address = True
    doneEvent = threading.Event()

    print("main thread id:%x"%(id(threading.currentThread())))

    global tcp_server
    tcp_server = ThreadedTCPServer((server_host, server_port_number), TCPRequestHandler)
    tcp_running_message = 'TCP server is started on host \'' + server_host + ':' + str(server_port_number) + '\'\r\n'
    print(tcp_running_message)

    try:
        tcp_server.serve_forever()
        print(threading.enumerate())
        sys.exit(0)
    except KeyboardInterrupt:
        print("Arret forcé")
        tcp_server.server_close()


if __name__ == "__main__":
    create_tcp_server()

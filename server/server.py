import socketserver

from socketserver import StreamRequestHandler, DatagramRequestHandler
from socketserver import ThreadingTCPServer, TCPServer, ThreadingUDPServer, UDPServer
from time import ctime
import threading
import socket


class TCPRequestHandler(StreamRequestHandler):
    def setup(self) -> None:
        self.cmdPrompt = CommandPrompt()
        return super().setup()

    def handle(self) -> None:
        # Get the connection of a client
        client_ip = self.client_address[0]
        print("connected from " + client_ip)

        # Get what send the client
        client_send_data_line = self.rfile.readline().strip()
        client_data_str = client_send_data_line.decode('utf-8')

        # Check what current login_state is the client
        if "login_state" in getCDisVar(client_data_str) and getCDisVar(client_data_str)["login_state"] in ["1", "2"]:
            self.client_login_state = getCDisVar(client_data_str)["login_state"]
            self.wfile.write(b"1")

        client_send_data_line = self.rfile.readline().strip()
        client_data_str = client_send_data_line.decode('utf-8')

        if self.client_login_state == "1" and "user_name" in getCDisVar(client_data_str):
            print("AAAAAAA")



        #self.cmdPrompt.check_cmd(client_data_str, tcp_server)

        # Send to the client data
        #curr_time = ctime()
        #self.wfile.write((curr_time + ' - ' + client_data_str).encode('utf-8'))

    def finish(self) -> None:
        return super().finish()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def getCDisVar(cd=str()):
    if "=" in cd:
        data_var_list = cd.split("=")

    if len(data_var_list) == 2:
        c = 0
        for data in data_var_list:
            data_var_list[c] = data.lstrip()
            c += 1

    return {data_var_list[0]: data_var_list[1]}


class CommandPrompt():

    def __init__(self):
        self.cmdDict = {"close": self.close_server}

    def check_cmd(self, data, server):
        self.dataList = data.split()
        self.serverClass = server

        if len(self.dataList) <= 1 and self.dataList[0] in self.cmdDict.keys():
            self.cmdDict[self.dataList[0]](self.serverClass)

    def close_server(self, server):
        print("Closing the server...")
        server.shutdown()




def create_tcp_server():
    server_host = '0.0.0.0'
    server_port_number = 9999

    socketserver.TCPServer.allow_reuse_address = True

    global tcp_server
    tcp_server = ThreadedTCPServer((server_host, server_port_number), TCPRequestHandler)
    tcp_running_message = 'TCP server is started on host \'' + server_host + ':' + str(server_port_number) + '\'\r\n'
    print(tcp_running_message)
    try:
        tcp_server.serve_forever()
    except KeyboardInterrupt:
        print("Arret forcé")
        tcp_server.server_close()

if __name__ == "__main__":
    create_tcp_server()

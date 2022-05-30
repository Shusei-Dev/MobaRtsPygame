import socketserver

from socketserver import StreamRequestHandler, DatagramRequestHandler
from socketserver import ThreadingTCPServer, TCPServer, ThreadingUDPServer, UDPServer
from time import ctime
import socket


class TCPRequestHandler(StreamRequestHandler):
    def setup(self) -> None:
        self.cmdPrompt = CommandPrompt()
        return super().setup()

    def handle(self) -> None:
        client_ip = self.client_address[0]
        print("connected from " + client_ip)

        client_send_data_line = self.rfile.readline().strip()
        client_send_data_line_str = client_send_data_line.decode('utf-8')
        self.cmdPrompt.check_cmd(client_send_data_line_str, self)


        curr_time = ctime()
        self.wfile.write((curr_time + ' - ' + client_send_data_line_str).encode('utf-8'))

    def finish(self) -> None:
        return super().finish()

class CommandPrompt():

    def __init__(self):
        self.cmdDict = {"close": close_server}

    def check_cmd(self, data, server):
        self.dataList = data.split()
        self.serverClass = server

        if len(self.dataList) <= 1:
            self.cmdDict[self.dataList[0]](self.serverClass)

class close_server:

    def __init__(self, server):
        print("Closing the server...")
        server.shutdown()


def create_tcp_server():
    server_host = '0.0.0.0'
    server_port_number = 9999

    socketserver.TCPServer.allow_reuse_address = True
    tcp_server = TCPServer((server_host, server_port_number), TCPRequestHandler)
    tcp_running_message = 'TCP server is started on host \'' + server_host + ':' + str(server_port_number) + '\'\r\n'
    print(tcp_running_message)
    try:
        tcp_server.serve_forever()
    except KeyboardInterrupt:
        print("Arret forcé")
        tcp_server.server_close()

if __name__ == "__main__":
    create_tcp_server()

import socketserver

from socketserver import StreamRequestHandler, DatagramRequestHandler
from socketserver import ThreadingTCPServer, TCPServer, ThreadingUDPServer, UDPServer
from time import ctime
import socket


class TCPRequestHandler(StreamRequestHandler):
    def setup(self) -> None:
        print('\nSetup TCP request handler.')
        return super().setup()

    def handle(self) -> None:
        client_ip = self.client_address[0]
        print("connected from " + client_ip)

        client_send_data_line = self.rfile.readline().strip()
        client_send_data_line_str = client_send_data_line.decode('utf-8')
        print('client_send_data_line : ' + client_send_data_line_str)
        curr_time = ctime()
        self.wfile.write((curr_time + ' - ' + client_send_data_line_str).encode('utf-8'))

    def finish(self) -> None:
        print('Finish TCP request handler.\r\n')
        return super().finish()


def create_tcp_server():
    server_host = '0.0.0.0'
    server_port_number = 9999

    tcp_server = TCPServer((server_host, server_port_number), TCPRequestHandler)
    tcp_running_message = 'TCP server is started on host \'' + server_host + ':' + str(server_port_number) + '\'\r\n'
    print(tcp_running_message)
    tcp_server.serve_forever()

if __name__ == "__main__":
    create_tcp_server()

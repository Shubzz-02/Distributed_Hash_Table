import os,subprocess
import socket
from _thread import *
from socket import error

from Database import Database

IP_ADDRESS = socket.gethostbyname(socket.gethostname())
Port = 4553


class Server:
    """MAIN SERVER"""

    masterServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    masterServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self):
        self.masterServer.bind((IP_ADDRESS, Port))
        self.masterServer.listen(500)
        # self.Database = Database("../res/database.db")
        pass

    def start_server(self):
        # self.Database.check_if_exist()
        # self.Database.insert_node("Sad")
        while True:
            conn, addr = self.masterServer.accept()
            start_new_thread(self.node_thread, (conn, addr))
            # print("-----------> NEW CLIENT " + addr[0] + " " + str(addr[1]))
        pass

    def node_thread(self, conn, addr):
        try:
            while True:
                req = conn.recv(2048)
                if req:
                    if "GET" in req.decode("utf-8"):
                        out = os.subprocess.Popen(['java', 'my_text_file.txt'],
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.STDOUT)
                        # path = self.Database.get_det(req.decode("utf-8").split(":")[1])
                        # res = Server.read_file(path)
                        # conn.send(bytes(res))
                        # # print res         zip,2849963  192.168.43.240:4006
                        # # print ip_det   ../res/118B50C9E03B77F2A7311444FF6B01807E1C793905A2D693C97B18A335AD7475_IP_LIST.detail
                        # # print(req)     GET:118B50C9E03B77F2A7311444FF6B01807E1C793905A2D693C97B18A335AD7475
                        # conn.send(bytes("Hello Client " + addr[0] + " " + str(addr[1]), "utf-8"))
                    elif "PUT" in req.decode("utf-8"):
                        self.Database.insert(req.decode().split(":")[1])
                        Server.create_ip_list(req.decode().split(":")[1], addr)
                else:
                    break
        except error as e:
            print(e)
        pass

    @staticmethod
    def create_ip_list(data, addr):
        tdata = data.split(",")
        # print tdata  # ['118b50c9e03b77f2a7311444ff6b01807e1c793905a2d693c97b18a335ad7475', '2849963', 'zip']
        datatoe = tdata[2] + "," + tdata[1] + "\n" + str(addr[0]) + ":" + tdata[3] + " 1-10"
        print(datatoe)
        try:
            fp = open("../res/" + tdata[0] + "_IP_List.details", "wb")
            fp.write(bytes(datatoe, "utf-8"))
            fp.close()
            print("Server --> Create Ip list file")
        except error as e:
            print("Server --> Create Ip list file Error  " + str(e))
        pass

    @staticmethod
    def read_file(path):
        content = ""
        try:
            with open(path, 'rb') as f:
                content = f.read(os.path.getsize(path))
        except:
            print("Server --> unable to open ip_detail File")
        return content
        pass


if __name__ == "__main__":
    Server = Server()
    Server.start_server()

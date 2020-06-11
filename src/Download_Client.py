import socket
from socket import error

IP_ADDRESS = socket.gethostname()
PortTOS = 4553
ProtP2P = 4662


class DownloadClient:
    """NODES"""
    file = ""
    IP_Details = []
    file_info = []
    SHA = ""
    ui = ""

    def __init__(self, file_det, ui):
        self.file = file_det
        self.ui = ui
        pass

    def connect_to_server(self):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((IP_ADDRESS, PortTOS))
            conn.send(bytes("GET:" + self.SHA, "utf-8"))
            # print("SENT")
            res = conn.recv(6114)
            if self.write_file(res):
                # print(res)
                res = conn.recv(6114).decode("utf-8")
                print(res)
                conn.close()
                conn.close()
                return True
            else:
                conn.close()
                return False
        except error as e:
            self.ui.LogText.append("DownloadClient --> Error in connecting to server" + str(e))
            return False
        pass

    def read_sha(self):
        try:
            print("FILE " + self.file)
            f = open(self.file, 'rb')
            cont = f.read(1024)
            contw = cont
            while contw:
                contw = f.read(1024)
                cont += contw
            f.close()
            self.SHA = cont.decode()
            return True
        except:
            self.ui.LogText.append("DownloadClient --> Unable to read given det file")
            return False
        pass

    def write_file(self, res):
        try:
            fp = open("../res/" + self.SHA + ".details", "wb")
            fp.write(res)
            fp.close()
            return True
        except Exception as e:
            self.ui.LogText.append("DownloadClient --> Error in Writing IP_List file ")
            print("DownloadClient --> " + str(e))
            return False
        pass

    def populate_details(self):
        try:
            f = open("../res/" + self.SHA + ".details", "rb")
            cont = f.read(1024)
            contw = cont
            while contw:
                contw = f.read(1024)
                cont += contw
            f.close()
            cont = cont.decode("utf-8")
            self.file_info = cont[0:cont.find("\n")].split(",")
            self.file_info.append(self.SHA)
            # print(self.file_info)
            self.IP_Details = cont[cont.find("\n") + 1:].split("\n")
            # print(self.IP_Details)
            return [self.file_info, self.IP_Details]
        except Exception as e:
            print("Client --> Error")
        pass

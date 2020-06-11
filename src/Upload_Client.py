import hashlib
import os
import socket
from socket import error

IP_ADDRESS = socket.gethostname()
PortTOS = 4553


class UploadClient:
    """NODES"""
    file_det = ""

    SHA = ""

    ui=""

    def __call__(self, *args, **kwargs):
        pass

    def __init__(self, file_det, ui):
        self.file_det = file_det
        self.ui = ui
        pass

    def connect_to_server(self, port):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((IP_ADDRESS, PortTOS))
            self.SHA = UploadClient.calc_sha(self)
            file_det(self.SHA, self.file_det)
            if self.SHA:
                conn.send(bytes("PUT:" + str(self.SHA) + "," + str(os.path.getsize(self.file_det)) + "," +
                                os.path.splitext(self.file_det)[1].replace('.', '') + "," + str(port), "utf-8"))
                print(self.SHA)
                conn.close()
                return True
            else:
                print("Error")
                return False
        except error as e:
            self.ui.LogText.append("Client --> Error in connecting to server ")
            print("Error client --> "+str(e))
            return False
        pass

    def calc_sha(self):
        sha256_hash = hashlib.sha256()
        try:
            with open(self.file_det, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
                return sha256_hash.hexdigest()
        except error as e:
            print("false" + str(e))
            return False
        pass


def file_det(sha, path):
    try:
        fp = open("../res/list.hs", "ab+")
        fp.write(bytes(sha + " " + path + "\n", "utf-8"))
        fp.close()
        print("Client --> Created hs file")
    except error as e:
        print("Client --> Failed to create hs file  " + str(e))
    pass

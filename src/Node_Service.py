import math
import os
import socket
import tempfile
import threading


class NodeService(threading.Thread):
    ip_address = socket.gethostbyname(socket.gethostname())
    node_service = ""
    port = 59570

    def __init__(self, name):
        threading.Thread.__init__(self, daemon=True)
        self.thread_name = name
        pass

    def run(self):
        self.node_service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.node_service.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.node_service.bind((self.ip_address, self.port))
        self.node_service.listen(500)
        while True:
            conn, addr = self.node_service.accept()
            new_thread = threading.Thread(target=self.new_connection, args=(conn, addr))
            new_thread.start()
        pass

    def new_connection(self, conn, addr):
        try:
            req = conn.recv(2048)  # ['118b50c9e03b77f2a7311444ff6b01807e1c793905a2d693c97b18a335ad7475', 'Part_1']
            print("got connection")
            sha = req.decode("utf-8").split(" ")[0]
            part = req.decode("utf-8").split(" ")[1]
            path = self.get_path(sha)
            print(path)
            ptt = tempfile.gettempdir() + "/" + sha
            if not os.path.exists(ptt):
                print("Creating Directory in tmp")
                os.makedirs(ptt)
                self.div_file(path, ptt)
            self.send_file(conn, ptt, part)
            print("Started")
        except Exception as e:
            print("NODE SERVER " + str(e))
        pass

    @staticmethod
    def div_file(path, ptt):
        chunk = math.floor(os.path.getsize(path) / 10)
        fp = open(path, "rb")
        for i in range(9):
            filename = ptt + "/Part_" + str(i + 1)
            f = open(filename, "wb")
            f.write(fp.read(chunk))
            f.close()
        f = open(ptt + "/Part_10", "wb")
        f.write(fp.read())
        f.close()
        fp.close()
        pass

    def send_file(self, conn, path, part):
        try:
            print(path + "/" + part)
            fp = open(path + "/" + part, "rb")
            data = bytes()
            data = fp.read(1024)
            print(data)
            while data:
                conn.send(data)
                data = fp.read(1024)
            fp.close()
            print("Done sending")
            conn.close()
        except Exception as e:
            print("EEEEError in sending file " + repr(e))
        pass

    @staticmethod
    def get_path(sha):
        try:
            with open("../res/list.hs", 'rb') as f:
                content = f.read(os.path.getsize("../res/list.hs"))
            cont_l = content.decode("utf-8").split("\n")
            # print(cont_l.__len__())
            for i in range(cont_l.__len__()):
                if sha == cont_l[i].split(" ")[0]:
                    return cont_l[i].split(" ")[1]
        except Exception as e:
            print("Client --> file not found" + str(e))
        return ""
        pass

# TO-DO dhkk yaha bss abb kaam rhh gya file ko send krna div_file function ye kaam krra ki uss file ko 10 equal parts m
# divide krdera temp folder k ander abb bss upload file m ye kaam rhgya ki jo part request m aye usse send kre ...
# send_file function m kaam h bss iske baad download krni h file bss and UI m update krna h progress time delay k saath
# bss ab ye check krna h ki jo parts equal divide kre h wo sahi kre h

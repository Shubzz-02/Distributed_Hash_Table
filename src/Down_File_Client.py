import os
import random
import socket
import threading
import time


class DownloadService(threading.Thread):
    IP_ADDRESS = ""
    down_service = ""
    Port = ""
    Part = ""
    SHA = ""

    def __init__(self, ip, port, part, sha):
        threading.Thread.__init__(self)
        self.IP_ADDRESS = ip
        self.Port = port
        self.Part = part
        self.SHA = sha
        #  print(self.IP_ADDRESS + " " + str(self.Port) + " " + self.Part + " " + self.SHA)
        pass

    def run(self):
        time.sleep(random.randrange(5, 20))
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.IP_ADDRESS, self.Port))
        conn.send(bytes(self.SHA + " " + self.Part, "utf-8"))
        home = os.path.expanduser("~")
        downloads = os.path.join(home, "Downloads")
        with open(downloads + "/" + self.SHA + "/" + self.Part, "wb") as fp:
            while True:
                data = conn.recv(1024)
                # print(data)
                if not data:
                    break
                fp.write(data)
        print("Written " + self.Part)
        pass

# x = DownloadService("192.168.125.1", 59569, "Part_10",
#                     "118b50c9e03b77f2a7311444ff6b01807e1c793905a2d693c97b18a335ad7475")
# x.start()

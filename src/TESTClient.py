# #!/usr/bin/python3           # This is client.py file
#
# import socket
#
# # create a socket object
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # get local machine name
# host = socket.gethostname()
#
# port = 59569
#
# # connection to hostname on the port.
# s.connect((host, port))
#
# # Receive no more than 1024 bytes
# # msg = s.recv(1024)
#
# s.close()

# import os
#
# try:
#     with open("../res/list.hs", 'rb') as f:
#         content = f.read(os.path.getsize("../res/list.hs"))
#     cont_l = content.decode("utf-8").split("\n")
#     # print(cont_l.__len__())
#     for i in range(cont_l.__len__()):
#         if "118b50c9e03b77f2a7311444ff6b01807e1c793905a2d693c97b18a335ad7475" == cont_l[i].split(" ")[0]:
#             print("return "+ cont_l[i].split(" ")[1])
#
# except Exception as e:
#     print("Client --> file not found" + str(e))


try:
    f = open("../res/118b50c9e03b77f2a7311444ff6b01807e1c793905a2d693c97b18a335ad7475.details", "rb")
    cont = f.read(1024)
    contw = cont
    while contw:
        contw = f.read(1024)
        cont += contw
    f.close()
    cont = cont.decode("utf-8")
    # print(cont)  # zip,2849963   # 192.168.125.1:59569 1-10
    # print(cont[0: 11])    #zip,2849963
    # print(cont[0:cont.find("\n")].split(","))    #['zip', '2849963']
    # print(cont.find("\n"))  # 11
    # print(cont[12:])  # 192.168.125.1:59569 1-10
    # print(cont[12:].split("\n"))
    data = [cont[0:cont.find("\n")].split(","), cont[cont.find("\n") + 1:].split("\n")]
    print(data)  # [['zip', '2849963'], ['192.168.125.1:59569 1-10', '192.168.125.2:59569 2-10', '192.168.125.3:59569 3-10']]
    for i in range(data[1].__len__()):
        print(data[1][i].split(" ")[0] + " Part " + data[1][i].split(" ")[1])
except Exception as e:
    print("Client --> Error " + str(e))

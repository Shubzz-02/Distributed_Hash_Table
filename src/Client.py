import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from ClientGUI import Ui_MainWindow
from Down_File_Client import DownloadService
from Download_Client import DownloadClient
from Node_Service import NodeService
from Upload_Client import UploadClient


class MyWindow(QtWidgets.QMainWindow):
    DownloadClient = ""
    UploadClient = ""
    dwFileDet = ""

    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.upButton.clicked.connect(self.upbutton_clicked)
        self.ui.addButton.clicked.connect(self.addbutton_clicked)
        self.ui.dwbutton.clicked.connect(self.dwbutton_clicked)
        NodeService("NOde server").start()
        # service = threading.Thread(target=self.startService, args=(), daemon=True)
        # service.start()
        # self.startService()
        # self.port = random.randrange(54000, 62000)
        pass

    def upbutton_clicked(self):
        file = QFileDialog.getOpenFileName()[0]
        if file == "":
            self.ui.LogText.append("Client --> Select a valid file")
        else:
            self.UploadClient = UploadClient(file, self.ui)
            try:
                if UploadClient.connect_to_server(self.UploadClient, 59569):
                    self.ui.LogText.append("Client --> Successfully Updated")
                else:
                    self.ui.LogText.append("Client --> Aborting.....")
            except Exception as e:
                print(e)
        pass

    def addbutton_clicked(self):
        file = QFileDialog.getOpenFileName()[0]
        if file == "":
            self.ui.LogText.append("Client --> Select a valid .det file")
        else:
            self.DownloadClient = DownloadClient(file, self.ui)
            try:
                if DownloadClient.read_sha(self.DownloadClient) and DownloadClient.connect_to_server(
                        self.DownloadClient):
                    self.ui.LogText.append("Client --> Successfully Downloaded")
                    # self.ui.p_progressbar_1.setEnabled(True)
                    # self.ui.p_progressbar_1.setProperty("value", 50)
                    data = self.DownloadClient.populate_details()
                    self.dwFileDet = data
                    for i in range(data[1].__len__()):
                        self.ui.detText.append(
                            data[1][i].split(" ")[0] + " ------ Part " + data[1][i].split(" ")[1] + "\n")
                    self.ui.dwbutton.setEnabled(True)
                    self.ui.file_sha.setText(self.dwFileDet[0][2])
                    self.ui.file_size.setText(self.dwFileDet[0][1])
                else:
                    self.ui.LogText.append("Client --> Aborting.....")
            except Exception as e:
                print("Error " + str(e))
        pass

    def dwbutton_clicked(self):
        try:
            ip_lists = self.dwFileDet[1]  # ['192.138.1.1:59569 1-10']
            # print("IP LISTS ")
            print(ip_lists)
            print(ip_lists.__len__())
            print(ip_lists[0].split(" ")[0])
            print(ip_lists[0].split(" ")[0].split(":")[0])
            print(int(ip_lists[0].split(" ")[0].split(":")[1]))
            ct = 0
            home = os.path.expanduser("~")
            downloads = os.path.join(home, "Downloads")
            if not os.path.exists(downloads + "/" + self.dwFileDet[0][2]):
                os.mkdir(downloads + "/" + self.dwFileDet[0][2])
            for i in range(10):
                new_download = DownloadService(ip_lists[ct].split(" ")[0].split(":")[0],
                                               int(ip_lists[ct].split(" ")[0].split(":")[1]), "Part_" + str(i + 1),
                                               self.dwFileDet[0][2])
                new_download.start()
                if ct >= ip_lists.__len__():
                    ct = 0
            while self.get_dir_size(downloads + "/" + self.dwFileDet[0][2]) < int(self.dwFileDet[0][1]):
                self.ui.progressBar.setProperty("value", (
                        (self.get_dir_size(downloads + "/" + self.dwFileDet[0][2]))) / int(self.dwFileDet[0][1]) * 100)

                self.ui.progressBar.setProperty("value", 100)

            # self.start_download(ip_lists)
        except Exception as e:
            print(repr(e))
        pass

    def get_dir_size(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size
    # def add_progress(self, ip, i):
    #     font = QtGui.QFont()
    #     font.setFamily("Segoe UI Black")
    #     font.setPointSize(9)
    #     font.setBold(True)
    #     font.setWeight(75)
    #     _translate = QtCore.QCoreApplication.translate
    #     if i < 6:
    #         self.ui.p_label = QtWidgets.QLabel(self.ui.formLayoutWidget)
    #         self.ui.p_label.setEnabled(True)
    #         self.ui.p_label_1.setFont(font)
    #         self.ui.p_label_1.setObjectName("p_label_1")
    #         self.ui.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ui.p_label_1)
    #         self.ui.p_progressbar_1 = QtWidgets.QProgressBar(self.ui.formLayoutWidget)
    #         self.ui.p_progressbar_1.setEnabled(False)
    #         self.ui.p_progressbar_1.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    #         self.ui.p_progressbar_1.setProperty("value", 0)
    #         self.ui.p_progressbar_1.setTextVisible(True)
    #         self.ui.p_progressbar_1.setObjectName("p_progressbar_1")
    #         self.ui.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ui.p_progressbar_1)
    #         self.ui.p_label_1.setText(_translate("MainWindow", "Part-1 - 0.0.0.0"))
    #     pass


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()
sys.exit(app.exec_())

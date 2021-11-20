import os
import sqlite3
from configparser import ConfigParser
import re
from time import strftime
#from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import random
import datetime
import js8callAPIsupport
#import folium
import sqlite3
import io


serverip = ""
serverport = ""
callsign = ""
grid = ""
selectedgroup = ""
acklist = ""


class Ui_FormStatack(object):
    def setupUi(self, FormStatack):
        self.MainWindow = FormStatack
        FormStatack.setObjectName("FormStatack")
        FormStatack.resize(950, 500)
        font = QtGui.QFont()
        font.setPointSize(10)
        FormStatack.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("USA-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormStatack.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(FormStatack)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(FormStatack)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(FormStatack)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(FormStatack)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 1, 2)
        self.tableWidget = QtWidgets.QTableWidget(FormStatack)
        self.tableWidget.setObjectName("tableWidget")
        #self.tableWidget.setColumnCount(0)
        #self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 2)
        self.label = QtWidgets.QLabel(FormStatack)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(FormStatack)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 4, 2)
        self.tableWidget.clicked.connect(self.on_Click)

        self.getConfig()
        self.loadData()



        self.serveripad = serverip
        self.servport = int(serverport)
        self.api = js8callAPIsupport.js8CallUDPAPICalls((self.serveripad),
                                                        int(self.servport))
        self.pushButton_2.clicked.connect(self.MainWindow.close)
        self.pushButton.clicked.connect(self.transmit)



        self.retranslateUi(FormStatack)
        QtCore.QMetaObject.connectSlotsByName(FormStatack)

    def retranslateUi(self, FormStatack):
        _translate = QtCore.QCoreApplication.translate
        FormStatack.setWindowTitle(_translate("FormStatack", "CommStatX StatRep Ack"))
        self.label_2.setText(_translate("FormStatack", "Selected Callsigns for ACK :"))
        self.pushButton.setText(_translate("FormStatack", "Transmit"))
        #self.label.setText(_translate("FormStatack", ""))
        self.pushButton_2.setText(_translate("FormStatack", "Cancel"))


    def getConfig(self):
        global serverip
        global serverport
        global grid
        global callsign
        global selectedgroup
        if os.path.exists("config.ini"):
            config_object = ConfigParser()
            config_object.read("config.ini")
            userinfo = config_object["USERINFO"]
            systeminfo = config_object["DIRECTEDCONFIG"]
            callsign = format(userinfo["callsign"])
            callsignSuffix = format(userinfo["callsignsuffix"])
            group1 = format(userinfo["group1"])
            group2 = format(userinfo["group2"])
            grid = format(userinfo["grid"])
            path = format(systeminfo["path"])
            serverip = format(systeminfo["server"])
            serverport = format(systeminfo["port"])
            selectedgroup = format(userinfo["selectedgroup"])
            labeltext = ("Currently Active Group : " + selectedgroup)
            self.label.setText(labeltext)
            self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


    def loadData(self):
        #self.tableWidget = QtWidgets.QTableWidget(FormStatack)
        connection = sqlite3.connect('traffic.db3')
        query = """SELECT datetime, SRid, callsign, grid, prec, status, comments FROM StatRep_Data where groupname = ?"""
        result = connection.execute(query,(selectedgroup,))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                cellval = self.tableWidget.item(row_number, column_number).text()
                if self.tableWidget.item(row_number, column_number).text() == "1":
                    self.tableWidget.item(row_number, column_number).setBackground(QtGui.QColor(000, 128, 000))
                    self.tableWidget.item(row_number, column_number).setForeground(QtGui.QColor(000, 128, 000))
                if self.tableWidget.item(row_number, column_number).text() == "2":
                    # print("if statement worked"+cellval)
                    self.tableWidget.item(row_number, column_number).setBackground(QtGui.QColor(255, 255, 000))
                    self.tableWidget.item(row_number, column_number).setForeground(QtGui.QColor(255, 255, 000))
                if self.tableWidget.item(row_number, column_number).text() == "3":
                    # print("if statement worked" + cellval)
                    self.tableWidget.item(row_number, column_number).setBackground(QtGui.QColor(255, 000, 000))
                    self.tableWidget.item(row_number, column_number).setForeground(QtGui.QColor(255, 000, 000))
                # else:
                #   print("if statement failed"+cellval)

        table = self.tableWidget
        table.setHorizontalHeaderLabels(
            str("Date Time UTC ;ID ;Callsign; Grid ; Priority; Stat; Remarks").split(
                ";"))
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().setVisible(False)
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setStretchLastSection(True)
        # header.horizontalHeaderStretchLastSection = True
        # self.tableWidget = QtWidgets.QTableWidget()
        # self.addWidget(QTableWidget(table),0, 0, 1, 2)
        # self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.sortItems(0, QtCore.Qt.DescendingOrder)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 3)
        print("loadData completed")
        connection.close()





    def on_Click(self):
        global acklist
        index=(self.tableWidget.selectionModel().currentIndex())
        value = index.sibling(index.row(),2).data()
        acklist = acklist+ " * "+value
        self.lineEdit.setText("StatRep Received from : "+acklist)

    def transmit(self):
        global selectedgroup
        global callsign
        global acklist
        

        comments1 = "StatRep Received   "+ acklist
        comments = re.sub("[^A-Za-z0-9*\-\s]+", " ", comments1)

        if len(comments) < 5 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText( "Text too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox

            return
        group = "@"+selectedgroup
        message = "" + group + " MSG ," + comments + ""
        #message = ""+group + " ," + comments + ""
        messageType = js8callAPIsupport.TYPE_TX_SEND
        messageString = message

        #res = QMessageBox.question(FormCheckin, "Question", "Are you sure?", QMessageBox.Yes | QMessageBox.No)
        msg = QMessageBox()
        msg.setWindowTitle("CommStatX TX")
        msg.setText("CommStatX will transmit : " + message)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        x = msg.exec_()



        self.sendMessage(messageType, messageString)
        acklist = ""
        self.closeapp()

    def closeapp(self):
        self.MainWindow.close()

    def sendMessage(self, messageType, messageText):
        self.api.sendMessage(messageType, messageText)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormStatack = QtWidgets.QWidget()
    ui = Ui_FormStatack()
    ui.setupUi(FormStatack)
    FormStatack.show()
    sys.exit(app.exec_())

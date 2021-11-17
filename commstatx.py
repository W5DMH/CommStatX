import subprocess
import sys
import webbrowser
from random import randint
import feedparser
from file_read_backwards import FileReadBackwards
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QPlainTextEdit, QWidget, QTableWidget, QMenu, \
    QAction, qApp, QScrollArea, QLabel, QDialog, QInputDialog
from PyQt5.QtCore import QUrl, QTime, QTimer, QDateTime, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
import io
import folium
import sqlite3
import os
import settings
from settings import Ui_FormSettings
from configparser import ConfigParser
import threading
from subprocess import call
import time
from js8mail import Ui_FormJS8Mail
from js8sms import Ui_FormJS8SMS
from statrep import Ui_FormStatRep
from bulletin import Ui_FormBull
from marquee import Ui_FormMarquee
from checkin import Ui_FormCheckin
from members import Ui_FormMembers
from heardlist import Ui_FormHeard
from roster import Ui_FormRoster
from statack import Ui_FormStatack
from datareset import Ui_FormReset
from about import Ui_FormAbout


callsign = ""
callsignSuffix = ""
group1 = ""
group2 = ""
grid = ""
path = ""
selectedgroup = ""
counter = 0
directedcounter = 0



class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        global marqueecolor
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("USA-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(400, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)

        self.label.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                   "color: rgb(0, 200, 0);")

        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0,0, 1, 2, QtCore.Qt.AlignHCenter)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                   "color: rgb(0, 200, 0);")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_3.setText("Current Group : AMMRRON")


        self.readconfig()
        #self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        #self.tableWidget.setObjectName("tableWidget")
        #self.tableWidget.setColumnCount(0)
        #self.tableWidget.setRowCount(0)
        #self.gridLayout_2.addWidget(self.tableWidget, 1, 0, 1, 1)
        #self.loadData()

        #self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        #self.plainTextEdit.setObjectName("plainTextEdit")
        #self.gridLayout_2.addWidget(self.plainTextEdit, 2, 0, 1, 1)
        self.directed()


        #self.widget = QtWidgets.QWidget(self.centralwidget)
        #self.widget.setObjectName("widget")
        #self.gridLayout_2.addWidget(self.widget, 3, 0, 1, 1)
        self.mapperWidget()

        #self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        #self.tableWidget_2.setObjectName("tableWidget_2")
        #self.tableWidget_2.setColumnCount(0)
        #self.tableWidget_2.setRowCount(0)
        #self.gridLayout_2.addWidget(self.tableWidget_2, 3, 1, 1, 1)
        #self.loadbulletins()

        self.gridLayout_2.setRowStretch(0, 0);
        self.gridLayout_2.setRowStretch(1, 1);
        self.gridLayout_2.setRowStretch(2, 1);
        self.gridLayout_2.setRowStretch(3, 1);
        #self.gridLayout.setRowStretch(0, 3);
        #self.gridLayout.setRowStretch(1, 1);
        #self.gridLayout.setRowStretch(2, 2);
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)

        #self.actionExit_2 = QAction('&actionEXIT', MainWindow)
        #self.actionExit_2.setShortcut('Ctrl+Q')
        #self.actionExit_2.setStatusTip('APPLICATION EXIT')


        #self.actionYellow.triggered.connect(lambda: self.change("yellow"))



        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 886, 22))
        self.menubar.setObjectName("menubar")
        self.menuEXIT = QtWidgets.QMenu(self.menubar)
        self.menuEXIT.setObjectName("menuEXIT")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionJS8EMAIL = QtWidgets.QAction(MainWindow)
        self.actionJS8EMAIL.setObjectName("actionJS8EMAIL")
        self.actionJS8SMS = QtWidgets.QAction(MainWindow)
        self.actionJS8SMS.setObjectName("actionJS8SMS")
        self.actionSTATREP = QtWidgets.QAction(MainWindow)
        self.actionSTATREP.setObjectName("actionSTATREP")
        self.actionNET_CHECK_IN = QtWidgets.QAction(MainWindow)
        self.actionNET_CHECK_IN.setObjectName("actionNET_CHECK_IN")
        self.actionMEMBER_LIST = QtWidgets.QAction(MainWindow)
        self.actionMEMBER_LIST.setObjectName("actionMEMBER_LIST")
        self.actionHEARD_LIST = QtWidgets.QAction(MainWindow)
        self.actionHEARD_LIST.setObjectName("actionHEARD_LIST")
        self.actionSTATREP_ACK = QtWidgets.QAction(MainWindow)
        self.actionSTATREP_ACK.setObjectName("actionSTATREP_ACK")
        self.actionNET_ROSTER = QtWidgets.QAction(MainWindow)
        self.actionNET_ROSTER.setObjectName("actionNET_ROSTER")
        self.actionNEW_MARQUEE = QtWidgets.QAction(MainWindow)
        self.actionNEW_MARQUEE.setObjectName("actionNEW_MARQUEE")
        self.actionFLASH_BULLETIN = QtWidgets.QAction(MainWindow)
        self.actionFLASH_BULLETIN.setObjectName("actionFLASH_BULLETIN")
        self.actionSETTINGS = QtWidgets.QAction(MainWindow)
        self.actionSETTINGS.setObjectName("actionSETTINGS")
        self.actionDATA_RESET = QtWidgets.QAction(MainWindow)
        self.actionDATA_RESET.setObjectName("actionDATA_RESET")
        self.actionHELP = QtWidgets.QAction(MainWindow)
        self.actionHELP.setObjectName("actionHELP")
        self.actionABOUT = QtWidgets.QAction(MainWindow)
        self.actionABOUT.setObjectName("actionABOUT")

        self.actionEXIT_2 = QtWidgets.QAction(MainWindow)
        self.actionEXIT_2.setObjectName("actionEXIT_2")


        self.menuEXIT.addAction(self.actionJS8EMAIL)
        self.actionJS8EMAIL.triggered.connect(self.js8email_window)
        self.menuEXIT.addAction(self.actionJS8SMS)
        self.actionJS8SMS.triggered.connect(self.js8sms_window)
        self.menuEXIT.addAction(self.actionSTATREP)
        self.actionSTATREP.triggered.connect(self.statrep_window)
        self.menuEXIT.addAction(self.actionNET_CHECK_IN)
        self.actionNET_CHECK_IN.triggered.connect(self.checkin_window)
        self.menuEXIT.addAction(self.actionMEMBER_LIST)
        self.actionMEMBER_LIST.triggered.connect(self.members_window)
        self.menuEXIT.addAction(self.actionHEARD_LIST)
        self.actionHEARD_LIST.triggered.connect(self.heard_window)
        self.menuEXIT.addSeparator()
        self.menuEXIT.addAction(self.actionSTATREP_ACK)
        self.actionSTATREP_ACK.triggered.connect(self.statack_window)
        self.menuEXIT.addAction(self.actionNET_ROSTER)
        self.actionNET_ROSTER.triggered.connect(self.roster_window)
        self.menuEXIT.addAction(self.actionNEW_MARQUEE)
        self.actionNEW_MARQUEE.triggered.connect(self.marquee_window)
        self.menuEXIT.addAction(self.actionFLASH_BULLETIN)
        self.actionFLASH_BULLETIN.triggered.connect(self.bull_window)
        self.menuEXIT.addSeparator()
        self.menuEXIT.addAction(self.actionSETTINGS)
        self.actionSETTINGS.triggered.connect(self.settings_window)


        self.menuEXIT.addAction(self.actionDATA_RESET)
        self.actionDATA_RESET.triggered.connect(self.reset_window)
        self.menuEXIT.addAction(self.actionHELP)
        self.actionHELP.triggered.connect(self.open_webbrowser)
        self.menuEXIT.addAction(self.actionABOUT)
        self.actionABOUT.triggered.connect(self.about_window)

        self.menuEXIT.addSeparator()
        self.menuEXIT.addAction(self.actionEXIT_2)
        self.actionEXIT_2.triggered.connect(qApp.quit)
        self.menubar.addAction(self.menuEXIT.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000) # update every second
        self.showTime()

        self.timeLine = QtCore.QTimeLine()
        self.timeLine.setCurveShape(QtCore.QTimeLine.LinearCurve)                   # linear Timeline
        self.timeLine.frameChanged.connect(self.setText)
        self.timeLine.finished.connect(self.nextNews)
        self.signalMapper = QtCore.QSignalMapper(self)
        self.signalMapper.mapped[str].connect(self.setTlText)

        self.feed()


        finalpath = os.path.normpath(path)
        watch = QtCore.QFileSystemWatcher(self)
        watch.addPath(finalpath)
        print(finalpath)
        watch.fileChanged.connect(self.thread)



        finalpath2 = os.path.abspath(os.getcwd())
        finalpath3 = finalpath2+"/copyDIRECTED.TXT"
        watch2 = QtCore.QFileSystemWatcher(self)
        watch2.addPath(finalpath3)
        print(finalpath3)
        watch2.fileChanged.connect(self.directed)

        #finalpath2 = os.path.abspath(os.getcwd())
        #finalpath4 = finalpath2+"\\traffic.db3"
        #watch3 = QtCore.QFileSystemWatcher(self)
        #watch3.addPath(finalpath4)
        #print(finalpath3)
        #watch3.fileChanged.connect(self.directed)





    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CommStatX"))
        self.label.setText(_translate("MainWindow", "TextLabel Marquee"))
        self.label_2.setText(_translate("MainWindow", "TextLabel Clock"))
        self.menuEXIT.setTitle(_translate("MainWindow", "MENU"))
        self.actionJS8EMAIL.setText(_translate("MainWindow", "JS8EMAIL"))
        self.actionJS8SMS.setText(_translate("MainWindow", "JS8SMS"))
        self.actionSTATREP.setText(_translate("MainWindow", "STATREP"))
        self.actionNET_CHECK_IN.setText(_translate("MainWindow", "NET CHECK IN"))
        self.actionMEMBER_LIST.setText(_translate("MainWindow", "MEMBER LIST"))
        self.actionHEARD_LIST.setText(_translate("MainWindow", "HEARD LIST"))
        self.actionSTATREP_ACK.setText(_translate("MainWindow", "STATREP ACK"))
        self.actionNET_ROSTER.setText(_translate("MainWindow", "NET ROSTER"))
        self.actionNEW_MARQUEE.setText(_translate("MainWindow", "NEW MARQUEE"))
        self.actionFLASH_BULLETIN.setText(_translate("MainWindow", "FLASH BULLETIN"))
        self.actionSETTINGS.setText(_translate("MainWindow", "SETTINGS"))
        self.actionDATA_RESET.setText(_translate("MainWindow", "DATA RESET"))
        self.actionABOUT.setText(_translate("MainWindow", "ABOUT"))
        self.actionHELP.setText(_translate("MainWindow", "HELP"))
        self.actionEXIT_2.setText(_translate("MainWindow", "EXIT"))









    def readconfig(self):
        # Read config.ini file
        config_object = ConfigParser()
        config_object.read("config.ini")
        global callsign
        global callsignSuffix
        global group1
        global group2
        global grid
        global path
        global selectedgroup

        # Get the password
        userinfo = config_object["USERINFO"]
        #print("callsign is {}".format(userinfo["callsign"]))
        #print("callsignsuffix is {}".format(userinfo["callsignsuffix"]))
        #print("group1 is {}".format(userinfo["group1"]))
        #print("group2 is {}".format(userinfo["group2"]))
        #print("grid is {}".format(userinfo["grid"]))
        systeminfo = config_object["DIRECTEDCONFIG"]
        #print("file path  is {}".format(systeminfo["path"]))
        callsign = format(userinfo["callsign"])
        callsignSuffix = format(userinfo["callsignsuffix"])
        group1 = format(userinfo["group1"])
        group2 = format(userinfo["group2"])
        grid = format(userinfo["grid"])
        path1 = format(systeminfo["path"])
        path = (path1+"/DIRECTED.TXT")
        selectedgroup = format(userinfo["selectedgroup"])
        #print("this is the new path :"+path)
        #print(selectedgroup)
        if (callsign =="NOCALL"):
            self.settings_window()

    def help_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormSettings()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()



    def settings_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormSettings()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()


    def js8email_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormJS8Mail()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()


    def js8sms_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormJS8SMS()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()


    def statrep_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormStatRep()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()

    def bull_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormBull()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()


    def marquee_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormMarquee()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()


    def checkin_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormCheckin()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()


    def members_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormMembers()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()

    def heard_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormHeard()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()

    def roster_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormRoster()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()


    def statack_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormStatack()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()

    def reset_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormReset()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()

    def about_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormAbout()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()

    def loadData(self):
        print("load data restarted")
        self.readconfig()
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        connection = sqlite3.connect('traffic.db3')
        query = """SELECT datetime, SRid, callsign, grid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel, food, crime, civil, political, comments FROM StatRep_Data where groupname = ?"""
        result = connection.execute(query,(selectedgroup,))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(18)
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
            str("Date Time UTC ;ID ;Callsign; Grid ; Priority; Stat; Pow; H2O; Med; Com; Trv; Int; Fuel; Food; Cri; Civ; Pol; Remarks").split(
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
        self.gridLayout_2.addWidget(self.tableWidget, 1, 0, 1, 4)
        print("loadData completed")
        connection.close()


    def directed(self):
        global directedcounter
        with open(path) as f, open('output.txt', 'w') as fout:
            fout.writelines(reversed(f.readlines()))
        text = open('output.txt').read()
        text_edit_widget = QPlainTextEdit(text)
        # text_edit_widget.setStyleSheet(
        #     """QPlainTextEdit {background-color: #7E7C7A;
        #                      color: #FCF55F;
        #                     text-decoration: underline;
        #                    font-family: Courier;}""")
        self.gridLayout_2.addWidget(text_edit_widget, 2, 0, 1, 4)
        directedcounter += 1
        print("Directed completed : counter :"+str(directedcounter))

        self.loadbulletins()
        self.loadData()
        self.label_3.setText(" Active Group : "+selectedgroup)
        QtCore.QTimer.singleShot(30000, self.directed)

    def mapperWidget(self):
        mapper = QWebEngineView()
        coordinate = (38.8199286, -90.4782551)
        m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=4,
            location=coordinate

        )

        try:
            sqliteConnection = sqlite3.connect('traffic.db3')
            cursor = sqliteConnection.cursor()
           # print("Connected to SQLite")
            sqlite_select_query = 'SELECT gridlat, gridlong, callsign, date FROM heard_Data;'
            cursor.execute(sqlite_select_query)
            items = cursor.fetchall()

            for item in items:
                glat = item[0]
                glon = item[1]
                call = item[2]
                utc = item[3]

                pinstring = (" Last Heard :")
                html = '''<HTML> <BODY><p style="color:blue;font-size:14px;">%s<br>
                %s<br>
                %s
                </p></BODY></HTML>''' % (call, pinstring, utc)
                iframe = folium.IFrame(html,
                                       width=160,
                                       height=70)

                popup = folium.Popup(iframe,
                                     min_width=100, max_width=160)
                #folium.Marker(location=[glat, glon], popup=popup).add_to(m)
                folium.CircleMarker(radius=6,fill=True, fill_color="darkblue",
                 location=[glat, glon], popup=popup, icon=folium.Icon(color="red")).add_to(m)


            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
         #       print("The SQLite connection is closed")
        # return map

        # folium.Marker(location=[38.655800, -87.274721],popup='<h3 style="color:green;">Marker2</h3>').add_to(m)
        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        #self.gridLayout.addWidget()widget = QWebEngineView()
        mapper.setHtml(data.getvalue().decode())
        self.gridLayout_2.addWidget(mapper, 3, 0, 1, 1)
        #print("Mapping completed")

        QtCore.QTimer.singleShot(180000, self.mapperWidget)

    def loadbulletins(self):
        self.readconfig()
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        connection = sqlite3.connect('traffic.db3')
        query = "SELECT datetime, idnum, callsign, message FROM bulletins_Data where groupid = ?"
        result = connection.execute(query, (selectedgroup,))
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(4)
        for row_number, row_data in enumerate(result):
            self.tableWidget_2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_2.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        table = self.tableWidget_2
        table.setHorizontalHeaderLabels(
            str("Date Time UTC ;ID ;Callsign; Grid ; Priority; Status; Power; Water; Medical; Comms; Travel; Internet; Fuel; Food; Crime; Civil; Political; Remarks").split(
                ";"))
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # self.tableWidget = QtWidgets.QTableWidget()
        # self.addWidget(QTableWidget(table),0, 0, 1, 2)
        # self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.sortItems(0, QtCore.Qt.DescendingOrder)
        self.gridLayout_2.addWidget(self.tableWidget_2, 3, 1, 1, 3)

        #print("Load Bulletins & Marquee Completed")
        #QtCore.QTimer.singleShot(30000, self.loadbulletins)



    def thread_second():
        call(["python", "datareader.py"])

    #processThread = threading.Thread(target=thread_second)  # <- note extra ','
    #processThread.daemon = True
    #processThread.start()

    def showTime(self):
        #currentTime = QTime.currentTime()
        #currentTime = QTime.toUTC()
        now = QDateTime.currentDateTime()
        displayTxt = (now.toUTC().toString(Qt.ISODate))
        self.label_2.setText(" "+displayTxt+" ")

    def thread(self):
        t1 = threading.Thread(target=self.Operation)
        t1.start()

    def Operation(self):
        global counter
        print("time start")
        counter += 1
        print("here is the thread counter"+str(counter))
        call(["python3", "datareader.py"])

        #time.sleep(10)
        print("datareader stopped")


    def feed(self):
        #QtCore.QTimer.singleShot(30000, self.loadbulletins)
        marqueegreen = "color: rgb(0, 200, 0);"
        marqueeyellow = "color: rgb(255, 255, 0);"
        marqueered = "color: rgb(255, 0, 0);"
        connection = sqlite3.connect('traffic.db3')
        query = "SELECT* FROM marquees_data WHERE groupname = ? ORDER BY date DESC LIMIT 1"
        result = connection.execute(query, (selectedgroup,))
        result = result.fetchall()
        if len(result) < 1:
            print("no records found")
            return
        callSend = (result[0][2])
        id = (result[0][1])
        group = (result[0][3])
        date = (result[0][4])
        msg = (result[0][6])
        color = (result[0][5])
        if (color == "2"):
            self.label.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                     "" + marqueered + "")
        elif(color == "1"):
            self.label.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                     "" + marqueeyellow + "")
        else:
            self.label.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                     "" + marqueegreen + "")

        marqueetext = (" ID "+id+" Received  : "+date+"  From : "+group+" by : "+callSend+" MSG : "+msg )
        connection.close()
        fm = self.label.fontMetrics()
        self.nl = int(self.label.width()/fm.averageCharWidth())     # shown stringlength
        news = [marqueetext]
        appendix = ' '*self.nl                      # add some spaces at the end
        news.append(appendix)
        delimiter = '      +++      '                   # shown between the messages
        self.news = delimiter.join(news)
        newsLength = len(self.news)                 # number of letters in news = frameRange
        lps = 6                                 # letters per second
        dur = newsLength*500/lps               # duration until the whole string is shown in milliseconds
        self.timeLine.setDuration(20000)
        self.timeLine.setFrameRange(0, newsLength)
        self.timeLine.start()


    def setText(self, number_of_frame):
        if number_of_frame < self.nl:
            start = 0
        else:
            start = number_of_frame - self.nl
        text = '{}'.format(self.news[start:number_of_frame])
        self.label.setText(text)
        self.label.setFixedWidth(400)

    def nextNews(self):
        self.feed()                             # start again

    def setTlText(self, text):
        string = '{} pressed'.format(text)
        self.textLabel.setText(string)

    def open_webbrowser(self):
        webbrowser.open('CommStat_Help.pdf')




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

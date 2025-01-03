# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\PiratePlay\views\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 800)
        self.mainGridLayout = QtWidgets.QGridLayout(MainWindow)
        self.mainGridLayout.setObjectName("mainGridLayout")
        self.line = QtWidgets.QFrame(MainWindow)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.mainGridLayout.addWidget(self.line, 2, 0, 1, 2)
        self.stackedWidget = QtWidgets.QStackedWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")
        self.mainContentPage = QtWidgets.QWidget()
        self.mainContentPage.setObjectName("mainContentPage")
        self.stackedWidget.addWidget(self.mainContentPage)
        self.secondaryContentPage = QtWidgets.QWidget()
        self.secondaryContentPage.setObjectName("secondaryContentPage")
        self.stackedWidget.addWidget(self.secondaryContentPage)
        self.mainGridLayout.addWidget(self.stackedWidget, 4, 1, 1, 1)
        self.navigationLayout = QtWidgets.QVBoxLayout()
        self.navigationLayout.setObjectName("navigationLayout")
        self.navigationHomeButton = QtWidgets.QPushButton(MainWindow)
        self.navigationHomeButton.setObjectName("navigationHomeButton")
        self.navigationLayout.addWidget(self.navigationHomeButton)
        self.navigationDiscoverButton = QtWidgets.QPushButton(MainWindow)
        self.navigationDiscoverButton.setObjectName("navigationDiscoverButton")
        self.navigationLayout.addWidget(self.navigationDiscoverButton)
        self.navigationCollectionsButton = QtWidgets.QPushButton(MainWindow)
        self.navigationCollectionsButton.setObjectName("navigationCollectionsButton")
        self.navigationLayout.addWidget(self.navigationCollectionsButton)
        self.navigationDownloadsButton = QtWidgets.QPushButton(MainWindow)
        self.navigationDownloadsButton.setObjectName("navigationDownloadsButton")
        self.navigationLayout.addWidget(self.navigationDownloadsButton)
        self.navigationPlayerButton = QtWidgets.QPushButton(MainWindow)
        self.navigationPlayerButton.setObjectName("navigationPlayerButton")
        self.navigationLayout.addWidget(self.navigationPlayerButton)
        self.navigationNewsButton = QtWidgets.QPushButton(MainWindow)
        self.navigationNewsButton.setObjectName("navigationNewsButton")
        self.navigationLayout.addWidget(self.navigationNewsButton)
        self.navigationSettingsButton = QtWidgets.QPushButton(MainWindow)
        self.navigationSettingsButton.setObjectName("navigationSettingsButton")
        self.navigationLayout.addWidget(self.navigationSettingsButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.navigationLayout.addItem(spacerItem)
        self.mainGridLayout.addLayout(self.navigationLayout, 4, 0, 1, 1)
        self.headerLayout = QtWidgets.QHBoxLayout()
        self.headerLayout.setObjectName("headerLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.headerLayout.addItem(spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.headerLayout.addItem(spacerItem2)
        self.globalSearchInput = QtWidgets.QLineEdit(MainWindow)
        self.globalSearchInput.setObjectName("globalSearchInput")
        self.headerLayout.addWidget(self.globalSearchInput)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.headerLayout.addItem(spacerItem3)
        self.userProfileButton = QtWidgets.QPushButton(MainWindow)
        self.userProfileButton.setObjectName("userProfileButton")
        self.headerLayout.addWidget(self.userProfileButton)
        self.themeToggleButton = QtWidgets.QPushButton(MainWindow)
        self.themeToggleButton.setObjectName("themeToggleButton")
        self.headerLayout.addWidget(self.themeToggleButton)
        self.mainGridLayout.addLayout(self.headerLayout, 3, 0, 1, 2)
        self.horizontalLayout_TITLEBAR = QtWidgets.QHBoxLayout()
        self.horizontalLayout_TITLEBAR.setSpacing(5)
        self.horizontalLayout_TITLEBAR.setObjectName("horizontalLayout_TITLEBAR")
        self.mainGridLayout.addLayout(self.horizontalLayout_TITLEBAR, 0, 0, 1, 2)
        self.applicationLogo = QtWidgets.QLabel(MainWindow)
        self.applicationLogo.setObjectName("applicationLogo")
        self.mainGridLayout.addWidget(self.applicationLogo, 5, 1, 1, 1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Musicly"))
        self.navigationHomeButton.setText(_translate("MainWindow", "Home"))
        self.navigationDiscoverButton.setText(_translate("MainWindow", "Discover"))
        self.navigationCollectionsButton.setText(_translate("MainWindow", "Collections"))
        self.navigationDownloadsButton.setText(_translate("MainWindow", "Downloads"))
        self.navigationPlayerButton.setText(_translate("MainWindow", "Player"))
        self.navigationNewsButton.setText(_translate("MainWindow", "News"))
        self.navigationSettingsButton.setText(_translate("MainWindow", "Settings"))
        self.globalSearchInput.setPlaceholderText(_translate("MainWindow", "Search for movies, tv series, or animes..."))
        self.userProfileButton.setText(_translate("MainWindow", "Profile"))
        self.themeToggleButton.setText(_translate("MainWindow", "Dark Mode"))

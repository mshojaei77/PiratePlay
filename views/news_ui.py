# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\PiratePlay\views\news.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewsWidget(object):
    def setupUi(self, NewsWidget):
        NewsWidget.setObjectName("NewsWidget")
        NewsWidget.resize(800, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(NewsWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.NewsScrollArea = QtWidgets.QScrollArea(NewsWidget)
        self.NewsScrollArea.setWidgetResizable(True)
        self.NewsScrollArea.setObjectName("NewsScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 798, 598))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.NewsScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.NewsScrollArea)

        self.retranslateUi(NewsWidget)
        QtCore.QMetaObject.connectSlotsByName(NewsWidget)

    def retranslateUi(self, NewsWidget):
        _translate = QtCore.QCoreApplication.translate
        NewsWidget.setWindowTitle(_translate("NewsWidget", "News"))
        self.label.setText(_translate("NewsWidget", "News"))

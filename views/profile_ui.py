# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\PiratePlay\views\profile.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StreamingProfileDialog(object):
    def setupUi(self, StreamingProfileDialog):
        StreamingProfileDialog.setObjectName("StreamingProfileDialog")
        StreamingProfileDialog.resize(538, 295)
        self.verticalLayout = QtWidgets.QVBoxLayout(StreamingProfileDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.profileGroup = QtWidgets.QGroupBox(StreamingProfileDialog)
        self.profileGroup.setTitle("")
        self.profileGroup.setObjectName("profileGroup")
        self.formLayout = QtWidgets.QFormLayout(self.profileGroup)
        self.formLayout.setObjectName("formLayout")
        self.usernameLabel = QtWidgets.QLabel(self.profileGroup)
        self.usernameLabel.setObjectName("usernameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.usernameLabel)
        self.usernameEdit = QtWidgets.QLineEdit(self.profileGroup)
        self.usernameEdit.setObjectName("usernameEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.usernameEdit)
        self.emailLabel = QtWidgets.QLabel(self.profileGroup)
        self.emailLabel.setObjectName("emailLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.emailLabel)
        self.emailEdit = QtWidgets.QLineEdit(self.profileGroup)
        self.emailEdit.setObjectName("emailEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.emailEdit)
        self.subscriptionLabel = QtWidgets.QLabel(self.profileGroup)
        self.subscriptionLabel.setObjectName("subscriptionLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.subscriptionLabel)
        self.subscriptionCombo = QtWidgets.QComboBox(self.profileGroup)
        self.subscriptionCombo.setObjectName("subscriptionCombo")
        self.subscriptionCombo.addItem("")
        self.subscriptionCombo.addItem("")
        self.subscriptionCombo.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.subscriptionCombo)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonLayout.addItem(spacerItem)
        self.cancelButton = QtWidgets.QPushButton(self.profileGroup)
        self.cancelButton.setObjectName("cancelButton")
        self.buttonLayout.addWidget(self.cancelButton)
        self.saveButton = QtWidgets.QPushButton(self.profileGroup)
        self.saveButton.setObjectName("saveButton")
        self.buttonLayout.addWidget(self.saveButton)
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.SpanningRole, self.buttonLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        self.verticalLayout.addWidget(self.profileGroup)

        self.retranslateUi(StreamingProfileDialog)
        QtCore.QMetaObject.connectSlotsByName(StreamingProfileDialog)

    def retranslateUi(self, StreamingProfileDialog):
        _translate = QtCore.QCoreApplication.translate
        StreamingProfileDialog.setWindowTitle(_translate("StreamingProfileDialog", "Streaming Profile Settings"))
        self.usernameLabel.setText(_translate("StreamingProfileDialog", "Username:"))
        self.emailLabel.setText(_translate("StreamingProfileDialog", "Email:"))
        self.subscriptionLabel.setText(_translate("StreamingProfileDialog", "Subscription Plan:"))
        self.subscriptionCombo.setItemText(0, _translate("StreamingProfileDialog", "Basic"))
        self.subscriptionCombo.setItemText(1, _translate("StreamingProfileDialog", "Standard"))
        self.subscriptionCombo.setItemText(2, _translate("StreamingProfileDialog", "Premium"))
        self.cancelButton.setText(_translate("StreamingProfileDialog", "Cancel"))
        self.saveButton.setText(_translate("StreamingProfileDialog", "Save Changes"))
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BaseConfig.ui'
#
# Created: Thu Feb 04 11:39:52 2016
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DatabaseConfig(object):
    def setupUi(self, DatabaseConfig):
        DatabaseConfig.setObjectName(_fromUtf8("DatabaseConfig"))
        DatabaseConfig.resize(320, 240)
        self.gridLayout = QtGui.QGridLayout(DatabaseConfig)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pb_accept = QtGui.QPushButton(DatabaseConfig)
        self.pb_accept.setObjectName(_fromUtf8("pb_accept"))
        self.gridLayout.addWidget(self.pb_accept, 6, 1, 1, 1)
        self.lb_server = QtGui.QLabel(DatabaseConfig)
        self.lb_server.setObjectName(_fromUtf8("lb_server"))
        self.gridLayout.addWidget(self.lb_server, 2, 0, 1, 1)
        self.lb_user = QtGui.QLabel(DatabaseConfig)
        self.lb_user.setObjectName(_fromUtf8("lb_user"))
        self.gridLayout.addWidget(self.lb_user, 3, 0, 1, 1)
        self.lb_pass = QtGui.QLabel(DatabaseConfig)
        self.lb_pass.setObjectName(_fromUtf8("lb_pass"))
        self.gridLayout.addWidget(self.lb_pass, 4, 0, 1, 1)
        self.lb_basename = QtGui.QLabel(DatabaseConfig)
        self.lb_basename.setObjectName(_fromUtf8("lb_basename"))
        self.gridLayout.addWidget(self.lb_basename, 5, 0, 1, 1)
        self.le_server = QtGui.QLineEdit(DatabaseConfig)
        self.le_server.setObjectName(_fromUtf8("le_server"))
        self.gridLayout.addWidget(self.le_server, 2, 1, 1, 2)
        self.le_user = QtGui.QLineEdit(DatabaseConfig)
        self.le_user.setObjectName(_fromUtf8("le_user"))
        self.gridLayout.addWidget(self.le_user, 3, 1, 1, 2)
        self.le_basename = QtGui.QLineEdit(DatabaseConfig)
        self.le_basename.setObjectName(_fromUtf8("le_basename"))
        self.gridLayout.addWidget(self.le_basename, 5, 1, 1, 2)
        self.pb_cancel = QtGui.QPushButton(DatabaseConfig)
        self.pb_cancel.setObjectName(_fromUtf8("pb_cancel"))
        self.gridLayout.addWidget(self.pb_cancel, 6, 2, 1, 1)
        self.le_pass = QtGui.QLineEdit(DatabaseConfig)
        self.le_pass.setEchoMode(QtGui.QLineEdit.Password)
        self.le_pass.setObjectName(_fromUtf8("le_pass"))
        self.gridLayout.addWidget(self.le_pass, 4, 1, 1, 2)
        self.lb_info = QtGui.QLabel(DatabaseConfig)
        self.lb_info.setMaximumSize(QtCore.QSize(16777215, 16))
        self.lb_info.setObjectName(_fromUtf8("lb_info"))
        self.gridLayout.addWidget(self.lb_info, 0, 1, 1, 2)

        self.retranslateUi(DatabaseConfig)
        QtCore.QMetaObject.connectSlotsByName(DatabaseConfig)

    def retranslateUi(self, DatabaseConfig):
        DatabaseConfig.setWindowTitle(QtGui.QApplication.translate("DatabaseConfig", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_accept.setText(QtGui.QApplication.translate("DatabaseConfig", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_server.setText(QtGui.QApplication.translate("DatabaseConfig", "Servidor", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_user.setText(QtGui.QApplication.translate("DatabaseConfig", "Usuario", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_pass.setText(QtGui.QApplication.translate("DatabaseConfig", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_basename.setText(QtGui.QApplication.translate("DatabaseConfig", "Base", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_cancel.setText(QtGui.QApplication.translate("DatabaseConfig", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_info.setText(QtGui.QApplication.translate("DatabaseConfig", "Datos de conexion ", None, QtGui.QApplication.UnicodeUTF8))


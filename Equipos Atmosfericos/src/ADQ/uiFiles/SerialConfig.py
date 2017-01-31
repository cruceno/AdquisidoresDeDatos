# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SerialConfig.ui'
#
# Created: Tue Feb 02 15:56:28 2016
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SerialConfig(object):
    def setupUi(self, SerialConfig):
        SerialConfig.setObjectName(_fromUtf8("SerialConfig"))
        SerialConfig.setWindowModality(QtCore.Qt.WindowModal)
        SerialConfig.resize(319, 276)
        SerialConfig.setModal(True)
        self.gridLayout = QtGui.QGridLayout(SerialConfig)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lb_parity = QtGui.QLabel(SerialConfig)
        self.lb_parity.setObjectName(_fromUtf8("lb_parity"))
        self.gridLayout.addWidget(self.lb_parity, 2, 0, 1, 1)
        self.cb_stopbits = QtGui.QComboBox(SerialConfig)
        self.cb_stopbits.setObjectName(_fromUtf8("cb_stopbits"))
        self.gridLayout.addWidget(self.cb_stopbits, 3, 1, 1, 1)
        self.lb_stopbits = QtGui.QLabel(SerialConfig)
        self.lb_stopbits.setObjectName(_fromUtf8("lb_stopbits"))
        self.gridLayout.addWidget(self.lb_stopbits, 3, 0, 1, 1)
        self.lb_port = QtGui.QLabel(SerialConfig)
        self.lb_port.setObjectName(_fromUtf8("lb_port"))
        self.gridLayout.addWidget(self.lb_port, 0, 0, 1, 1)
        self.cb_port = QtGui.QComboBox(SerialConfig)
        self.cb_port.setObjectName(_fromUtf8("cb_port"))
        self.gridLayout.addWidget(self.cb_port, 0, 1, 1, 1)
        self.cb_parity = QtGui.QComboBox(SerialConfig)
        self.cb_parity.setObjectName(_fromUtf8("cb_parity"))
        self.gridLayout.addWidget(self.cb_parity, 2, 1, 1, 1)
        self.cb_baudrate = QtGui.QComboBox(SerialConfig)
        self.cb_baudrate.setObjectName(_fromUtf8("cb_baudrate"))
        self.gridLayout.addWidget(self.cb_baudrate, 1, 1, 1, 1)
        self.lb_bytesize = QtGui.QLabel(SerialConfig)
        self.lb_bytesize.setObjectName(_fromUtf8("lb_bytesize"))
        self.gridLayout.addWidget(self.lb_bytesize, 4, 0, 1, 1)
        self.pb_cancel = QtGui.QPushButton(SerialConfig)
        self.pb_cancel.setObjectName(_fromUtf8("pb_cancel"))
        self.gridLayout.addWidget(self.pb_cancel, 6, 1, 1, 1)
        self.cb_bytesize = QtGui.QComboBox(SerialConfig)
        self.cb_bytesize.setObjectName(_fromUtf8("cb_bytesize"))
        self.gridLayout.addWidget(self.cb_bytesize, 4, 1, 1, 1)
        self.lb_baudrate = QtGui.QLabel(SerialConfig)
        self.lb_baudrate.setObjectName(_fromUtf8("lb_baudrate"))
        self.gridLayout.addWidget(self.lb_baudrate, 1, 0, 1, 1)
        self.pb_accept = QtGui.QPushButton(SerialConfig)
        self.pb_accept.setObjectName(_fromUtf8("pb_accept"))
        self.gridLayout.addWidget(self.pb_accept, 6, 0, 1, 1)
        self.lb_puntos = QtGui.QLabel(SerialConfig)
        self.lb_puntos.setObjectName(_fromUtf8("lb_puntos"))
        self.gridLayout.addWidget(self.lb_puntos, 5, 0, 1, 1)
        self.sb_puntos = QtGui.QSpinBox(SerialConfig)
        self.sb_puntos.setMinimum(1)
        self.sb_puntos.setMaximum(60)
        self.sb_puntos.setObjectName(_fromUtf8("sb_puntos"))
        self.gridLayout.addWidget(self.sb_puntos, 5, 1, 1, 1)

        self.retranslateUi(SerialConfig)
        QtCore.QMetaObject.connectSlotsByName(SerialConfig)

    def retranslateUi(self, SerialConfig):
        SerialConfig.setWindowTitle(QtGui.QApplication.translate("SerialConfig", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_parity.setText(QtGui.QApplication.translate("SerialConfig", "Paridad", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_stopbits.setText(QtGui.QApplication.translate("SerialConfig", "Bits de Parada", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_port.setText(QtGui.QApplication.translate("SerialConfig", "Puerto Serie", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_bytesize.setText(QtGui.QApplication.translate("SerialConfig", "Bit de datos", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_cancel.setText(QtGui.QApplication.translate("SerialConfig", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_baudrate.setText(QtGui.QApplication.translate("SerialConfig", "Velocidad ", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_accept.setText(QtGui.QApplication.translate("SerialConfig", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_puntos.setText(QtGui.QApplication.translate("SerialConfig", "Puntos por hora", None, QtGui.QApplication.UnicodeUTF8))


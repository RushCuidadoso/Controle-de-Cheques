# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmmenu.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmmenu(object):
    def setupUi(self, frmmenu):
        frmmenu.setObjectName("frmmenu")
        frmmenu.setEnabled(True)
        frmmenu.resize(1128, 438)
        self.groupBox = QtWidgets.QGroupBox(frmmenu)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 311, 371))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.btnlista = QtWidgets.QPushButton(self.groupBox)
        self.btnlista.setGeometry(QtCore.QRect(60, 260, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnlista.setFont(font)
        self.btnlista.setObjectName("btnlista")
        self.btnabrirparametros = QtWidgets.QPushButton(self.groupBox)
        self.btnabrirparametros.setGeometry(QtCore.QRect(60, 150, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnabrirparametros.setFont(font)
        self.btnabrirparametros.setObjectName("btnabrirparametros")
        self.btnabrircheque = QtWidgets.QPushButton(self.groupBox)
        self.btnabrircheque.setGeometry(QtCore.QRect(60, 40, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnabrircheque.setFont(font)
        self.btnabrircheque.setObjectName("btnabrircheque")
        self.groupBox_2 = QtWidgets.QGroupBox(frmmenu)
        self.groupBox_2.setGeometry(QtCore.QRect(330, 10, 791, 421))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.btnimprimir = QtWidgets.QPushButton(self.groupBox_2)
        self.btnimprimir.setGeometry(QtCore.QRect(670, 390, 75, 23))
        self.btnimprimir.setObjectName("btnimprimir")
        self.tabla = QtWidgets.QTableWidget(self.groupBox_2)
        self.tabla.setEnabled(True)
        self.tabla.setGeometry(QtCore.QRect(10, 30, 771, 351))
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabla.setObjectName("tabla")
        self.tabla.setColumnCount(0)
        self.tabla.setRowCount(0)
        self.tabla.verticalHeader().setVisible(False)
        self.lblsinreg = QtWidgets.QLabel(self.groupBox_2)
        self.lblsinreg.setGeometry(QtCore.QRect(400, 190, 111, 21))
        self.lblsinreg.setObjectName("lblsinreg")
        self.lblfechamax = QtWidgets.QLabel(self.groupBox_2)
        self.lblfechamax.setGeometry(QtCore.QRect(250, 10, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblfechamax.setFont(font)
        self.lblfechamax.setObjectName("lblfechamax")
        self.lblindice = QtWidgets.QLabel(self.groupBox_2)
        self.lblindice.setGeometry(QtCore.QRect(380, 390, 46, 13))
        self.lblindice.setObjectName("lblindice")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(30, 390, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lblfechamin = QtWidgets.QLabel(self.groupBox_2)
        self.lblfechamin.setGeometry(QtCore.QRect(10, 10, 221, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblfechamin.setFont(font)
        self.lblfechamin.setObjectName("lblfechamin")
        self.lblsuma = QtWidgets.QLabel(self.groupBox_2)
        self.lblsuma.setGeometry(QtCore.QRect(90, 390, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblsuma.setFont(font)
        self.lblsuma.setObjectName("lblsuma")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(230, 10, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(frmmenu)
        self.tabla.cellClicked['int','int'].connect(self.lblindice.setNum)
        QtCore.QMetaObject.connectSlotsByName(frmmenu)
        frmmenu.setTabOrder(self.btnabrircheque, self.btnabrirparametros)
        frmmenu.setTabOrder(self.btnabrirparametros, self.btnlista)
        frmmenu.setTabOrder(self.btnlista, self.tabla)
        frmmenu.setTabOrder(self.tabla, self.btnimprimir)

    def retranslateUi(self, frmmenu):
        _translate = QtCore.QCoreApplication.translate
        frmmenu.setWindowTitle(_translate("frmmenu", "Menu Principal"))
        self.btnlista.setText(_translate("frmmenu", "Lista de cheques"))
        self.btnabrirparametros.setText(_translate("frmmenu", "Registro de parametros"))
        self.btnabrircheque.setText(_translate("frmmenu", "Registro de cheque"))
        self.btnimprimir.setText(_translate("frmmenu", "Imprimir"))
        self.lblsinreg.setText(_translate("frmmenu", "Sin Registros"))
        self.lblfechamax.setText(_translate("frmmenu", "TextLabel"))
        self.lblindice.setText(_translate("frmmenu", "TextLabel"))
        self.label.setText(_translate("frmmenu", "Total:"))
        self.lblfechamin.setText(_translate("frmmenu", "TextLabel"))
        self.lblsuma.setText(_translate("frmmenu", "TextLabel"))
        self.label_3.setText(_translate("frmmenu", "até"))

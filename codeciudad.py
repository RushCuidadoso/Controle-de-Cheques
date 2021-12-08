from PyQt5 import QtWidgets
import sys
import frmciudad
from codeconexion import conexion


class ciudadApp(QtWidgets.QMainWindow, frmciudad.Ui_frmciudad):
    conexion = conexion()
    caller = None
    buscar = "%%"

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.cancelar()
        self.consultar()
        self.setFixedWidth(830)
        self.setFixedHeight(260)
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        self.btnguardar.clicked.connect(self.guardar)
        self.tabla.cellClicked.connect(self.cargar)
        self.btneliminar.clicked.connect(self.eliminar)
        self.btneditar.clicked.connect(self.editar)
        self.bnd = 0
        self.lblindice.setVisible(False)
        # -----
        # self.tabla.setSortingEnabled(True)
        self.tabla.resizeRowsToContents()
        self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)

        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(True)
        # -----

    def iniciar(self, caller):
        self.caller = caller

    def closeEvent(self, evnt):
        self.caller.setEnabled(True)

    def cancelar(self):
        self.txtcod.clear()
        self.txtnom.clear()
        self.txtnom.setEnabled(False)
        self.btnnovo.setEnabled(True)
        self.btncancelar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btnguardar.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneliminar.setEnabled(False)

    def nuevo(self):
        self.bnd = 0
        self.txtcod.clear()
        self.txtnom.clear()
        self.txtnom.setEnabled(True)
        self.btnnovo.setEnabled(False)
        self.btncancelar.setEnabled(True)
        self.btnguardar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btneditar.setVisible(False)
        self.txtnom.setFocus()

    def editar(self):
        self.bnd = 1
        self.txtnom.setEnabled(True)
        self.btnnovo.setEnabled(False)
        self.btncancelar.setEnabled(True)
        self.btnguardar.setVisible(True)
        self.btnguardar.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btneliminar.setEnabled(False)
        self.txtnom.setFocus()

    def config(self):
        self.tabla.setColumnCount(2)
        self.tabla.setRowCount(int(self.rows[0]))
        lista = 'Codigo', 'Ciudad'
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0, 50)
        self.tabla.setColumnWidth(1, 319)

    def consultar(self):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from cidade')
        self.rows = cur.fetchone()

        if int(self.rows[0]) > 0:
            self.lblsinreg.setVisible(False)
            self.config()
            cur.execute('select cod_cidade, nom_cidade from cidade order by cod_cidade')
            self.cidade = cur.fetchall()

            for i in range(int(self.rows[0])):
                item = self.cidade[i]
                self.tabla.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.tabla.setItem(i, 1, QtWidgets.QTableWidgetItem(str(item[1])))

        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)

    def cargar(self):
        self.cancelar()
        index = int(self.lblindice.text())
        item = self.cidade[index]
        self.txtcod.setText(str(item[0]))
        self.txtnom.setText(str(item[1]))
        self.btnguardar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)

    def eliminar(self):
        cod = int(self.txtcod.text())
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from loja where cod_cidade=%s', [cod])
        rows = cur.fetchone()
        if int(rows[0]) == 0:
            if (QtWidgets.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?",
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes):
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute('delete from cidade where cod_cidade= %s', [cod])
                con.commit()
                self.cancelar()
                self.consultar()
                QtWidgets.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado",
                                                        QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.question(self, "Error ao eliminar registro",
                                                 "Esse registro tem uma loja registrada", QtWidgets.QMessageBox.Ok)

    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        nom = str(self.txtnom.text())
        if len(nom) > 3:
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute('insert into cidade (nom_cidade) values(%s)', [nom])
                con.commit()
                row = self.tabla.rowCount()
                self.tabla.selectRow(row - 1)
            else:
                cur.execute('update cidade set nom_cidade=%s where cod_cidade=%s', [nom, cod])
                con.commit()
            self.cancelar()
            self.consultar()
        else:
            QtWidgets.QMessageBox.information(self, "Caracteres insuficientes",
                                                    "Um campo nao cumpre os requisitos", QtWidgets.QMessageBox.Ok)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ciudadApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

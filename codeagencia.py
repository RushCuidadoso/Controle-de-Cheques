from PyQt5 import QtWidgets, QtGui
import sys
import frmagencia
from codeconexion import conexion


class agenciaApp(QtWidgets.QMainWindow, frmagencia.Ui_frmagencia):
    conexion = conexion()

    # caller = None
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.consultar()
        self.cancelar()
        self.setFixedWidth(830)
        self.setFixedHeight(260)
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        self.cbobanco.currentIndexChanged.connect(self.cargarbanco)
        self.tabla.cellClicked.connect(self.cargar)
        self.btneditar.clicked.connect(self.editar)
        self.btnguardar.clicked.connect(self.guardar)
        self.btneliminar.clicked.connect(self.eliminar)
        self.lblindice.setVisible(False)
        self.cargarbanco()
        # -----
        # -----

    def iniciar(self, caller):
        self.caller = caller

    def closeEvent(self, evnt):
        self.caller.setEnabled(True)

    def nuevo(self):
        self.bnd = 0
        self.txtnomagencia.setEnabled(True)
        self.txtnomagencia.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btnguardar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)
        self.cbobanco.setEnabled(True)
        self.cbobanco.setCurrentIndex(0)

    def editar(self):
        self.bnd = 1
        self.txtnomagencia.setEnabled(True)
        self.txtnomagencia.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btnguardar.setEnabled(True)
        self.btnguardar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)
        self.cbobanco.setEnabled(True)

    def cancelar(self):
        self.txtnomagencia.setEnabled(False)
        self.txtnomagencia.clear()
        self.txtcod.clear()
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btnguardar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(False)
        self.cbobanco.setEnabled(False)

    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        nom = str(self.txtnomagencia.text())
        banco = int(self.txtcodbanco.text())
        if len(nom) > 3:
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute(
                    'insert into agencia (num_agencia, cod_banco) values(%s,%s)', [nom, banco])
            else:
                cur.execute('update agencia set num_agencia=%s, cod_banco=%s where cod_agencia=%s', [nom, banco, cod])
            con.commit()
            self.cancelar()
            self.consultar()
        else:
            QtWidgets.QMessageBox.information(self, "Caracteres insuficientes",
                                                    "Um campo nao cumpre os requisitos", QtWidgets.QMessageBox.Ok)

    def config(self, rows):
        lista = 'Codigo', 'Agencia', 'Banco'
        self.tabla.setColumnCount(3)
        self.tabla.setRowCount(int(rows[0]))
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0, 50)
        self.tabla.setColumnWidth(1, 119)
        self.tabla.setColumnWidth(2, 200)
        self.tabla.resizeRowsToContents()
        self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)
        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(True)

    def consultar(self):
        self.tabla.setSortingEnabled(False)
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from agencia')
        rows = cur.fetchone()
        # self.rows=rows

        if int(rows[0]) > 0:
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute('select a.cod_agencia, a.num_agencia, b.nom_banco, b.cod_banco '
                        'from agencia a, banco b where a.cod_banco=b.cod_banco order by cod_agencia asc')
            self.agencia = cur.fetchall()

            for i in range(int(rows[0])):
                item = self.agencia[i]
                self.tabla.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.tabla.setItem(i, 1, QtWidgets.QTableWidgetItem(str(item[1])))
                self.tabla.setItem(i, 2, QtWidgets.QTableWidgetItem(str(item[2])))
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)
        self.consultarbanco(0)

    def cargar(self):
        self.cancelar()
        index = int(self.lblindice.text())
        item = self.agencia[index]
        self.txtcod.setText(str(item[0]))
        self.txtnomagencia.setText(str(item[1]))
        self.txtcodbanco.setText(str(item[3]))
        self.btnguardar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)
        # ----
        cantbanco = self.cbobanco.count()
        banco = item[2]
        for i in range(cantbanco):
            if self.cbobanco.itemText(i) == banco:
                self.cbobanco.setCurrentIndex(i)
                break
                # ----

    def consultarbanco(self, sel):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) as cant from banco')
        rowbanco = cur.fetchone()
        self.banco = int(rowbanco[0])
        cur.execute('select cod_banco, nom_banco from banco order by cod_banco')
        self.verbanco = cur.fetchall()
        self.cargarbanco()
        if self.banco > 0:
            self.cbobanco.setMaxVisibleItems(10)
            self.cbobanco.clear()
            cont = int(rowbanco[0] - 1)
            for row in range(self.banco):
                var = self.verbanco[cont]
                banco = var[1]
                self.cbobanco.insertItem(0, banco)
                cont = cont - 1
            self.cbobanco.setCurrentIndex(0)
        if sel != 0:
            for cont in range(self.banco):
                carg = self.verbanco[cont]
                if sel == int(carg[0]):
                    self.cboconta.setCurrentIndex(cont)
                    break

    def cargarbanco(self):
        if self.banco > 0:
            valor = self.cbobanco.currentIndex()
            item = self.verbanco[int(valor)]
            self.txtcodbanco.setText(str(item[0]))

    def eliminar(self):
        cod = int(self.txtcod.text())
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from conta where cod_agencia=%s', [cod])
        rows = cur.fetchone()
        if int(rows[0]) == 0:
            if (QtGui.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?",
                                           QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes):
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute('delete from agencia where cod_agencia = %s', [cod])
                con.commit()
                self.cancelar()
                self.consultar()
                QtWidgets.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado",
                                                        QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.question(self, "Error ao eliminar registro",
                                                 "Esse registro tem uma conta registrada", QtWidgets.QMessageBox.Ok)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = agenciaApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

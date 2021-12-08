from PyQt5 import QtWidgets
import sys
import frmloja
from codeconexion import conexion


class lojaApp(QtWidgets.QMainWindow, frmloja.Ui_frmloja):
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
        self.cbocidade.currentIndexChanged.connect(self.cargarcidade)
        self.tabla.cellClicked.connect(self.cargar)
        self.btneditar.clicked.connect(self.editar)
        self.btnguardar.clicked.connect(self.guardar)
        self.btneliminar.clicked.connect(self.eliminar)
        self.lblindice.setVisible(False)
        self.cargarcidade()
        # -----

        # -----

    def iniciar(self, caller):
        self.caller = caller

    def closeEvent(self, evnt):
        self.caller.setEnabled(True)

    def nuevo(self):
        self.cancelar()
        self.bnd = 0
        self.txtnomloja.setEnabled(True)
        self.txtnomloja.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btnguardar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)
        self.cbocidade.setEnabled(True)
        self.cbocidade.setCurrentIndex(0)

    def editar(self):
        self.bnd = 1
        self.txtnomloja.setEnabled(True)
        self.txtnomloja.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btnguardar.setEnabled(True)
        self.btnguardar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)
        self.cbocidade.setEnabled(True)

    def cancelar(self):
        self.txtnomloja.setEnabled(False)
        self.txtnomloja.clear()
        self.txtcod.clear()
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btnguardar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(False)
        self.cbocidade.setEnabled(False)

    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        nom = str(self.txtnomloja.text())
        cidade = int(self.txtcodcidade.text())
        if len(nom) > 3:
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute('insert into loja (nom_loja, cod_cidade) values(%s,%s)', [nom, cidade])
            else:
                cur.execute('update loja set nom_loja=%s, cod_cidade=%s where cod_loja=%s', [nom, cidade, cod])
            con.commit()
            self.cancelar()
            self.consultar()
        else:
            QtWidgets.QMessageBox.information(self, "Caracteres insuficientes",
                                                    "Um campo nao cumpre os requisitos", QtWidgets.QMessageBox.Ok)

    def config(self, rows):
        lista = 'Codigo', 'Loja', 'Cidade'
        self.tabla.setColumnCount(3)
        self.tabla.setRowCount(int(rows[0]))
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0, 50)
        self.tabla.setColumnWidth(1, 119)
        self.tabla.setColumnWidth(2, 200)
        self.tabla.setSortingEnabled(True)
        self.tabla.resizeRowsToContents()
        self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)

        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(True)

    def consultar(self):

        self.tabla.setSortingEnabled(False)
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from loja')
        rows = cur.fetchone()

        if int(rows[0]) > 0:
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute('select a.cod_loja, a.nom_loja, b.nom_cidade, b.cod_cidade '
                        'from loja a, cidade b where a.cod_cidade=b.cod_cidade order by a.cod_loja asc')
            self.loja = cur.fetchall()

            for i in range(int(rows[0])):
                item = self.loja[i]
                self.tabla.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.tabla.setItem(i, 1, QtWidgets.QTableWidgetItem(str(item[1])))
                self.tabla.setItem(i, 2, QtWidgets.QTableWidgetItem(str(item[2])))
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)
        self.consultarcidade(0)

    def cargar(self):
        self.cancelar()
        index = int(self.lblindice.text())
        item = self.loja[index]
        self.txtcod.setText(str(item[0]))
        self.txtnomloja.setText(str(item[1]))
        self.txtcodcidade.setText(str(item[3]))
        self.btnguardar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)
        # ----
        cantcidade = self.cbocidade.count()
        for i in range(cantcidade):
            if self.cbocidade.itemText(i) == cantcidade:
                self.cbocidade.setCurrentIndex(i)
                break
                # ----

    def consultarcidade(self, sel):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from cidade')
        rowcidade = cur.fetchone()
        self.cidade = int(rowcidade[0])
        cur.execute('select cod_cidade, nom_cidade from cidade order by cod_cidade')
        self.vercidade = cur.fetchall()
        self.cargarcidade()
        if self.cidade > 0:
            self.cbocidade.setMaxVisibleItems(10)
            self.cbocidade.clear()
            cont = int(rowcidade[0] - 1)
            for row in range(self.cidade):
                var = self.vercidade[cont]
                cidade = var[1]
                self.cbocidade.insertItem(0, cidade)
                cont = cont - 1
            self.cbocidade.setCurrentIndex(0)
        if sel != 0:
            for cont in range(self.cidade):
                carg = self.vercidade[cont]
                if sel == int(carg[0]):
                    self.cbocidade.setCurrentIndex(cont)
                    break

    def cargarcidade(self):
        if self.cidade > 0:
            valor = self.cbocidade.currentIndex()
            item = self.vercidade[int(valor)]
            self.txtcodcidade.setText(str(item[0]))

    def eliminar(self):
        cod = int(self.txtcod.text())
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from cheque where cod_loja=%s', [cod])
        rows = cur.fetchone()
        if int(rows[0]) == 0:
            if (QtWidgets.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?",
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes):
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute('delete from loja where cod_loja = %s', [cod])
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
    form = lojaApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
